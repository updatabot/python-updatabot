from .schema.ResponseDataset import KeyFamily
from . import api
import json
from typing import List
from collections import OrderedDict


def indent(s: str, width: int = 2) -> str:
    return "\n".join(f"{' ' * width}{line}" for line in s.splitlines())


def rpad(s: str, width: int) -> str:
    return s + ' ' * (width - len(s))


class NomisSearchHitAnnotations:
    """
    Use our judgement to extract the most useful annotations.
    """

    def __init__(self, keyfamily: KeyFamily):
        tmp = {
            a.annotationtitle: a.annotationtext for a in keyfamily.annotations.annotation
        }
        def getstr(k): return str(tmp.get(k)) if k in tmp else None
        self.units = getstr('Units')
        self.mnemonic = getstr('Mnemonic')
        self.sources = getstr('contenttype/sources')
        self.subdescription = getstr('SubDescription')
        self.metadata_count = getstr('MetadataCount')
        self.geoglevel = getstr('contenttype/geoglevel')
        self.first_released = getstr('FirstReleased')
        self.last_updated = getstr('LastUpdated')
        self.census_release = getstr('contenttype/censusrelease')

    def __str__(self):
        tmp = [f"{k.title()}\t= {json.dumps(v)}" for (k, v)
               in vars(self).items() if v]
        return "\n".join(tmp)

    def _repr_html_(self):
        tmp = [
            f"<li><strong>{k.title()}</strong>: {v}</li>" for (k, v) in vars(self).items() if v]
        return f"<ul>{''.join(tmp)}</ul>"


class NomisSearchHitDimensions:
    """
    Extract a tightly structured set of dimensions.
    There are hundreds of single-use dimensions, but we capture those
    which appear in >20% of NOMIS datasets for easy fetching.
    """

    def __init__(self, keyfamily: KeyFamily):
        # Always present.
        # eg. "CL_1_1_TIME" or "CL_37_1_TIME"
        self.time = keyfamily.components.timedimension.codelist
        # Always present
        self.freq = None
        self.measures = None
        # Optional, but mostly present
        self.geography = None
        self.age = None
        self.c_age = None
        self.sex = None
        self.c_sex = None
        self.misc = OrderedDict()

        for d in keyfamily.components.dimension:
            if d.isfrequencydimension:
                # All datasets have one frequency dimension
                if self.freq is not None:
                    raise ValueError(f"Duplicate frequency dimensions")
                if d.conceptref != 'FREQ':
                    raise ValueError(f"Frequency dimension is not FREQ")
                self.freq = d.codelist

            elif d.conceptref == 'MEASURES':
                # All datasets have one measures dimension
                if self.measures is not None:
                    raise ValueError(f"Duplicate measures dimensions")
                self.measures = d.codelist

            elif d.conceptref == 'GEOGRAPHY':
                # [1584/1615] datasets have a geography dimension
                if self.geography is not None:
                    raise ValueError(f"Duplicate geography dimensions")
                self.geography = d.codelist

            elif d.conceptref == 'AGE':
                # 43 datasets have AGE
                if self.age is not None:
                    raise ValueError(f"Duplicate age dimensions")
                self.age = d.codelist
            elif d.conceptref == 'C_AGE':
                # 298 datasets have C_AGE
                if self.c_age is not None:
                    raise ValueError(f"Duplicate C_AGE dimensions")
                self.c_age = d.codelist

            elif d.conceptref == 'SEX':
                # 64 datasets have SEX
                if self.sex is not None:
                    raise ValueError(f"Duplicate sex dimensions")
                self.sex = d.codelist

            elif d.conceptref == 'C_SEX':
                # 335 datasets have C_SEX
                if self.c_sex is not None:
                    raise ValueError(f"Duplicate C_SEX dimensions")
                self.c_sex = d.codelist

            else:
                # conceptref is the URL key for the download.
                # codelist is used to look up valid values
                if d.conceptref in self.misc:
                    raise ValueError(f"Duplicate dimension {d.conceptref}")
                self.misc[d.conceptref] = d.codelist

    def __iter__(self):
        """List the dimensions available on this dataset"""
        usual_suspects = ['time', 'geography', 'freq',
                          'measures', 'age', 'c_age', 'sex', 'c_sex']
        for x in usual_suspects:
            if getattr(self, x):
                yield x
        for key in self.misc:
            yield key.lower()

    def __str__(self):
        return json.dumps(list(self))

    def _repr_html_(self):
        return ' '.join([f'<code>{x}</code>' for x in self])


