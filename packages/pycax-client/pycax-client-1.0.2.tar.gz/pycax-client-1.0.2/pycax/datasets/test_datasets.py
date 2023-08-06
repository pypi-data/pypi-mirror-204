"""Tests for datasets module"""
import requests

from pycax import datasets

from pycax.caxutils import cax_api_key


def test_datasets_get_data():
    "datasets.get - test data"
    query = datasets.get()
    assert "DatasetsResponse" == query.__class__.__name__
    assert not query.data
    query.execute()
    assert query.data.__class__.__name__ == "dict"
    assert 1 == len(query.data)
    assert dict == query.data["tables"][0].__class__
    assert query.to_pandas().__class__.__name__ == "DataFrame"

def test_datasets_get_url():
    "datasets.get - test api_url"
    query = datasets.get()
    assert requests.get(query.api_url, params = {'XApiKey': cax_api_key}).status_code == 200

def test_datasets_getdf_result():
    "datasets.getdf - test result"
    res = datasets.getdf()
    assert res.__class__.__name__ == "DataFrame"

