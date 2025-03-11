from . import fetch
from .schema import ResponseDataset
from urllib.parse import urlencode
from typing import List


def fetch_search(q=None) -> ResponseDataset:
    """Provide q=... to filter results. Otherwise all search hits are returned."""
    if q:
        obj = fetch(
            f'/dataset/def.sdmx.json?{urlencode({"search": q})}')
    else:
        obj = fetch('/dataset/def.sdmx.json')

    parsed = ResponseDataset(**obj)
    return parsed
