from . import fetch
from .schema import SchemaDataset
from .NomisDataset import NomisDataset
from urllib.parse import urlencode
from typing import List


def get_datasets(search=None) -> List[NomisDataset]:
    if search:
        obj = fetch(
            f'/dataset/def.sdmx.json?{urlencode({"search": search})}')
    else:
        obj = fetch('/dataset/def.sdmx.json')

    parsed = SchemaDataset(**obj)
    return [NomisDataset(k) for k in parsed.structure.keyfamilies.keyfamily]
