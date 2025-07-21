from ..load_url import _ensure_cached
from . import schema
from urllib.parse import urlencode
from typing import List
from updatabot import logger
import json
from pydantic import ValidationError
from .schema.ResponseCodelist import Codelist
# from .schema.ResponseDataset import KeyFamily

BASE_URL = "https://www.nomisweb.co.uk/api/v01"


def fetch(url: str) -> dict:
    """
    Get a JSON object from the NOMIS API.
    The JSON object will be cached locally after the first request.

    Args:
        url: Relative URL, eg. "/dataset/def.sdmx.json"

    Returns:
        The JSON object.
    """
    local_path = _ensure_cached(BASE_URL + url)
    with open(local_path, 'r') as f:
        return json.load(f)


def fetch_search(q=None) -> schema.ResponseDataset:
    """Provide q=... to filter results. Otherwise all search hits are returned."""
    if q:
        obj = fetch(
            f'/dataset/def.sdmx.json?{urlencode({"search": q})}')
    else:
        obj = fetch('/dataset/def.sdmx.json')

    parsed = schema.ResponseDataset(**obj)
    return parsed


def fetch_dataset(id: str) -> schema.ResponseDataset:
    """A single-entry version of fetch_search, with the keyfamily extracted."""
    obj = fetch(
        f'/dataset/{id}.def.sdmx.json'
    )

    parsed = schema.ResponseDataset(**obj)
    keyfamilies = parsed.structure.keyfamilies
    if not keyfamilies:
        raise ValueError(f"NOMIS dataset not found: {id}")
    if len(keyfamilies.keyfamily) != 1:
        raise ValueError(
            f"Expected 1 keyfamily, got {len(keyfamilies.keyfamily)}")
    return keyfamilies.keyfamily[0]


def fetch_dataset_overview(id: str) -> schema.ResponseDatasetOverview:
    """
    Main document for viewing a NOMIS dataset.
    Contains all the useful metadata, except the massive geography breakdown.
    """
    obj = fetch(f'/dataset/{id}.overview.json')
    parsed = schema.ResponseDatasetOverview(**obj)
    return parsed


def fetch_codelist(codelist_id: str) -> Codelist:
    if not codelist_id:
        return None
    obj = fetch(f'/dataset/codelist/{codelist_id}.def.sdmx.json')
    parsed = schema.ResponseCodelist(**obj)
    if not parsed.structure.codelists:
        return None
    if len(parsed.structure.codelists.codelist) != 1:
        raise ValueError(
            f"Expected 1 codelist, got {len(parsed.structure.codelists.codelist)}")
    return parsed.structure.codelists.codelist[0]


def fetch_geography(dataset_id, parent=None):
    """Get the geography codelist for a dataset."""
    raise NotImplementedError("Not implemented")


def fetch_concept(conceptref: str) -> str:
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
        parsed = schema.ResponseConcept(**obj)
    except ValidationError as e:
        logger.error(json.dumps(obj, indent=2))
        raise ValueError(f"Invalid concept response: {e}") from e
    if parsed.structure.concepts is None:
        logger.warning(f"No concepts found for {conceptref}")
        return conceptref
    return parsed.structure.concepts.concept.name.value
