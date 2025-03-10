from pydantic import BaseModel
from typing import Optional, List


class Contact(BaseModel):
    email: str
    name: str
    telephone: str
    uri: str


class Sender(BaseModel):
    contact: Contact
    id: str


class Header(BaseModel):
    id: str
    prepared: str
    sender: Sender
    test: str


class Annotation(BaseModel):
    annotationtext: str
    annotationtitle: str


class Annotations(BaseModel):
    annotation: List[Annotation]


class Attribute(BaseModel):
    assignmentstatus: str
    attachmentlevel: str
    codelist: Optional[str] = None
    conceptref: str


class Dimension(BaseModel):
    codelist: str
    conceptref: str
    isfrequencydimension: Optional[str] = None


class PrimaryMeasure(BaseModel):
    conceptref: str


class TimeDimension(BaseModel):
    codelist: str
    conceptref: str


class Components(BaseModel):
    attribute: List[Attribute]
    dimension: List[Dimension]
    primarymeasure: PrimaryMeasure
    timedimension: TimeDimension


class Description(BaseModel):
    value: str
    lang: str


class Name(BaseModel):
    value: str
    lang: str


class KeyFamily(BaseModel):
    agencyid: str
    annotations: Annotations
    id: str
    components: Components
    description: Description
    name: Name
    uri: str
    version: float


class KeyFamilies(BaseModel):
    keyfamily: List[KeyFamily]


class Structure(BaseModel):
    header: Header
    keyfamilies: KeyFamilies
    xmlns: str
    common: str
    structure: str
    xsi: str
    schemalocation: str


class DatasetStructureResponse(BaseModel):
    structure: Structure


## fmt: off
## --------------------------
## /dataset/:id/def.sdmx.json
## --------------------------
## {
##   "structure": {
##     "xmlns": "http://www.SDMX.org/resources/SDMXML/schemas/v2_0/message",
##     "common": "http://www.SDMX.org/resources/SDMXML/schemas/v2_0/common",
##     "structure": "http://www.SDMX.org/resources/SDMXML/schemas/v2_0/structure",
##     "xsi": "http://www.w3.org/2001/XMLSchema-instance",
##     "schemalocation": "http://sdmx.org/docs/2_0/SDMXMessage.xsd",
##     "header": {
##       "id": "NM_162_1",
##       "prepared": "2025-03-09T09:01:10Z",
##       "sender": {
##         "contact": {
##           "email": "support@nomisweb.co.uk",
##           "name": "Nomis",
##           "telephone": "+44(0) 191 3342680",
##           "uri": "https://www.nomisweb.co.uk"
##         },
##         "id": "NOMIS"
##       },
##       "test": "false"
##     },
##     "keyfamilies": {
##       "keyfamily": [
##         {
##           "agencyid": "NOMIS",
##           "annotations": {
##             "annotation": [
##               {
##                 "annotationtext": "Current (being actively updated)",
##                 "annotationtitle": "Status"
##               },
##               ...
##             ]
##           },
##           "id": "NM_162_1",
##           "components": {
##             "attribute": [
##               {
##                 "assignmentstatus": "Mandatory",
##                 "attachmentlevel": "Observation",
##                 "codelist": "CL_OBS_STATUS",
##                 "conceptref": "OBS_STATUS"
##               },
##               ...
##             ],
##             "dimension": [
##               {
##                 "codelist": "CL_162_1_GEOGRAPHY",
##                 "conceptref": "GEOGRAPHY"
##               },
##               ...
##             ],
##             "primarymeasure": {
##               "conceptref": "OBS_VALUE"
##             },
##             "timedimension": {
##               "codelist": "CL_162_1_TIME",
##               "conceptref": "TIME"
##             }
##           },
##           "description": {
##             "value": "The Claimant Count - the stock of Universal Credit and Job Seekers Allowance claimants broken down by sex, age and type of benefit being claimed. Claimant count proportions are available but not when the figures are not broken down by age.",
##             "lang": "en"
##           },
##           "name": {
##             "value": "Claimant count by sex and age",
##             "lang": "en"
##           },
##           "uri": "Nm-162d1",
##           "version": 1.0
##         }
##       ]
##     }
##   }
## }