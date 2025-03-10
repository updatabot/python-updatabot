from pydantic import Field
from typing import List, Optional, Literal, Annotated, Union
from .api_common import get_json, NomisStructure, StrictObject
from urllib.parse import urlencode

# ---
# NOMIS API: Full dataset list
#  /api/v01/dataset/def.sdmx.json
#
# This API supports ?search params, but we can do that locally.
# Requesting them all (~1600 objects) gives better cache performance.
# ---

## fmt: off
## Example JSON response:
## {
##   "structure": {
##     "header": {
##       "id": "none",
##       "prepared": "2025-03-10T10:19:25Z",
##       "sender": {
##         "contact": {
##           "email": "support@nomisweb.co.uk",
##           "name": "Nomis",
##           "telephone": "+44(0) 191 3342680",
##           "uri": "https://www.nomisweb.co.uk"
##         },
##         "id": "NOMIS"
##       },
##       "test": "false"
##     },
##     "keyfamilies": {
##       "keyfamily": [
##         {
##           "agencyid": "NOMIS",
##           "annotations": {
##             "annotation": [
##               {
##                 "annotationtext": "Current (being actively updated)",
##                 "annotationtitle": "Status"
##               },
##               ...
##             ]
##           },
##           "id": "NM_1_1",
##           "components": {
##             "attribute": [
##               {
##                 "assignmentstatus": "Mandatory",
##                 "attachmentlevel": "Observation",
##                 "codelist": "CL_OBS_STATUS",
##                 "conceptref": "OBS_STATUS"
##               },
##             ],
##             "dimension": [
##               {
##                 "codelist": "CL_1_1_GEOGRAPHY",
##                 "conceptref": "GEOGRAPHY"
##               },
##             ],
##             "primarymeasure": {
##               "conceptref": "OBS_VALUE"
##             },
##             "timedimension": {
##               "codelist": "CL_1_1_TIME",
##               "conceptref": "TIME"
##             }
##           },
##           "description": {
##             "value": "Records the number of people claiming Jobseeker's Allowance (JSA) and National Insurance credits at Jobcentre Plus local offices. This is not an official measure of unemployment, but is the only indicative statistic available for areas smaller than Local Authorities.",
##             "lang": "en"
##           },
##           "name": {
##             "value": "Jobseeker's Allowance with rates and proportions",
##             "lang": "en"
##           },
##           "uri": "Nm-1d1",
##           "version": 1.0
##         },
##         ...
##       ]
##     },
##     "xmlns": "http://www.SDMX.org/resources/SDMXML/schemas/v2_0/message",
##     "common": "http://www.SDMX.org/resources/SDMXML/schemas/v2_0/common",
##     "structure": "http://www.SDMX.org/resources/SDMXML/schemas/v2_0/structure",
##     "xsi": "http://www.w3.org/2001/XMLSchema-instance",
##     "schemalocation": "http://sdmx.org/docs/2_0/SDMXMessage.xsd"
##   }
## }
## fmt: on

# ------- JSON Response Schema -------


class Annotation(StrictObject):
    annotationtext: str | int | float | None
    # From JSON analysis - Common Annotation titles:
    #   1615 	 Status
    #   1615 	 Units
    #   1615 	 Mnemonic
    #   1572 	 contenttype/sources
    #   1568 	 SubDescription
    #   1519 	 Keywords
    #   1460 	 MetadataCount
    #   1402 	 MetadataText0
    #   1402 	 MetadataText1
    #   1385 	 contenttype/geoglevel
    #   1338 	 MetadataTitle1
    #   1305 	 FirstReleased
    #   1305 	 LastUpdated
    #   748 	 contenttype/censusrelease
    #   375 	 MetadataTitle0
    #   320 	 contenttype/2001census
    #   97    	 LastRevised
    #   58   	 MetadataText
    #   38   	 MetadataText2
    #   37   	 MetadataTitle2
    #   36   	 MetadataTitle
    #   28   	 contenttype/1961census
    #   8   	 contenttype/1921census
    #   1   	 contenttype/sorting
    #   1   	 MetadataTitle3
    #   1   	 MetadataText3
    annotationtitle: str


