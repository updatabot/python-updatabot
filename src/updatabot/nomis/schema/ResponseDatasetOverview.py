from typing import List, Optional, Literal, Union
from .NomisStructure import StrictObject, Contact

# ---
# NOMIS API: Full dataset list
#  /api/v01/dataset/def.sdmx.json
#
# This API supports ?search params, but we can do that locally.
# Requesting them all (~1600 objects) gives better cache performance.
# ---

## fmt: off
## Example JSON response:
## {
##   "overview": {
##     "analyses": {
##       "analysis": [
##         {
##           "code": 1,
##           "id": "NM_162_1",
##           "name": "output data for a single date or a range of dates"
##         },
##         {
##           "code": 2,
##           "id": "NM_162_2",
##           "name": "average data over a specified period"
##         },
##         {
##           "code": 3,
##           "id": "NM_162_3",
##           "name": "change between two dates"
##         }
##       ]
##     },
##     "analysisname": "output data for a single date or a range of dates",
##     "analysisnumber": 1,
##     "contact": {
##       "email": "support@nomisweb.co.uk",
##       "name": "Nomis",
##       "telephone": "+44(0) 191 3342680",
##       "uri": "https://www.nomisweb.co.uk"
##     },
##     "contenttypes": {
##       "contenttype": {
##         "id": "sources",
##         "value": "cc"
##       }
##     },
##     "coverage": "United Kingdom",
##     "datasetnumber": 162,
##     "description": "The Claimant Count - the stock of Universal Credit and Job Seekers Allowance claimants broken down by sex, age and type of benefit being claimed. Claimant count proportions are available but not when the figures are not broken down by age.",
##     "dimensions": {
##       "dimension": [
##         {
##           "concept": "geography",
##           "internaltype": 22,
##           "make": {
##             "part": {
##               "description": "Codes that make this Geography",
##               "name": "Geography"
##             }
##           },
##           "name": "geography",
##           "size": 0,
##           "types": {
##             "type": [
##               {
##                 "name": "jobcentre plus group as of April 2019",
##                 "value": "TYPE83"
##               },
##               {
##                 "name": "jobcentre plus district as of April 2019",
##                 "value": "TYPE84"
##               },
##               {
##                 "name": "local authorities: district / unitary (prior to April 2015)",
##                 "value": "TYPE464"
##               },
##               {
##                 "name": "english counties",
##                 "value": "TYPE469"
##               },
##               {
##                 "name": "regions",
##                 "value": "TYPE480"
##               },
##               {
##                 "name": "countries",
##                 "value": "TYPE499"
##               }
##             ]
##           }
##         },
##         {
##           "codes": {
##             "code": [
##               {
##                 "level": 1,
##                 "name": "January 1986",
##                 "value": "1986-01"
##               },
##               ...
##             ]
##           },
##           "concept": "time",
##           "defaults": {
##             "code": {
##               "level": 1,
##               "name": "January 2025",
##               "revisions": {
##                 "revision": [
##                   {
##                     "id": "",
##                     "released": "2025-02-18 07:00:00",
##                     "scheduled": "2025-02-18 07:00:00",
##                     "status": "current",
##                     "version": 0
##                   },
##                   {
##                     "id": "",
##                     "released": "",
##                     "scheduled": "2025-03-20 07:00:00",
##                     "status": "pending",
##                     "version": 1
##                   }
##                 ]
##               },
##               "value": "2025-01"
##             }
##           },
##           "internaltype": 23,
##           "name": "date",
##           "size": 469
##         },
##         {
##           "codes": {
##             "code": [
##               {
##                 "level": 0,
##                 "name": "Total",
##                 "value": 0
##               },
##               {
##                 "level": 1,
##                 "name": "Male",
##                 "value": 1
##               },
##               {
##                 "level": 1,
##                 "name": "Female",
##                 "value": 2
##               }
##             ]
##           },
##           "concept": "gender",
##           "defaults": {
##             "code": {
##               "level": 0,
##               "name": "Total",
##               "value": 0
##             }
##           },
##           "internaltype": 25,
##           "name": "Gender",
##           "size": 3
##         },
##         {
##           "codes": {
##             "code": [
##               {
##                 "level": 0,
##                 "name": "All categories: Age 16+",
##                 "ui_suggestcontextmenus": "false",
##                 "ui_suggestexpanddepth": 4,
##                 "ui_suggestreview": "false",
##                 "ui_suggestsearch": "false",
##                 "ui_suggestsorting": "false",
##                 "value": 0
##               },
##               {
##                 "level": 1,
##                 "name": "Age unknown (clerical claims)",
##                 "value": 1
##               },
##             ]
##           },
##           "concept": "age",
##           "defaults": {
##             "code": {
##               "level": 0,
##               "name": "All categories: Age 16+",
##               "ui_suggestcontextmenus": "false",
##               "ui_suggestexpanddepth": 4,
##               "ui_suggestreview": "false",
##               "ui_suggestsearch": "false",
##               "ui_suggestsorting": "false",
##               "value": 0
##             }
##           },
##           "internaltype": 26,
##           "make": {
##             "part": {
##               "description": "Codes that make this definition",
##               "name": "Age"
##             }
##           },
##           "name": "Age",
##           "size": 17
##         },
##         {
##           "codes": {
##             "code": [
##               {
##                 "level": 0,
##                 "name": "Claimant count",
##                 "value": 1
##               },
##               {
##                 "level": 0,
##                 "name": "Claimants as a proportion of residents aged 16-64",
##                 "value": 2
##               },
##               {
##                 "level": 0,
##                 "name": "Claimants as a proportion of economically active residents aged 16+",
##                 "ui_suggeststyle": "line-above-solid",
##                 "value": 3
##               },
##               {
##                 "level": 0,
##                 "name": "Claimants as a proportion of the workforce",
##                 "value": 4
##               }
##             ]
##           },
##           "concept": "measure",
##           "defaults": {
##             "code": {
##               "level": 0,
##               "name": "Claimant count",
##               "value": 1
##             }
##           },
##           "internaltype": 27,
##           "name": "measure",
##           "size": 4
##         },
##         {
##           "codes": {
##             "code": [
##               {
##                 "level": 1,
##                 "name": "value",
##                 "value": 20100
##               },
##               {
##                 "level": 1,
##                 "name": "percent",
##                 "value": 20301
##               }
##             ]
##           },
##           "concept": "measures",
##           "defaults": {
##             "code": {
##               "level": 1,
##               "name": "value",
##               "value": 20100
##             }
##           },
##           "internaltype": 52,
##           "name": "measures",
##           "size": 2
##         }
##       ]
##     },
##     "firstreleased": "2015-06-17 09:30:00",
##     "id": "NM_162_1",
##     "lastrevised": "2025-02-18 07:00:00",
##     "lastupdated": "2025-02-18 07:00:00",
##     "metadata": null,
##     "mnemonic": "ucjsa",
##     "name": "Claimant count by sex and age",
##     "nextupdate": "2025-03-20 07:00:00",
##     "restricted": "false",
##     "status": "Current (being actively updated)",
##     "subdescription": "previously unavailable",
##     "units": {
##       "unit": {
##         "name": "Persons"
##       }
##     }
##   }
## }

