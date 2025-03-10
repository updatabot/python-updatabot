from pydantic import BaseModel, Field
from typing import List, Optional


class Annotation(BaseModel):
    annotationtext: str | int
    annotationtitle: str


class Annotations(BaseModel):
    annotation: List[Annotation]


class Description(BaseModel):
    value: str
    lang: str


class Code(BaseModel):
    annotations: Annotations
    description: Description
    value: str | int
    parentcode: Optional[str | int] = None


class Name(BaseModel):
    value: str
    lang: str


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


class Codelist(BaseModel):
    agencyid: str
    id: str
    code: List[Code]
    name: Name
    uri: str


class Codelists(BaseModel):
    codelist: List[Codelist]


class Structure(BaseModel):
    codelists: Codelists
    header: Header
    xmlns: str = Field(alias="xmlns")
    common: str
    structure: str
    xsi: str
    schemalocation: str


class DsGeography(BaseModel):
    structure: Structure


## fmt: off
## {
##   "structure": {
##     "codelists": {
##       "codelist": [
##         {
##           "agencyid": "NOMIS",
##           "id": "CL_162_1_GEOGRAPHY",
##           "code": [
##             {
##               "annotations": {
##                 "annotation": [
##                   {
##                     "annotationtext": "countries",
##                     "annotationtitle": "TypeName"
##                   },
##                   {
##                     "annotationtext": 499,
##                     "annotationtitle": "TypeCode"
##                   },
##                   {
##                     "annotationtext": "K02000001",
##                     "annotationtitle": "GeogCode"
##                   }
##                 ]
##               },
##               "description": {
##                 "value": "United Kingdom",
##                 "lang": "en"
##               },
##               "value": 2092957697
##             },
##             {
##               "annotations": {
##                 "annotation": [
##                   {
##                     "annotationtext": "countries",
##                     "annotationtitle": "TypeName"
##                   },
##                   {
##                     "annotationtext": 499,
##                     "annotationtitle": "TypeCode"
##                   },
##                   {
##                     "annotationtext": "K03000001",
##                     "annotationtitle": "GeogCode"
##                   }
##                 ]
##               },
##               "description": {
##                 "value": "Great Britain",
##                 "lang": "en"
##               },
##               "value": 2092957698
##             },
##             {
##               "annotations": {
##                 "annotation": [
##                   {
##                     "annotationtext": "countries",
##                     "annotationtitle": "TypeName"
##                   },
##                   {
##                     "annotationtext": 499,
##                     "annotationtitle": "TypeCode"
##                   },
##                   {
##                     "annotationtext": "E92000001",
##                     "annotationtitle": "GeogCode"
##                   }
##                 ]
##               },
##               "description": {
##                 "value": "England",
##                 "lang": "en"
##               },
##               "value": 2092957699
##             },
##             {
##               "annotations": {
##                 "annotation": [
##                   {
##                     "annotationtext": "countries",
##                     "annotationtitle": "TypeName"
##                   },
##                   {
##                     "annotationtext": 499,
##                     "annotationtitle": "TypeCode"
##                   },
##                   {
##                     "annotationtext": "W92000004",
##                     "annotationtitle": "GeogCode"
##                   }
##                 ]
##               },
##               "parentcode": 2092957700,
##               "description": {
##                 "value": "Wales",
##                 "lang": "en"
##               },
##               "value": 2092957700
##             },
##             {
##               "annotations": {
##                 "annotation": [
##                   {
##                     "annotationtext": "countries",
##                     "annotationtitle": "TypeName"
##                   },
##                   {
##                     "annotationtext": 499,
##                     "annotationtitle": "TypeCode"
##                   },
##                   {
##                     "annotationtext": "S92000003",
##                     "annotationtitle": "GeogCode"
##                   }
##                 ]
##               },
##               "parentcode": 2092957701,
##               "description": {
##                 "value": "Scotland",
##                 "lang": "en"
##               },
##               "value": 2092957701
##             },
##             {
##               "annotations": {
##                 "annotation": [
##                   {
##                     "annotationtext": "countries",
##                     "annotationtitle": "TypeName"
##                   },
##                   {
##                     "annotationtext": 499,
##                     "annotationtitle": "TypeCode"
##                   },
##                   {
##                     "annotationtext": "N92000002",
##                     "annotationtitle": "GeogCode"
##                   }
##                 ]
##               },
##               "parentcode": 2092957702,
##               "description": {
##                 "value": "Northern Ireland",
##                 "lang": "en"
##               },
##               "value": 2092957702
##             },
##             {
##               "annotations": {
##                 "annotation": [
##                   {
##                     "annotationtext": "countries",
##                     "annotationtitle": "TypeName"
##                   },
##                   {
##                     "annotationtext": 499,
##                     "annotationtitle": "TypeCode"
##                   },
##                   {
##                     "annotationtext": "K04000001",
##                     "annotationtitle": "GeogCode"
##                   }
##                 ]
##               },
##               "description": {
##                 "value": "England and Wales",
##                 "lang": "en"
##               },
##               "value": 2092957703
##             }
##           ],
##           "name": {
##             "value": "geography",
##             "lang": "en"
##           },
##           "uri": ""
##         }
##       ]
##     },
##     "header": {
##       "id": "NM_162_1",
##       "prepared": "2025-03-09T09:12:57Z",
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
##     "xmlns": "http://www.SDMX.org/resources/SDMXML/schemas/v2_0/message",
##     "common": "http://www.SDMX.org/resources/SDMXML/schemas/v2_0/common",
##     "structure": "http://www.SDMX.org/resources/SDMXML/schemas/v2_0/structure",
##     "xsi": "http://www.w3.org/2001/XMLSchema-instance",
##     "schemalocation": "http://sdmx.org/docs/2_0/SDMXMessage.xsd"
##   }
## }