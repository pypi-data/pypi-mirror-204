"""Tests for hli module"""
import requests

from pycax import hli

def test_hli_return_tablename():
    """
    hli.return_tablename - test that string returned
    """
    for val in hli.HLI_SHORT:
        for tabtype in ['base', 'xport']:
            res = hli.return_tablename(val, tabtype)
            assert "str" == res.__class__.__name__

def test_hli_getdf():
    """
    hli.getdf - test that data frame returned
    """
    df = hli.getdf("NOSA", qargs={'limit': 1})
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

def test_hli_get():
    """
    hli.get - test that get function returns proper types
    """
    query = hli.get("NOSA", qargs={'limit': 2})
    assert "TablesResponse" == query.__class__.__name__
    assert not query.data
    query.execute()
    assert "dict" == query.data.__class__.__name__
    assert 6 == len(query.data)
    assert dict == query.data["records"][0].__class__
    assert int == query.data["records"][0]["popid"].__class__
    assert str == query.api_url.__class__
    assert 2 == len(query.data["records"])

import unittest

class MyTestCase(unittest.TestCase):
    def test_hli_return_tablename_exception(self):
        self.assertRaises(ValueError, hli.return_tablename, "badname", "xport")

    def test_hli_return_tablename_tabletype_exception(self):
        self.assertRaises(ValueError, hli.return_tablename, "NOSA", "badname")

    def test_hli_get_exception(self):
        self.assertRaises(TypeError, hli.get, "NOSA", **{'fargs': 'a'})

