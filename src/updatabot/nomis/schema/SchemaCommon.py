from pydantic import BaseModel, ConfigDict
from typing import Optional


class StrictObject(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Contact(StrictObject):
    email: str
    name: str
    telephone: Optional[str] = None
    uri: Optional[str] = None


class Sender(StrictObject):
    contact: Contact
    id: str


class Header(StrictObject):
    id: str
    prepared: str
    sender: Sender
    test: str


class NomisStructure(StrictObject):
    """
    Abstract base class. Every NOMIS response is like:

    {
      "structure": {
        "header": { ... },
        "xmlns": "...",
        "common": "...",
        "structure": "...",
        "xsi": "...",
        "schemalocation": "...",

        ...and the actual data we want.
      },
    }
    """
    header: Header
    xmlns: str
    common: str
    structure: str
    xsi: str
    schemalocation: str
