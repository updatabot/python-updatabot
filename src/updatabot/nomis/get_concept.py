from .fetch import fetch
from .schema import SchemaConcept
from pydantic import ValidationError
from updatabot import logger
import json


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
    logger.warning(
        f"get_concept({conceptref}) is deprecated. Use conceptref.replace('_', ' ').title()")
    # --
    obj = fetch(f'/concept/{conceptref}.def.sdmx.json')
    try:
        parsed = SchemaConcept(**obj)
    except ValidationError as e:
        logger.error(json.dumps(obj, indent=2))
        raise ValueError(f"Invalid concept response: {e}") from e
    if parsed.structure.concepts is None:
        logger.warning(f"No concepts found for {conceptref}")
        return conceptref
    return parsed.structure.concepts.concept.name.value