## fmt: on

# ------- JSON Response Schema -------


class ContentType(StrictObject):
    """eg.
    { "id": "geoglevel", "value": "la2021" }
    { "id": "sources", "value": "census_2021_st" }
    """
    # Analysis of id:
    # 1:      sorting
    # 8:      1921census
    # 28:     1961census
    # 320:    2001census
    # 748:    censusrelease
    # 1385:   geoglevel
    # 1572:   sources
    id: str
    value: Union[str, int, float]


class ContentTypes(StrictObject):
    contenttype: Union[ContentType, List[ContentType]]


class DimensionGeographyType(StrictObject):
    # Compound literal value
    # ~250 available values seen in analysis. eg:
    # {"name":"local enterprise partnerships (as of April 2021)","value":"TYPE459"}
    # {"name":"local authorities: district / unitary (prior to April 2015)","value":"TYPE464"}
    # {"name":"regions","value":"TYPE480"}
    # {"name":"countries","value":"TYPE499"}
    name: str
    value: str


class DimensionGeographyTypes(StrictObject):
    """
    List of available dimension types, like
    'regions', 'countries', '2021 electoral ward'.
    Only applies to geography dimension.
    """
    # Analysis:
    # --
    # types = null            # 6737 dimensions
    # types = [{...}, ...]    # 1604 dimensions
    # types = {...}           # 1604 dimensions
    type: Union[DimensionGeographyType, List[DimensionGeographyType]]