class NomisSearchHit:
    """
    Represents a cleaned-up version of the JSON API response.
    A search hit has an ID, name, description, and some annotations.
    It lists the IDs of dimensions, which are a foreign key into Codelists.
    """

    def __init__(self, keyfamily: KeyFamily):
        # Important!
        self.id = keyfamily.id

        # eg. "Jobseeker's Allowance with rates and proportions"
        self.name = keyfamily.name.value

        # eg. "Records the number of people claiming Jobseeker's..."
        self.description = keyfamily.description.value if keyfamily.description else None

        self.annotations = NomisSearchHitAnnotations(keyfamily)
        self.dimensions = NomisSearchHitDimensions(keyfamily)
        self.is_current = None
        current_annotation = next(
            (a for a in keyfamily.annotations.annotation if a.annotationtitle == 'Status'), None)
        if current_annotation:
            text = current_annotation.annotationtext
            if text == 'Current (being actively updated)':
                self.is_current = True
            elif text == 'Historical (not actively being updated)':
                self.is_current = False
            else:
                raise ValueError(f"Unknown status: {text}")
        keywords_annotation = next(
            (a for a in keyfamily.annotations.annotation if a.annotationtitle == 'Keywords'), None)
        if keywords_annotation:
            self.keywords = keywords_annotation.annotationtext.split(',')
        else:
            self.keywords = []

    def __stringpairs__(self):
        out = OrderedDict()
        out['Is Current'] = self.is_current
        out['Last Updated'] = self.annotations.last_updated
        out['First Released'] = self.annotations.first_released
        out['Description'] = self.description
        if self.annotations.subdescription:
            out['SubDescription'] = self.annotations.subdescription
        out['Dimensions'] = list(self.dimensions)
        out['Keywords'] = self.keywords
        if self.annotations.geoglevel:
            out['Geoglevel'] = self.annotations.geoglevel
        if self.annotations.census_release:
            out['CensusRelease'] = self.annotations.census_release
        return out

    def __str__(self):
        header = f"{self.id} {json.dumps(self.name)}"
        parts = [f'{rpad(k, 20)}: {json.dumps(v)}' for (
            k, v) in self.__stringpairs__().items()]
        return header + "\n" + indent("\n".join(parts))

    def _repr_html_(self):
        """Rich HTML representation for IPython/Jupyter"""
        html = [
            f"<div style='margin:10px; padding:10px; border:1px solid #ddd; border-radius:5px'>",
            f"<h3><code style='float:right'>{self.id}</code>{self.name}</h3>",
            f"<p>{self.description}</p>" if self.description else "",
            f"<p>{self.annotations.subdescription}</p>" if self.annotations.subdescription else "",
            f'<table>',
        ]
        for (k, v) in self.__stringpairs__().items():
            if k in ['Description', 'SubDescription']:
                continue
            if isinstance(v, list):
                v = list(map(lambda x: f"<code>{x}</code>", v))
                v = ' '.join(v) if len(v) else '<em>none</em>'
            else:
                v = json.dumps(v)
                v = '<code>' + v + '</code>'
            html.append(
                f"<tr><td align='right'><strong>{k}</strong></td><td align='left'>{v}</td></tr>")
        html.append(f"</table>")
        html.append("</div>")
        return "\n".join(html)


def search(query: str = None) -> List[NomisSearchHit]:
    """
    Search for datasets by name or description.
    """
    resp = api.fetch_search(query)
    keyfamilies = resp.structure.keyfamilies.keyfamily if resp.structure.keyfamilies else []
    return [NomisSearchHit(k) for k in keyfamilies]
