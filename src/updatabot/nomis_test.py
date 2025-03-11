# Run with "pytest"
from . import nomis


def test_api_search():
    # Test with search term
    resp = nomis.api.fetch_search(q='population')
    assert len(resp.structure.keyfamilies.keyfamily) == 13

    # Test without search term (all datasets)
    resp = nomis.api.fetch_search()
    assert len(resp.structure.keyfamilies.keyfamily) > 1600


def test_api_codelist():
    resp = nomis.api.fetch_codelist('CL_162_1_AGE')
    assert len(resp.code) == 17


def test_api_dataset_overview():
    resp = nomis.api.fetch_dataset_overview('NM_162_1')
    assert "Job Seekers Allowance claimants" in resp.overview.description


def test_api_concept():
    resp = nomis.api.fetch_concept('SOC2020_FULL')
    assert resp == "Soc2020 full"


def test_lib_codelist():
    ds = nomis.codelist('CL_162_1_AGE')
    assert '[3] "Aged 25-49"' in str(ds)


def test_lib_search():
    ds = nomis.search('population')
    assert len(ds) == 13
