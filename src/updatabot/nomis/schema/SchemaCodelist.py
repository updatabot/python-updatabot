from typing import Literal, List, Optional
from .SchemaCommon import NomisStructure, StrictObject
import json

# ---
# NOMIS API: Get the name of a 'concept'
#  /api/v01/concept/{conceptref}.def.sdmx.json
#
# This is a heavyweight wrapper around a single string!
# ---

## fmt: off
## Example JSON response:
##
##  {
##    "structure": {
##      "codelists": {
##        "codelist": [
##          {
##            "agencyid": "NOMIS",
##            "id": "CL_162_1_AGE",
##            "code": [
##              {
##                "annotations": {
##                  "annotation": [
##                    {
##                      "annotationtext": 4,
##                      "annotationtitle": "ChildCount"
##                    },
##                    ...
##                  ]
##                },
##                "description": {
##                  "value": "All categories: Age 16+",
##                  "lang": "en"
##                },
##                "value": 0
##              },
##              ...
##            ],
##            "name": {
##              "value": "Age",
##              "lang": "en"
##            },
##            "uri": ""
##          }
##        ]
##      },
##      "header": {
##        "id": "NM_162_1",
##        "prepared": "2025-03-10T18:39:01Z",
##        "sender": {
##          "contact": {
##            "email": "support@nomisweb.co.uk",
##            "name": "Nomis",
##            "telephone": "+44(0) 191 3342680",
##            "uri": "https://www.nomisweb.co.uk"
##          },
##          "id": "NOMIS"
##        },
##        "test": "false"
##      },
##      "xmlns": "http://www.SDMX.org/resources/SDMXML/schemas/v2_0/message",
##      "common": "http://www.SDMX.org/resources/SDMXML/schemas/v2_0/common",
##      "structure": "http://www.SDMX.org/resources/SDMXML/schemas/v2_0/structure",
##      "xsi": "http://www.w3.org/2001/XMLSchema-instance",
##      "schemalocation": "http://sdmx.org/docs/2_0/SDMXMessage.xsd"
##    }
##  }

## fmt: on


class Annotation(StrictObject):
    annotationtext: int | str
    annotationtitle: str


class Annotations(StrictObject):
    annotation: List[Annotation]


class Description(StrictObject):
    value: str
    lang: Literal["en"]


class Name(StrictObject):
    value: str
    lang: Literal["en"]


class Code(StrictObject):
    annotations: Optional[Annotations] = None
    description: Description
    value: int | str
    parentcode: Optional[int] = None


class Codelist(StrictObject):
    agencyid: Literal["NOMIS"]
    id: str
    code: List[Code]
    name: Name
    uri: Literal[""]


class Codelists(StrictObject):
    codelist: List[Codelist]


class Structure(NomisStructure):
    codelists: Optional[Codelists] = None


class SchemaCodelist(StrictObject):
    structure: Structure
