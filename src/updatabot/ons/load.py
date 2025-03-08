import requests
import pandas as pd
from pydantic import TypeAdapter, BaseModel
from typing import TypeVar, Type
from .schema.ds_root import DatasetRoot
from .schema.ds_version import DatasetVersion
from updatabot import logger, load_url

T = TypeVar('T', bound=BaseModel)


def load(id: str) -> pd.DataFrame:
    # --
    # Phase 1: Fetch the dataset root JSON
    url = f"https://api.beta.ons.gov.uk/v1/datasets/{id}"
    logger.info(f"Loading dataset {id} from {url}")
    response = requests.get(url)
    response.raise_for_status()
    # Validate response against schema
    root = TypeAdapter(DatasetRoot).validate_python(response.json())
    logger.info(f"Dataset {id} loaded successfully: {root.title}")

    # Extract link to the dataset version
    if not root.links.latest_version.href:
        raise ValueError(f"Dataset {id} has no latest version listed")
    url = root.links.latest_version.href.unicode_string()

    # --
    # Phase 2: Fetch the dataset version JSON
    logger.info(f"Loading dataset version {id} from {url}")
    response = requests.get(url)
    response.raise_for_status()
    # Validate response against schema
    version = TypeAdapter(DatasetVersion).validate_python(response.json())
    logger.info(
        f"Dataset version {id} loaded successfully: release date={version.release_date}")

    # --
    # Phase 3: Download the data
    if version.downloads.csv:
        return load_url(version.downloads.csv.href.unicode_string())
    if version.downloads.xls:
        return load_url(version.downloads.xls.href.unicode_string())
    raise ValueError(
        f"Dataset version {id} has no CSV or XLS downloads listed")
