"""
Get a table from the API via table_id
"""

import json
import sys
from urllib.parse import urlencode

import pandas as pd
import numpy as np
import requests

from pycax.caxutils import (
    build_api_url, 
    cax_baseurl, 
    cax_GET,
    as_list,
    stop,
)

from pycax import datasets

CAX_TABLES = datasets.getdf()

class TablesResponse:
    """
    A tables Response Object
    """

    def __init__(self, tablename, args):
        """
        Initialise the object parameters
        """
        self.data = None
        self.tablename = tablename
        self.tableid = tableid(tablename)[0]
        args['table_id'] =  self.tableid
        url = cax_baseurl + "ca"
        self.api_url = build_api_url(url, args)
        
        # private members
        self.__args = args
        self.__url = url
  
    def execute(self, **kwargs):
        """
        Execute or fetch the data based on the query
        """
        out = cax_GET(
            self.__url, self.__args, **kwargs
        )
        self.data = out
        return self.data

    def to_pandas(self):
        """
        Convert the results into a pandas DataFrame
        """
        return pd.DataFrame(self.data["records"])


def get(tablename, qargs={}, fargs={}, **kwargs):
    """
    Get a table using the table name from /ca/tables API

    :param tablename: [String] A table name listed in the datasets table
    :param qargs: [dict] a dictionary of query parameters. The default is no parameters. See usage for common query parameters
    :param fargs: [dict] a dictionary of filter values as {colname1: value}, {colname1: [value1, value2]} or {colname1: value, colname2: value}. The default is no filter. See usage for examples.

    :return: A dictionary of class TableResponse ready for execution

    Usage::

        from pycax import tables
        query = tables.get('EscData', qargs={'limit': 1})
        query.execute()
        query.data # get the data
        query.api_url # get the API url

    """
    if not isinstance(qargs, dict):
        raise TypeError('qargs must be a dictionary; got %s' % type(qargs).__name__)

    if not isinstance(fargs, dict):
        raise TypeError('fargs must be a dictionary; got %s' % type(fargs).__name__)

    if len(fargs)>0: qargs['filter'] = dict_to_json(fargs)

    return TablesResponse(tablename, qargs)


def getdf(tablename, qargs={}, fargs={}, **kwargs):
    """
    Make table query and return a pandas DataFrame

    :param qargs: [dict] a dictionary of query parameters. The default is no parameters which returns the full table.
    :param fargs: [dict] a dictionary of filter values as {colname1: value}, {colname1: [value1, value2]} or {colname1: value, colname2: value}. The default is no filter. See usage for examples.
    :return: A pandas DataFrame

    Usage::

        from pycax import tables
        tables.getdf('EscData')
    """
    query = get(tablename, qargs=qargs, fargs=fargs, **kwargs)
    res = query.execute()
   
    return query.to_pandas()

def tableid(tablename):
    """
    Retrieve a table id given a tablename

    :param tablename: [String] table name from pycax.tables.getdf()["name"]

    :return: A table id as an array of length 1 with id as a string

    Usage::

        from pycax import tables
        tables.tableid("NOSA")
    """
    tab = CAX_TABLES[CAX_TABLES['name']==tablename]['id']
    if not 1 == len(tab):
        stop('Something wrong; no table id returned. Did you misspell the table name?')

    return tab.values

def dict_to_json(fargs):
    """
    Convert a dictionary to JSON format for CAX API: field, value, string format

    :param fargs: [dict] a dictionary of filter values as {colname1: value}, {colname1: [value1, value2]} or {colname1: value, colname2: value}. The default is no filter. See usage for examples.
    :return: JSON for the filter in the format that CAX API wants: '[{"field": "popid", "value": 7, "type": "string"}]'

    Usage::

        from pycax import tables
        tables.dict_to_json({'popid':7})
    """    
    # The CAX API requires that the filter be in a specific format
    array = [ {'field' : i, 'value' : fargs[i], 'type': 'string' if len(as_list(fargs[i]))<2 else 'list'}  for i in fargs]
    json_string = json.dumps(array, default=lambda x: x.item() if isinstance(x, np.generic) else x)
    
    return json_string