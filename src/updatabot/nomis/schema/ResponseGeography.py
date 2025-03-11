from .NomisStructure import NomisStructure, StrictObject
from typing import List, Optional

## fmt: off
## {
##   "structure": {
##     "codelists": {
##       "codelist": [
##         {
##           "agencyid": "NOMIS",
##           "id": "CL_162_1_GEOGRAPHY",
##           "code": [
##             {
##               "annotations": {
##                 "annotation": [
##                   {
##                     "annotationtext": "countries",
##                     "annotationtitle": "TypeName"
##                   },
##                   ...
##                 ]
##               },
##               "description": {
##                 "value": "United Kingdom",
##                 "lang": "en"
##               },
##               "value": 2092957697
##             },
##           ],
##           "name": {
##             "value": "geography",
##             "lang": "en"
##           },
##           "uri": ""
##         }
##       ]
##     },
##     "header": {
##       "id": "NM_162_1",
##       "prepared": "2025-03-09T09:12:57Z",
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
##     "xmlns": "http://www.SDMX.org/resources/SDMXML/schemas/v2_0/message",
##     "common": "http://www.SDMX.org/resources/SDMXML/schemas/v2_0/common",
##     "structure": "http://www.SDMX.org/resources/SDMXML/schemas/v2_0/structure",
##     "xsi": "http://www.w3.org/2001/XMLSchema-instance",
##     "schemalocation": "http://sdmx.org/docs/2_0/SDMXMessage.xsd"
##   }
## }
## fmt: on


class Annotation(StrictObject):
    annotationtext: str | int
    annotationtitle: str


class Annotations(StrictObject):
    annotation: List[Annotation]


class Description(StrictObject):
    value: str
    lang: str


class Code(StrictObject):
    annotations: Annotations
    description: Description
    value: str | int
    parentcode: Optional[str | int] = None


class Name(StrictObject):
    value: str
    lang: str


class Codelist(StrictObject):
    agencyid: str
    id: str
    code: List[Code]
    name: Name
    uri: str


class Codelists(StrictObject):
    codelist: List[Codelist]


class Structure(NomisStructure):
    codelists: Codelists


class ResponseGeography(StrictObject):
    structure: Structure
