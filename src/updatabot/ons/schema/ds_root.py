from typing import List, Optional, Literal
from pydantic import BaseModel, HttpUrl, EmailStr, Field


class Contact(BaseModel):
    email: EmailStr
    name: str
    telephone: str


class Link(BaseModel):
    href: HttpUrl


class Links(BaseModel):
    editions: Link
    latest_version: Link
    self: Link
    id: Optional[str] = Field(None, alias="latest_version.id")


class RelatedContent(BaseModel):
    description: str
    href: HttpUrl
    title: str


class IsBasedOn(BaseModel):
    type: str = Field(alias="@type")
    id: str = Field(alias="@id")


class DatasetRoot(BaseModel):
    canonical_topic: str
    contacts: List[Contact]
    description: str
    id: str
    is_based_on: IsBasedOn
    keywords: List[str]
    links: Links
    national_statistic: bool
    qmi: dict
    related_content: List[RelatedContent]
    state: Literal["published"]  # Could be expanded if other states exist
    subtopics: List[str]
    survey: str
    themes: List[str]
    title: str
    type: str
    unit_of_measure: str

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