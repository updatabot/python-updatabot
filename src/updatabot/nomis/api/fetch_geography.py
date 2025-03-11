from . import fetch
from .schema import SchemaDataset


def fetch_geography(dataset_id, parent=None):
    """Get the geography codelist for a dataset."""
    # obj = fetch(f'/dataset/{id}/def.sdmx.json')
    # parsed = SchemaDataset(**obj)
    # if len(parsed.structure.keyfamilies.keyfamily) != 1:
    #     raise ValueError(
    #         f"Expected 1 keyfamily, got {len(parsed.structure.keyfamilies.keyfamily)}")
    # return NomisDataset(parsed.structure.keyfamilies.keyfamily[0])
    raise NotImplementedError("Not implemented")
    # url = f"{BASE_URL}/dataset/{dataset_id}/geography.def.sdmx.json"
    # if parent is not None:
    #     url = f"{BASE_URL}/dataset/{dataset_id}/geography/{parent}.def.sdmx.json"
    # response = requests.get(url)
    # response.raise_for_status()
    # data = DsGeography.model_validate_json(response.text)
    # codelist = data.structure.codelists.codelist
    # if len(codelist) != 1:
    #     logger.error(f"Expected 1 codelist, got {len(codelist)}")
    #     logger.error(data.model_dump_json())
    #     raise ValueError(f"Expected 1 codelist, got {len(codelist)}")
    # return codelist[0].code
