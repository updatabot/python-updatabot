from typing import Dict, List, Literal, Optional
from pydantic import BaseModel, HttpUrl, Field
from .ds_root import IsBasedOn


class Dimension(BaseModel):
    description: str
    href: HttpUrl
    id: str
    is_area_type: bool
    label: str
    links: Dict
    name: str
    number_of_options: int
    variable: str
    quality_statement_url: Optional[HttpUrl] = None


class Download(BaseModel):
    href: HttpUrl
    size: str
    public: Optional[HttpUrl] = None


class Downloads(BaseModel):
    csv: Download
    csvw: Download
    txt: Download
    xls: Download


class VersionLinks(BaseModel):
    dataset: Dict[str, str]
    dimensions: Dict
    edition: Dict[str, str]
    self: Dict[str, HttpUrl]


class DatasetVersion(BaseModel):
    alerts: List
    collection_id: Optional[str] = None
    dimensions: List[Dimension]
    downloads: Downloads
    edition: str
    id: str
    is_based_on: IsBasedOn  # Reusing from ds_root
    latest_changes: List
    links: VersionLinks
    lowest_geography: str
    release_date: str
    state: Literal["published"]
    type: str
    usage_notes: List
    version: int



## fmt: off
## {
##   "alerts": [],
##   "collection_id": "datacombiningmultiplevariablesenglandandwalescensus2021-63848095db68d1e2ef6b2efee725efbb0f04f723bd043de9f8b6f53e85476aef",
##   "dimensions": [
##     {
##       "description": "Lower tier local authorities provide a range of local services. There are 309 lower tier local authorities in England made up of 181 non-metropolitan districts, 59 unitary authorities, 36 metropolitan districts and 33 London boroughs (including City of London). In Wales there are 22 local authorities made up of 22 unitary authorities.",
##       "href": "https://api.beta.ons.gov.uk/v1/code-lists/ltla",
##       "id": "ltla",
##       "is_area_type": true,
##       "label": "Lower tier local authorities",
##       "links": {
##         "code_list": {},
##         "options": {},
##         "version": {}
##       },
##       "name": "ltla",
##       "number_of_options": 331,
##       "variable": "ltla"
##     },
##     {
##       "description": "The ethnic group that the person completing the census feels they belong to. This could be based on their culture, family background, identity or physical appearance.\n\nRespondents could choose one out of 19 tick-box response categories, including write-in response options.",
##       "href": "https://api.beta.ons.gov.uk/v1/code-lists/ethnic_group_tb_20b",
##       "id": "ethnic_group_tb_20b",
##       "is_area_type": false,
##       "label": "Ethnic group (20 categories)",
##       "links": {
##         "code_list": {},
##         "options": {},
##         "version": {}
##       },
##       "name": "ethnic_group_tb_20b",
##       "number_of_options": 20,
##       "quality_statement_url": "https://www.ons.gov.uk/peoplepopulationandcommunity/culturalidentity/ethnicity/methodologies/ethnicgroupnationalidentitylanguageandreligionqualityinformationforcensus2021",
##       "variable": "ethnic_group_tb_20b"
##     }
##   ],
##   "downloads": {
##     "csv": {
##       "href": "https://download.beta.ons.gov.uk/downloads/datasets/TS021/editions/2021/versions/3.csv",
##       "size": "490650"
##     },
##     "csvw": {
##       "href": "https://download.beta.ons.gov.uk/downloads/datasets/TS021/editions/2021/versions/3.csv-metadata.json",
##       "size": "2644"
##     },
##     "txt": {
##       "href": "https://download.beta.ons.gov.uk/downloads/datasets/TS021/editions/2021/versions/3.txt",
##       "public": "https://static.ons.gov.uk/datasets/TS021-2021-3.txt",
##       "size": "3838"
##     },
##     "xls": {
##       "href": "https://download.beta.ons.gov.uk/downloads/datasets/TS021/editions/2021/versions/3.xlsx",
##       "size": "142797"
##     }
##   },
##   "edition": "2021",
##   "id": "3f37f265-f175-4630-8323-6caf7b4934e8",
##   "is_based_on": {
##     "@id": "UR",
##     "@type": "cantabular_flexible_table"
##   },
##   "latest_changes": [],
##   "links": {
##     "dataset": {
##       "href": "https://api.beta.ons.gov.uk/v1/datasets/TS021",
##       "id": "TS021"
##     },
##     "dimensions": {},
##     "edition": {
##       "href": "https://api.beta.ons.gov.uk/v1/datasets/TS021/editions/2021",
##       "id": "2021"
##     },
##     "self": {
##       "href": "https://api.beta.ons.gov.uk/v1/datasets/TS021/editions/2021/versions/3"
##     }
##   },
##   "lowest_geography": "oa",
##   "release_date": "2023-03-28T00:00:00.000Z",
##   "state": "published",
##   "type": "cantabular_flexible_table",
##   "usage_notes": [],
##   "version": 3
## }