import json
from pydantic import BaseModel, ConfigDict
from typing import Optional
from ...load_url import _ensure_cached
BASE_URL = "https://www.nomisweb.co.uk/api/v01"


class StrictObject(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Contact(StrictObject):
    email: str
    name: str
    telephone: str
    uri: Optional[str] = ''


class Sender(StrictObject):
    contact: Contact
    id: str


class Header(StrictObject):
    id: str
    prepared: str
    sender: Sender
    test: str


class NomisStructure(StrictObject):
    """
    Abstract base class. Every NOMIS response is like:

    {
      "structure": {
        "header": { ... },
        "xmlns": "...",
        "common": "...",
        "structure": "...",
        "xsi": "...",
        "schemalocation": "...",

        ...and the actual data we want.
      },
    }
    """
    header: Header
    xmlns: str
    common: str
    structure: str
    xsi: str
    schemalocation: str


def get_json(url: str) -> dict:
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
