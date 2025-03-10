from typing import Literal
from pydantic import ValidationError
from .api_common import get_json, NomisStructure, StrictObject
from ...logger import logger
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
## 

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

class ConceptResponse(StrictObject):
    structure: Structure


def get_concept(conceptref: str) -> str:
    """
    **DEPRECATED**: use conceptref.replace('_', ' ').title()

    Get the name of a concept from the API.

    Deprecated because NOMIS do not store anything interesting against conceptref.
    There are hundreds of API calls to make, all mapping a conceptref to an obviously derived name:

    "UNIT_MULTIPLIER": "Unit Multiplier",
    "SOC2020_FULL": "Soc2020 full",
    "OCCPUK113_HRPPUK11": "Occpuk113 hrppuk11",
    "ICDGP_CONDITION": "Icdgp condition",

    The only exception found (2025-03-10) is "FREQ": "Frequency" which is not exciting enough to be worthwhile.
    Title-casing the ID gives the same result as sending a GET request.
    """
    logger.warning(f"get_concept({conceptref}) is deprecated. Use conceptref.replace('_', ' ').title()")
    # --
    obj = get_json(f'/concept/{conceptref}.def.sdmx.json')
    try:
        parsed = ConceptResponse(**obj)
    except ValidationError as e:
        logger.error(json.dumps(obj, indent=2))
        raise ValueError(f"Invalid concept response: {e}") from e
    if parsed.structure.concepts is None:
        logger.warning(f"No concepts found for {conceptref}")
        return conceptref
    return parsed.structure.concepts.concept.name.value

