from . import api
from .schema.ResponseDatasetOverview import Overview, Analysis, Dimension, Code, DimensionGeographyType
import json
from urllib.parse import urlencode
from updatabot import load_url, logger
import pandas as pd


def indent(s: str | list[str], prefix: str = "  "):
    if not isinstance(s, list):
        s = s.split("\n")
    return "\n".join(prefix + line for line in s)


def rpad(s: str, width: int):
    return s + ' ' * (width - len(s))


def lpad(s: str, width: int):
    return ' ' * (width - len(s)) + s


class NomisCode:
    def __init__(self, code: Code, is_default: bool = False):
        self.level = code.level
        self.name = code.name
        self.value = code.value
        self.is_default = is_default

    def __str__(self):
        indentation = '  ' * (self.level - 1)
        out = f"{indentation}[{self.value}] \"{self.name}\""
        if self.is_default:
            out += " [[DEFAULT]]"
        return out


class NomisQueryDimension:
    def __init__(self, dimension: Dimension):
        # Title, mostly matches key
        self.title = dimension.name
        # string; represents the "key" in the k/v querystring
        self.key = dimension.concept
        # List of values for the querystring
        self.values = []
        # Assume this is what gets preconfigured if not specified
        self.defaults = []
        if dimension.defaults:
            tmp = dimension.defaults.code
            if not isinstance(tmp, list):
                tmp = [tmp]
            self.defaults = [c.value for c in tmp]
        if dimension.codes:
            tmp = dimension.codes.code
            if not isinstance(tmp, list):
                tmp = [tmp]
            self.values = [
                NomisCode(c, is_default=c.value in self.defaults) for c in tmp]
        # Applies to geography (1568 times) and a handful
        # of other examples (less than 50). Not sure if useful.
        self.types = []
        if dimension.types:
            tmp = dimension.types.type
            self.types = tmp if isinstance(tmp, list) else [tmp]

    def __str__(self):
        out = f'key: {json.dumps(self.key)}'
        if self.title.lower() != self.key.lower():
            out += f" (aka \"{self.title}\")"
        if len(self.values) > 0:
            out += f'\n> values: ({len(self.values)})'
            out += '\n' + indent([str(c) for c in self.values])
        if len(self.types) > 0:
            out += '\n' + f"> value_types: ({len(self.types)})"
            out += '\n' + indent([str(x) for x in self.types])
        return out


class NomisQuery:
    """Stateful query object"""

    def __init__(self, overview: Overview):
        self.id = overview.id
        self.name = overview.name
        self.description = overview.description
        self.subdescription = overview.subdescription
        self.is_current = overview.status == 'Current (being actively updated)'
        self.firstreleased = overview.firstreleased
        self.lastrevised = overview.lastrevised
        self.lastupdated = overview.lastupdated
        self.nextupdate = overview.nextupdate
        # -- keywords
        self.keywords = overview.keywords
        if self.keywords:
            self.keywords = self.keywords.split(',')
        else:
            self.keywords = []
        # -- analyses: Sibling datasets.
        # eg.  NM_11_1 has { "NM_11_2": "average over a specific period" }
        tmp_analyses = overview.analyses.analysis
        if not isinstance(tmp_analyses, list):
            tmp_analyses = [tmp_analyses]
        self.siblings = {
            x.id: x.name for x in tmp_analyses if x.id != overview.id}
        # -- dimensions
        self.dimensions = [NomisQueryDimension(d)
                           for d in overview.dimensions.dimension]
        # -- units
        tmp_units = overview.units.unit
        if not isinstance(tmp_units, list):
            tmp_units = [tmp_units]
        self.units = ', '.join(u.name for u in tmp_units)
        # -- query state
        self.q_filters = {}
        self.q_select = []

    def __str__(self):
        out = f"NomisQuery[ {self.id} ] \"{self.name}\""
        for d in self.dimensions:
            if d.key in self.q_filters:
                out += f"\n> {lpad(json.dumps(d.key), 20)}\t= {json.dumps(self.q_filters[d.key])}"
            else:
                defaults = [v for v in d.values if v.is_default]
                for v in defaults:
                    out += f"\n> {lpad(json.dumps(d.key), 20)}\t= [DEFAULT] {json.dumps(v.value)}"
                if len(defaults) == 0:
                    out += f"\n> {lpad(json.dumps(d.key), 20)}\t= null"
        return out

    def dimension(self, key: str) -> NomisQueryDimension:
        out = next(
            (x for x in self.dimensions if x.key.lower() == key.lower()), None)
        if not out:
            raise ValueError(f"Dimension {key} not found")
        return out

    def select(self, *keys: str):
        self.q_select = list(keys)
        return self

    def _append_filter(self, key: str, value: str):
        if isinstance(self.q_filters.get(key), list):
            self.q_filters[key].append(value)
        elif self.q_filters.get(key):
            self.q_filters[key] = [self.q_filters[key], value]
        else:
            self.q_filters[key] = value

    def geography(self, value: str):
        self._append_filter('geography', value)
        return self

    def filter(self, key: str, name: str | None = None, value: str | int | None = None):
        if key == 'geography':
            raise ValueError("use .geography() instead")
        if not name and not value:
            raise ValueError("Must specify either name or value")
        if name and value:
            raise ValueError("Must specify either name or value, not both")
        available = self.dimension(key).values
        if name:
            match = next((x for x in available if x.name == name), None)
            if not match:
                raise ValueError(f"Name {name} not found in dimension {key}")
        if value:
            match = next((x for x in available if x.value == value), None)
            if not match:
                raise ValueError(f"Value {value} not found in dimension {key}")
        self._append_filter(key, match.value)
        return self

    def csv_url(self, limit=None) -> str:
        url = f"{api.BASE_URL}/dataset/{self.id}.data.csv"

        # Build query parameters
        params = {}
        if limit:
            params['RecordLimit'] = limit
        # Add all filters from self.filters
        for k, v in self.q_filters.items():
            if isinstance(v, list):
                params[k] = ','.join([str(s) for s in v])
            else:
                params[k] = str(v)
        if self.q_select:
            params['select'] = ','.join(self.q_select)

        # Append querystring if we have parameters
        if params:
            url = f"{url}?{urlencode(params)}"

        return url

    def dataframe(self, limit=None) -> pd.DataFrame:
        url = self.csv_url(limit)
        df = load_url(url)
        if len(df) == 25000:
            logger.warning(
                f"NOMIS returned max limit of 25000 rows. Apply more filters to ensure you're getting all your data.")
        return df


def query(id: str) -> NomisQuery:
    """
    Open a dataset for querying.
    """
    resp = api.fetch_dataset_overview(id)
    return NomisQuery(resp.overview)
