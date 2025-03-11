from . import fetch
from .schema import SchemaDatasetOverview


def get_dataset_overview(id: str) -> SchemaDatasetOverview:
    obj = fetch(f'/dataset/{id}.overview.json')
    parsed = SchemaDatasetOverview(**obj)
    return parsed
