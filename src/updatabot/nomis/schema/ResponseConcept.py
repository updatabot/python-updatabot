from typing import Literal
from .NomisStructure import NomisStructure, StrictObject

# ---
# NOMIS API: Get the name of a 'concept'
#  /api/v01/concept/{conceptref}.def.sdmx.json
#
# This is a heavyweight wrapper around a single string!
# ---

## fmt: off
## Example JSON response:
##
## {
##   "structure": {
##     "concepts": {
##       "concept": {
##         "agencyid": "NOMIS",
##         "id": "TIME_FORMAT",
##         "name": {
##           "value": "Time Format",
##           "lang": "en"
##         },
##         "uri": "",
##         "version": ""
##       }
##     },
##     "header": {
##       "id": "none",
##       "prepared": "2025-03-10T15:19:26Z",
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


class Name(StrictObject):
    value: str
    lang: Literal["en"]


class Concept(StrictObject):
    name: Name
    # From request:
    id: str
    # Ignored:
    agencyid: Literal["NOMIS"]
    uri: Literal[""]
    version: Literal[""]


class Concepts(StrictObject):
    concept: Concept


class Structure(NomisStructure):
    concepts: Concepts | None = None


class ResponseConcept(StrictObject):
    structure: Structure
