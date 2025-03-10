from pydantic import BaseModel
from typing import Optional


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
    annotationtext: str | int
    annotationtitle: str


class Attribute(BaseModel):
    assignmentstatus: str
    attachmentlevel: str
    codelist: str | None = None
    conceptref: str


class Dimension(BaseModel):
    codelist: str
    conceptref: str
    isfrequencydimension: str | None = None


class PrimaryMeasure(BaseModel):
    conceptref: str


class TimeDimension(BaseModel):
    codelist: str
    conceptref: str


class Components(BaseModel):
    attribute: list[Attribute]
    dimension: list[Dimension]
    primarymeasure: PrimaryMeasure
    timedimension: TimeDimension


class Description(BaseModel):
    value: str
    lang: str


class KeyFamily(BaseModel):
    agencyid: str
    annotations: dict[str, list[Annotation]]
    id: str
    components: Components
    description: Optional[Description] = None
    name: Description
    uri: str
    version: float


class KeyFamilies(BaseModel):
    keyfamily: list[KeyFamily]


class Structure(BaseModel):
    header: Header
    keyfamilies: Optional[KeyFamilies] = None
    xmlns: str
    common: str
    structure: str
    xsi: str
    schemalocation: str


class DsSearchResponse(BaseModel):
    structure: Structure



## fmt: off
## Example response from NOMIS API
## -------------------------------
## {
##   "structure": {
##     "xmlns": "http://www.SDMX.org/resources/SDMXML/schemas/v2_0/message",
##     "common": "http://www.SDMX.org/resources/SDMXML/schemas/v2_0/common",
##     "structure": "http://www.SDMX.org/resources/SDMXML/schemas/v2_0/structure",
##     "xsi": "http://www.w3.org/2001/XMLSchema-instance",
##     "schemalocation": "http://sdmx.org/docs/2_0/SDMXMessage.xsd",
##     "header": {
##       "id": "none",
##       "prepared": "2025-03-09T08:16:04Z",
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
##           "id": "NM_1_1",
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
##             "primarymeasure": {
##               "conceptref": "OBS_VALUE"
##             },
##             "timedimension": {
##               "codelist": "CL_1_1_TIME",
##               "conceptref": "TIME"
##             }
##           },
##           "description": {
##             "value": "Records the number of people claiming Jobseeker's Allowance (JSA) and National Insurance credits at Jobcentre Plus local offices. This is not an official measure of unemployment, but is the only indicative statistic available for areas smaller than Local Authorities.",
##             "lang": "en"
##           },
##           "name": {
##             "value": "Jobseeker's Allowance with rates and proportions",
##             "lang": "en"
##           },
##           "uri": "Nm-1d1",
##           "version": 1.0
##         },
##         ...
##       ]
##     }
##   }
## }
## fmt: on
