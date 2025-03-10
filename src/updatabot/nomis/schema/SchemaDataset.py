from pydantic import Field
from typing import List, Optional, Literal, Annotated, Union
from .SchemaCommon import NomisStructure, StrictObject

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


class SchemaDataset(StrictObject):
    structure: Structure
