from . import api
from .schema.ResponseDatasetOverview import Overview


class NomisQuery:
    """Stateful query object"""

    def __init__(self, overview: Overview):
        self.__overview__ = overview
        self.id = overview.id


def query(id: str) -> NomisQuery:
    """
    Open a dataset for querying.
    """
    resp = api.fetch_dataset_overview(id)
    return NomisQuery(resp.overview)