class Annotations(StrictObject):
    annotation: List[Annotation]


class PrimaryMeasure(StrictObject):
    conceptref: Literal["OBS_VALUE"]  # Ignorable


class TimeDimension(StrictObject):
    conceptref: Literal["TIME"]  # Ignorable
    codelist: str  # eg. "CL_1_1_TIME" or "CL_37_1_TIME"


class Dimension(StrictObject):
    codelist: str
    conceptref: str
    isfrequencydimension: Optional[bool] = None


class AttributeStatus(StrictObject):
    assignmentstatus: Literal["Mandatory"]
    attachmentlevel: Literal["Observation"]
    codelist: Literal["CL_OBS_STATUS"]
    conceptref: Literal["OBS_STATUS"]


class AttributeRound(StrictObject):
    assignmentstatus: Literal["Conditional"]
    attachmentlevel: Literal["Observation"]
    codelist: Literal["CL_OBS_ROUND"]
    conceptref: Literal["OBS_ROUND"]


class AttributeConf(StrictObject):
    assignmentstatus: Literal["Conditional"]
    attachmentlevel: Literal["Observation"]
    codelist: Literal["CL_OBS_CONF"]
    conceptref: Literal["OBS_CONF"]


class AttributeUnitMultiplier(StrictObject):
    assignmentstatus: Literal["Conditional"]
    attachmentlevel: Literal["Series"]
    codelist: Literal["CL_UNIT_MULT"]
    conceptref: Literal["UNIT_MULTIPLIER"]


class AttributeUnit(StrictObject):
    assignmentstatus: Literal["Mandatory"]
    attachmentlevel: Literal["Series"]
    codelist: Literal["CL_UNIT"]
    conceptref: Literal["UNIT"]


class AttributeTitleCompl(StrictObject):
    assignmentstatus: Literal["Mandatory"]
    attachmentlevel: Literal["Series"]
    conceptref: Literal["TITLE_COMPL"]


class AttributeTimeFormat(StrictObject):
    assignmentstatus: Literal["Mandatory"]
    attachmentlevel: Literal["Series"]
    codelist: Literal["CL_TIME_FORMAT"]
    conceptref: Literal["TIME_FORMAT"]


class Components(StrictObject):
    dimension: List[Dimension]
    timedimension: TimeDimension
    # [ignorable] No differentiation between datasets.
    primarymeasure: PrimaryMeasure  # Ignorable
    # [ignorable] No differentiation between datasets.
    # Attributes are very boring.
    # They look like they'd be interesting! But they're not.
    # They always take these 7 compound values, bound by this
    # tight discriminated union. All are always present.
    attribute: List[Annotated[
        Union[AttributeStatus,
              AttributeRound,
              AttributeConf,
              AttributeUnitMultiplier,
              AttributeUnit,
              AttributeTitleCompl,
              AttributeTimeFormat,
              ],
        Field(discriminator='conceptref')
    ]]


class LanguageValue(StrictObject):
    value: str
    lang: Literal["en"]


class KeyFamily(StrictObject):
    agencyid: Literal["NOMIS"]
    version: float  # Always 1.0
    id: str
    description: Optional[LanguageValue] = None
    name: LanguageValue
    uri: str  # eg. "Nm-2334d1"
    components: Components
    annotations: Annotations


class KeyFamilies(StrictObject):
    keyfamily: List[KeyFamily]


class Structure(NomisStructure):
    keyfamilies: KeyFamilies


class DatasetList(StrictObject):
    structure: Structure

# ------- End of JSON Response Schema -------

# ------- Fetch & Parse -------


