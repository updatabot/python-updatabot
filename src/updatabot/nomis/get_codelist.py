from . import fetch
from .schema import SchemaCodelist
from .schema.SchemaCodelist import Codelist, Code
from typing import List
from updatabot import logger


def indent(s: str, prefix: str = "  "):
    return "\n".join(prefix + line for line in s.split("\n"))


class NomisCode:
    def __init__(self, code: Code):
        self.value = code.value
        self.description = code.description.value
        self.parentcode = code.parentcode
        self.children = []

    def __str__(self):
        out = f"[{self.value}] \"{self.description}\""
        for c in self.children:
            out += f"\n{indent(str(c))}"
        return out


class NomisCodelist:
    def __init__(self, codelist: Codelist):
        # "CL_162_1_AGE"
        self.id = codelist.id
        # "Age"
        self.name = codelist.name.value
        # Hierarchy of codes
        tmp = {c.value: NomisCode(c) for c in codelist.code}
        self.codes = []
        for c in tmp.values():
            if c.parentcode is None:
                self.codes.append(c)
            elif c.parentcode in tmp:
                tmp[c.parentcode].children.append(c)
            else:
                logger.warning(
                    'Dropping code %s because parent code %s not found in codelist %s', c.value, c.parentcode, self.id)

    def __str__(self):
        codes = "\n".join([str(c) for c in self.codes])
        return f"""NomisCodelist[id={self.id}] "{self.name}"
{codes}"""


def get_codelist(codelist_id: str):
    if not codelist_id:
        return None
    obj = fetch(f'/dataset/codelist/{codelist_id}.def.sdmx.json')
    parsed = SchemaCodelist(**obj)
    if not parsed.structure.codelists:
        return None
    if len(parsed.structure.codelists.codelist) != 1:
        raise ValueError(
            f"Expected 1 codelist, got {len(parsed.structure.codelists.codelist)}")
    return NomisCodelist(parsed.structure.codelists.codelist[0])
