import json
from ...load_url import _ensure_cached
from .base_url import BASE_URL


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
