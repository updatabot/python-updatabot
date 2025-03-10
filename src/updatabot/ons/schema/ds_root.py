from typing import List, Optional, Literal
from pydantic import BaseModel, HttpUrl, EmailStr, Field


class Contact(BaseModel):
    email: EmailStr
    name: str
    telephone: str


class Link(BaseModel):
    href: Optional[HttpUrl] = None


class Publication(BaseModel):
    href: HttpUrl
    title: str


class Links(BaseModel):
    editions: Link
    latest_version: Link
    self: Link
    taxonomy: Optional[Link] = None
    id: Optional[str] = Field(None, alias="latest_version.id")


class RelatedContent(BaseModel):
    description: str
    href: HttpUrl
    title: str


class IsBasedOn(BaseModel):
    type: str = Field(alias="@type")
    id: str = Field(alias="@id")


class DatasetRoot(BaseModel):
    contacts: List[Contact]
    description: str
    id: str
    keywords: List[str]
    links: Links
    title: str
    state: Literal["published"]

    # Not all fields always appear
    national_statistic: Optional[bool] = False
    license: Optional[str] = None
    next_release: Optional[str] = None
    release_frequency: Optional[str] = None
    publications: Optional[List[Publication]] = None
    related_datasets: Optional[List[Publication]] = None
    qmi: Optional[Link] = None
    unit_of_measure: Optional[str] = None
    canonical_topic: Optional[str] = None
    is_based_on: Optional[IsBasedOn] = None
    subtopics: Optional[List[str]] = None
    themes: Optional[List[str]] = None
    survey: Optional[str] = None
    type: Optional[str] = None

## # fmt: off
## ---------------------------------------------
## https://api.beta.ons.gov.uk/v1/datasets/TS021
## ---------------------------------------------
##
## {
##   "canonical_topic": "7779",
##   "contacts": [
##     {
##       "email": "census.customerservices@ons.gov.uk",
##       "name": "Michael Roskams",
##       "telephone": "+44 1329 444972"
##     }
##   ],
##   "description": "This dataset provides Census 2021 estimates that classify usual residents in England and Wales by ethnic group. The estimates are as at Census Day, 21 March 2021.",
##   "id": "TS021",
##   "is_based_on": {
##     "@id": "UR",
##     "@type": "cantabular_flexible_table"
##   },
##   "keywords": [
##     "ltla",
##     "ethnic_group_tb_20b"
##   ],
##   "links": {
##     "editions": {
##       "href": "https://api.beta.ons.gov.uk/v1/datasets/TS021/editions"
##     },
##     "latest_version": {
##       "href": "https://api.beta.ons.gov.uk/v1/datasets/TS021/editions/2021/versions/3",
##       "id": "3"
##     },
##     "self": {
##       "href": "https://api.beta.ons.gov.uk/v1/datasets/TS021"
##     }
##   },
##   "national_statistic": true,
##   "qmi": {},
##   "related_content": [
##     {
##       "description": "The ethnic groups of usual residents and household ethnic composition in England and Wales, Census 2021 data.",
##       "href": "https://www.ons.gov.uk/peoplepopulationandcommunity/culturalidentity/ethnicity/bulletins/ethnicgroupenglandandwales/census2021",
##       "title": "Ethnic group, England and Wales: Census 2021"
##     },
##     {
##       "description": "Detailed information about variables, definitions and classifications to help when using Census 2021 data.",
##       "href": "https://www.ons.gov.uk/census/census2021dictionary",
##       "title": "Census 2021 dictionary"
##     }
##   ],
##   "state": "published",
##   "subtopics": [
##     "9497"
##   ],
##   "survey": "census",
##   "themes": [
##     "7779",
##     "9497"
##   ],
##   "title": "Ethnic group",
##   "type": "cantabular_flexible_table",
##   "unit_of_measure": "Person"
## }
## # fmt: on