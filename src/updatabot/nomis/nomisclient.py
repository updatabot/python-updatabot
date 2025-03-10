import requests
import json
from ..logger import logger
from .schema.ds_search import DsSearchResponse
from .schema.ds_dataset_structure import DatasetStructureResponse
from .schema.ds_geography import DsGeography

# Base URL for NOMIS API
BASE_URL = "https://www.nomisweb.co.uk/api/v01"


def search_datasets(search_term):
    """Search for datasets containing the specified term."""
    url = f"{BASE_URL}/dataset/def.sdmx.json"
    params = {"search": search_term}

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = DsSearchResponse.model_validate_json(response.text)
    if not data.structure.keyfamilies:
        return []
    return data.structure.keyfamilies.keyfamily


def get_dataset_structure(dataset_id):
    """Get the structure of a specific dataset."""
    url = f"{BASE_URL}/dataset/{dataset_id}/def.sdmx.json"

    response = requests.get(url)
    response.raise_for_status()
    data = DatasetStructureResponse.model_validate_json(response.text)
    return data.structure


def get_geography_codelist(dataset_id, parent=None):
    """Get the geography codelist for a dataset."""
    url = f"{BASE_URL}/dataset/{dataset_id}/geography.def.sdmx.json"
    if parent is not None:
        url = f"{BASE_URL}/dataset/{dataset_id}/geography/{parent}.def.sdmx.json"
    response = requests.get(url)
    response.raise_for_status()
    data = DsGeography.model_validate_json(response.text)
    codelist = data.structure.codelists.codelist
    if len(codelist) != 1:
        logger.error(f"Expected 1 codelist, got {len(codelist)}")
        logger.error(data.model_dump_json())
        raise ValueError(f"Expected 1 codelist, got {len(codelist)}")
    return codelist[0].code


# def get_time_codelist(dataset_id):
#     """Get the available dates for a dataset."""
#     url = f"{BASE_URL}/dataset/{dataset_id}/time.def.sdmx.json"

#     response = requests.get(url)
#     if response.status_code == 200:
#         return response.json()
#     else:
#         print(f"Error: {response.status_code}")
#         return None
