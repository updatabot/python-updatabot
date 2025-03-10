from . import fetch
from .schema import SchemaDataset
from .NomisDataset import NomisDataset


def get_dataset(id: str) -> NomisDataset:
    obj = fetch(f'/dataset/{id}/def.sdmx.json')
    parsed = SchemaDataset(**obj)
    if len(parsed.structure.keyfamilies.keyfamily) != 1:
        raise ValueError(
            f"Expected 1 keyfamily, got {len(parsed.structure.keyfamilies.keyfamily)}")
    return NomisDataset(parsed.structure.keyfamilies.keyfamily[0])
