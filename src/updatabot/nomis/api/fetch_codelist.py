from . import fetch
from .schema.ResponseCodelist import ResponseCodelist, Codelist


def fetch_codelist(codelist_id: str) -> Codelist:
    if not codelist_id:
        return None
    obj = fetch(f'/dataset/codelist/{codelist_id}.def.sdmx.json')
    parsed = ResponseCodelist(**obj)
    if not parsed.structure.codelists:
        return None
    if len(parsed.structure.codelists.codelist) != 1:
        raise ValueError(
            f"Expected 1 codelist, got {len(parsed.structure.codelists.codelist)}")
    return parsed.structure.codelists.codelist[0]
