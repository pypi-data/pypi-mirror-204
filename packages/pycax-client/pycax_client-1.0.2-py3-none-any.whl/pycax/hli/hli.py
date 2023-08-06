"""
Query for a HLI base or XPort table

/ca?table_id=<id> API endpoint with id equal to one of the HLI or HLI_XPort table ids
"""
import pandas as pd

from pycax.caxutils import get_data

from pycax import tables

# Set up the variables

HLI_SHORT = {"NOSA", "SAR", "PNI", "JuvOut", "PreSmolt", "RperS"}
HLI_TABLENAMES = { 
    'base': {
        'NOSA': 'NOSA',  'SAR': 'SAR',  'PNI': 'PNI', 
        'JuvOut': 'JuvenileOutmigrants',  'PreSmolt': 'PresmoltAbundance', 
        'RperS': 'RperS'
        },
    'xport': {}
    }
for key in HLI_TABLENAMES['base']:
    HLI_TABLENAMES['xport'][key] = 'XPortCA_'+HLI_TABLENAMES['base'][key]+'_01'

import json
import pkgutil

#data = pkgutil.get_data(__name__, "data/xport_colnames_json.txt")
data = get_data("xport_colnames_json.txt")
HLI_XPORT_COLNAMES = json.loads(data)

 
def return_tablename(hli, tabletype):
    """
    Retrieve a table name for a hli short code for base or xport table type

    :param hli: [String] A HLI short code: NOSA, SAR, PNI, JuvOut, PreSmolt, RperS
    :param tabletype: [String] "base" or "xport"
    :return: A table name as a string

    Usage::

        from pycax import hli
        hli.tablename('NOSA', 'base')
    """
    valid = HLI_SHORT
    if hli not in valid:
        raise ValueError("hli must be one of %r." % valid)
    valid = ["base", "xport"]
    if tabletype not in valid:
        raise ValueError("tabletype must be one of %r." % valid)
    
    return HLI_TABLENAMES[tabletype][hli]

def get(hli, tabletype="xport", qargs={}, fargs={}, **kwargs):
    """
    Get a table using the table name from /ca/tables API: pycax.datasets.getdf()

    :param hli: [String] A HLI short code: NOSA, SAR, PNI, JuvOut, PreSmolt, RperS
    :param tabletype: [String] 'base' or 'xport'; default is xport
    :param qargs: [dict] a dictionary of query parameters. The default is no parameters. See usage for common query parameters
    :param fargs: [dict] a dictionary of filter values as {colname1: value}, {colname1: [value1, value2]} or {colname1: value, colname2: value}. The default is no filter. See usage for examples.

    :return: A dictionary of class HliResponse ready for execution

    Usage::

        from pycax import hli
        query = hli.get('NOSA', 'base', qargs={'limit': 1})
        query.execute()
        query.data # get the data
        query.api_url # get the API url

    """
    if not isinstance(qargs, dict):
        raise TypeError('qargs must be a dictionary; got %s' % type(qargs).__name__)

    if not isinstance(fargs, dict):
        raise TypeError('fargs must be a dictionary; got %s' % type(fargs).__name__)

    tablename = return_tablename(hli, tabletype)
    if len(fargs)>1: args['filter'] = tables.dict_to_json(fargs)

    return tables.TablesResponse(tablename, qargs)

def getdf(hli, tabletype="xport", qargs={}, fargs={}, **kwargs):
    """
    Get a HLI table and return a data frame sorted in the same order as the HLI Tabular Query

    This uses the json file for the column names in in the data directory.

    :param hli: [String] A HLI short code: NOSA, SAR, PNI, JuvOut, PreSmolt, RperS
    :param tabletype: [String] 'base' or 'xport'; default is xport
    :param qargs: [dict] a dictionary of query parameters. The default is no parameters. See usage for common query parameters
    :param fargs: [dict] a dictionary of filter values as {colname1: value}, {colname1: [value1, value2]} or {colname1: value, colname2: value}. The default is no filter. See usage for examples.

    :return: A dictionary of class HliResponse ready for execution

    Usage::

        from pycax import hli
        res = hli.getdf('NOSA', 'xport', fargs={'popid': 7})
        res.head()

    """
    if not isinstance(tabletype, str):
        raise TypeError('tabletype must be a string with value base or xport; got %s' % type(tabletype).__name__)
    if not tabletype in ('base', 'xport'):
        raise ValueError('tabletype must be a string with value base or xport')
    if not isinstance(hli, str):
        raise TypeError('hli must be a string with value base or xport; got %s' % type(tabletype).__name__)
    if not hli in ('NOSA', 'SAR', 'PNI', 'JuvOut', 'PreSmolt', 'RperS'):
        raise ValueError('hli must be a string with value NOSA, SAR, PNI, JuvOut, PreSmolt, or RperS')
    if not isinstance(qargs, dict):
        raise TypeError('qargs must be a dictionary; got %s' % type(qargs).__name__)
    if not isinstance(fargs, dict):
        raise TypeError('fargs must be a dictionary; got %s' % type(fargs).__name__)

    tablename = return_tablename(hli, tabletype)
    df = tables.getdf(tablename, qargs=qargs, fargs=fargs, **kwargs)
    col_order = HLI_XPORT_COLNAMES[hli].extend(["species", "agency", "hli", "publish"])
    df = df.reindex(columns=col_order)

    return df