class Code(StrictObject):
    level: int
    name: Union[str, int]
    value: Union[str, int]
    # [ignore] Metadata general-purpose
    metadata: Optional[dict] = None
    # [ignore] Metadata about code revisions
    revisions: Optional[dict] = None
    # [ignore] UI hints
    displayname: Optional[Union[str, int]] = None
    hierarchytitle: Optional[str] = None
    hierarchydescription: Optional[str] = None
    ui_suggestcontextmenus: Optional[str] = None
    ui_suggestexpanddepth: Optional[int] = None
    ui_suggestreview: Optional[str] = None
    ui_suggestsearch: Optional[str] = None
    ui_suggestsorting: Optional[str] = None
    ui_suggeststyle: Optional[str] = None
    ui_suggestshowheading: Optional[str] = None
    ui_suggestshowtotal: Optional[str] = None
    ui_suggesttoolbar: Optional[str] = None
    ui_suggesttoolbartickallhint: Optional[str] = None
    ui_suggestgroupselection: Optional[str] = None
    ui_suggesttypes: Optional[str] = None


class Codes(StrictObject):
    code: Union[Code, List[Code]]


class Dimension(StrictObject):
    # Dimension name:
    # [...dozens of others...]
    # 90:     Economic Activity
    # 99:     Rural Urban
    # 101:    Tenure
    # 336:    Sex
    # 346:    Age
    # 1568:   geography
    # 1582:   date
    # 1614:   measures
    name: str
    # conceptref, eg "c_age", "geography", "c_disability"...
    concept: str

    # Main list of codes, for every dimension except geography
    codes: Optional[Codes] = None

    # Set on 6600/6900 scanned dimensions.
    # defaults.code is a list on 31 dimensions. Seems weird.
    defaults: Optional[Codes] = None

    # "types" is a list of geographic coverage, eg. 'country', 'electoral ward'...
    # It is set on 1600/6000 dimensions, where concept is a geographical notion. eg.:
    # 4:      concept=second_address
    # 4:      concept=currently_residing_in
    # 10:     concept=address_one_year_ago
    # 11:     concept=place_of_work
    # 16:     concept=usual_residence
    # 1568:   concept=geography
    types: Optional[DimensionGeographyTypes] = None

    # [ignore] Metadata
    metadata: Optional[dict] = None

    # [ignore] A number? Derived from the codelist?
    size: int

    # [ignore] 30-50 disinct type codes, unexplained
    internaltype: int

    # [ignore] "make" is a redundant expansion of "name".
    # - make.part is a list on 3 dimensions out of 4,900+ scanned
    # - make.part.name matches Dimension.name on 4868/4900 scanned
    # - make.part.description takes only a dozen values, all boring.
    # Ther are only a doz
    # { /* eg... */
    #     "name": "Age",
    #     "make": {
    #       "part": {
    #         "description": "Codes that make this definition",
    #         "name": "Age"
    #       }
    #     },
    make: Optional[dict] = None


class Dimensions(StrictObject):
    dimension: List[Dimension]


class Unit(StrictObject):
    """Name of the base statistical unit of observations."""
    # Useful metadata!
    # Frequency analysis:
    # (couple dozen single values)...
    # 8:      Communal establishments
    # 11:     Dwellings
    # 14:     JCP Vacancies
    # 16:     Families
    # 21:     Household spaces
    # 38:     Household reference persons
    # 201:    Households
    # 1294:   Persons
    name: str


