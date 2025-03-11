from . import fetch
from .schema import ResponseDatasetOverview


def fetch_dataset_overview(id: str) -> ResponseDatasetOverview:
    obj = fetch(f'/dataset/{id}.overview.json')
    parsed = ResponseDatasetOverview(**obj)
    return parsed
