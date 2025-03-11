from . import api
from .schema.ResponseCodelist import Codelist, Code
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


# TODO not sure if i'm using this
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


def codelist(id: str) -> NomisCodelist:
    return NomisCodelist(api.fetch_codelist(id))