class Units(StrictObject):
    # Nearly always a single value.
    # Exceptions found: (unit.name list...)
    # --
    # NM_30_1:         ["GB pounds", "GB pounds per week", "Hours per week"]
    # NM_99_1:         ["GB pounds", "GB pounds per week", "Hours per week"]
    # NM_501_1:        ["Communal establishments", "Persons"]
    # NM_518_1:        ["Families", "Persons"]
    # NM_618_1:        ["Household spaces", "Dwellings"]
    # NM_622_1:        ["Communal establishments", "Persons"]
    # NM_1238_1:       ["Establishments", "Rooms", "Persons"]
    # NM_1254_1:       ["Household spaces", "Dwellings", "Rooms"]
    # NM_1256_1:       ["Households", "Persons", "Rooms"]
    # NM_1420_1:       ["Statute Acres", "Persons", "Families", "Dwellings", "Rooms"]
    # NM_1423_1:       ["Institutions", "Persons"]
    # NM_1506_1:       ["Household spaces", "Dwellings"]
    # NM_1509_1:       ["Communal establishments", "Persons"]
    # NM_1530_1:       ["Communal establishments", "Persons"]
    # NM_1542_1:       ["Families", "Persons"]
    # NM_1625_1:       ["Persons", "Households"]
    unit: Union[Unit, List[Unit]]


class Analysis(StrictObject):
    code: int
    id: str
    name: str


class Analyses(StrictObject):
    analysis: Union[Analysis, List[Analysis]]


class OverviewMetadataEntry(StrictObject):
    """Mostly ignorable. 'About this dataset' appears useful."""
    # Some kind of free-text field. Analysis:
    #   [dozens of one-shot values]
    #   2:      Economic activity
    #   2:      Hours worked
    #   2:      Industry
    #   2:      Occupation
    #   2:      NS-SeC
    #   321:    About this dataset
    #   323:    Protecting personal data
    #   1089:   Statistical Disclosure Control
    metadatatitle: Optional[str] = None
    text: Optional[str] = None


class OverviewMetadata(StrictObject):
    metaentry: Union[OverviewMetadataEntry, List[OverviewMetadataEntry]]


class Overview(StrictObject):
    # Top metadata
    id: str
    # Main title
    name: str
    # Set on 114/1614 datasets
    description: Optional[str] = ''
    # Set on nearly all datasets, eg.:
    # "All Household Reference Persons (HRPs) aged 16 to 74"
    # "All Household Reference Persons aged 16 to 64"
    # "All dependent children aged 3 to 4 in one family households in Wales"
    subdescription: Optional[str] = ''
    status: Literal[
        # 447 datasets found:
        'Historical (not actively being updated)',
        # 1127 datasets found:
        'Current (being actively updated)'
    ]

    # dates
    firstreleased: Optional[str] = None
    lastrevised: Optional[str] = None
    lastupdated: Optional[str] = None
    nextupdate: Optional[str] = None

    # Comma-separated list of keywords. eg. 'Claimants,JSA,Rates'
    keywords: Optional[str] = None

    # List of other analyses of this dataset
    analyses: Analyses

    # My entry within the analysis list
    analysisname: Optional[str] = None
    analysisnumber: int

    # [content] The core juicy part!
    dimensions: Dimensions

    # [content] The base unit of observation.
    units: Units

    # [ignore] Metadata about geographic coverage. Analysis:
    # 1:      Great Britain and overseas
    # 1:      England
    # 2:      United Kingdom, overseas or unknown
    # 3:      United Kingdom and offshore/abroad
    # 5:      Northern Ireland
    # 8:      United Kingdom and overseas
    # 14:     Great Britain and abroad
    # 71:     Great Britain
    # 95:     Wales
    # 146:    United Kingdom
    # 1268:   England and Wales
    coverage: str

    # [ignore] Always this compound literal:
    # { "digest": null, "url": null, "name": null }
    provider: Optional[dict] = None
    # [ignore] Mostly useless metadata, except 'About this dataset' on ~300 datasets
    metadata: Optional[OverviewMetadata] = None
    # [ignore] Some kind of loose relational mapping
    contenttypes: Optional[ContentTypes] = None
    # [ignore] true on 8 datasets
    restricted: Literal['true', 'false']
    # [ignore] Derived from id
    datasetnumber: int
    # [ignore] Set on 2 datasets, no useful data
    extensions: Optional[dict] = None
    # [ignore] For the web UI
    contact: Contact
    # [ignore] Set on all datasets, not used via API
    mnemonic: str


class ResponseDatasetOverview(StrictObject):
    overview: Overview
