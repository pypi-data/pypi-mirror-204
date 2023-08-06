"""Tests for tables module methods"""
import requests
import json
import unittest

from pycax import tables
from pycax import hli
  
def test_tables_tableid():
    """
    tables.tableid - test that only one value returned
    """
    for val in hli.HLI_SHORT:
        res = tables.tableid(hli.return_tablename(val, "base"))
        assert "ndarray" == res.__class__.__name__
        assert 1 == len(res)
        assert str == res[0].__class__

class MyTestCase(unittest.TestCase):
    def test_tables_tableid_exception(self):
        self.assertRaises(ValueError, tables.tableid, "badname")

    def test_tables_get_exception(self):
        self.assertRaises(TypeError, tables.get, "NOSA", **{'fargs': 'a'})


def test_tables_get():
    """
    tables.get - basic test for data, check type, size and other methods
    """
    query = tables.get("NOSA", qargs={'limit': 2})
    assert "TablesResponse" == query.__class__.__name__
    assert not query.data
    assert str == query.api_url.__class__
    assert "NOSA" == query.tablename
    assert str == query.tableid.__class__
    query.execute()
    assert dict == query.data.__class__
    assert 6 == len(query.data)
    assert dict == query.data["records"][0].__class__
    assert int == query.data["records"][0]["popid"].__class__
    assert 2 == len(query.data["records"])
    assert query.to_pandas().__class__.__name__ == "DataFrame"

def test_dict_to_json():
    """
    tables.dict_to_json - basic test for structure
    """
    res = tables.dict_to_json({'popid': '7'})
    assert "str" == res.__class__.__name__
    dictlist = json.loads(res)
    assert "list" == dictlist.__class__.__name__
    assert "dict" == dictlist[0].__class__.__name__
    assert 3 == len(dictlist[0])
    dictkeys = [key for key in dictlist[0]]
    dictvals = [dictlist[0][key] for key in dictlist[0]]
    assert dictkeys == ['field', 'value', 'type']
    assert dictvals == ['popid', '7', 'string']
    res = tables.dict_to_json({'popid': [7, 8]})
    dictlist = json.loads(res)
    dictvals = [dictlist[0][key] for key in dictlist[0]]
    assert "list" == dictvals[2]
    res = tables.dict_to_json({'popid': [7, 8], 'species': 'Chinook, salmon'})
    dictlist = json.loads(res)
    assert 2 == len(dictlist)

def test_tables_getdf():
    """
    tables.getdf - test that data frame returned
    """
    df = tables.getdf("NOSA", qargs={'limit': 1})
    assert "DataFrame" == df.__class__.__name__
    assert 1 == df.shape[0]
    id = df['popid'][0]
    df = hli.getdf("NOSA", qargs={'limit': 1}, fargs={'popid':id})
    assert 1 == df.shape[0]
    assert id == df['popid'][0]
    df = hli.getdf("NOSA", tabletype = "base", qargs={'limit': 1})
    assert "DataFrame" == df.__class__.__name__
    assert 1 == df.shape[0]
    id = df['popid'][0]
    df = hli.getdf("NOSA", qargs={'limit': 1}, fargs={'popid':id})
    assert 1 == df.shape[0]
    assert id == df['popid'][0]