class NomisDatasetAnnotations:
    """
    Use our judgement to extract the most useful annotations.
    """

    def __init__(self, keyfamily: KeyFamily):
        tmp = {
            a.annotationtitle: a.annotationtext for a in keyfamily.annotations.annotation
        }
        def getstr(k): return str(tmp.get(k)) if k in tmp else None
        self.status = getstr('Status')
        self.units = getstr('Units')
        self.mnemonic = getstr('Mnemonic')
        self.sources = getstr('contenttype/sources')
        self.subdescription = getstr('SubDescription')
        self.keywords = getstr('Keywords')
        self.metadata_count = getstr('MetadataCount')
        self.geoglevel = getstr('contenttype/geoglevel')
        self.first_released = getstr('FirstReleased')
        self.last_updated = getstr('LastUpdated')
        self.census_release = getstr('contenttype/censusrelease')

    def __str__(self):
        return f"""  [annotations]
    Status: {self.status}
    Units: {self.units}
    Mnemonic: {self.mnemonic}
    Sources: {self.sources}
    SubDescription: {self.subdescription}
    Keywords: {self.keywords}
    MetadataCount: {self.metadata_count}
    Geoglevel: {self.geoglevel}
    FirstReleased: {self.first_released}
    LastUpdated: {self.last_updated}
    CensusRelease: {self.census_release}"""


class NomisDatasetDimensions:
    """
    Extract a tightly structured set of dimensions.
    There are hundreds of single-use dimensions, but we capture those
    which appear in >20% of NOMIS datasets for easy fetching.
    """

    def __init__(self, keyfamily: KeyFamily):
        self.freq = None
        self.measures = None
        self.geo = None
        self.age = None
        self.sex = None
        self.misc = []

        # Always present.
        # eg. "CL_1_1_TIME" or "CL_37_1_TIME"
        self.time = keyfamily.components.timedimension.codelist

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
                if self.geo is not None:
                    raise ValueError(f"Duplicate geography dimensions")
                self.geo = d.codelist

            elif d.conceptref == 'AGE' or d.conceptref == 'C_AGE':
                # 298 datasets have C_AGE
                # 43 datasets have AGE
                if self.age is not None:
                    raise ValueError(f"Duplicate age dimensions")
                self.age = d.codelist

            elif d.conceptref == 'C_SEX' or d.conceptref == 'SEX':
                # 335 datasets have C_SEX
                # 64 datasets have SEX
                if self.sex is not None:
                    raise ValueError(f"Duplicate sex dimensions")
                self.sex = d.codelist

            else:
                # conceptref has very little information to offer beyond this point.
                # Values are like "C_TENHUK11", which isn't descriptive.
                if d.codelist in self.misc:
                    raise ValueError(f"Duplicate dimension {d.codelist}")
                self.misc.append(d.codelist)

    def __str__(self):
        return f"""  [dimensions]
    Freq: {self.freq}
    Measures: {self.measures}
    Geo: {self.geo}
    Age: {self.age}
    Sex: {self.sex}
    Misc: {', '.join(self.misc)}"""


class NomisDataset:
    def __init__(self, keyfamily: KeyFamily):
        # Important!
        self.id = keyfamily.id

        # eg. "Jobseeker's Allowance with rates and proportions"
        self.name = keyfamily.name.value

        # eg. "Records the number of people claiming Jobseeker's..."
        self.description = keyfamily.description.value if keyfamily.description else None

        self.annotations = NomisDatasetAnnotations(keyfamily)
        self.dimensions = NomisDatasetDimensions(keyfamily)

    def __str__(self):
        return f"""[dataset] {self.id}
Name: {self.name}
Description: {self.description}
{self.dimensions}
{self.annotations}"""


def get_datasets(search=None) -> List[NomisDataset]:
    if search:
        obj = get_json(
            f'/dataset/def.sdmx.json?{urlencode({"search": search})}')
    else:
        obj = get_json('/dataset/def.sdmx.json')

    parsed = DatasetList(**obj)
    return [NomisDataset(k) for k in parsed.structure.keyfamilies.keyfamily]
