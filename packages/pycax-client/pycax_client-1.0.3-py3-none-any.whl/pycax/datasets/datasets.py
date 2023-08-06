"""
ca/tables/ API endpoints. These are the available data sets with meta data, e.g. name and id.
"""

import pandas as pd

from pycax.caxutils import build_api_url, cax_baseurl, cax_GET

def get(args={}, **kwargs):
    """
    Get the table of data sets

    :param args: [dict] a dictionary of query parameters. The default is no parameters which returns the full table.
    :return: A Tables Response of the JSON

    Usage::

        from pycax import tables
        query = tables.get()
        res = query.execute()
        query.to_pandas()
    """
    url = cax_baseurl + "ca/tables"
  
    # returns a DatasetsResponse object
    return DatasetsResponse(url, args)
    
def getdf(args={}, **kwargs):
    """
    Make query for the data sets and return a pandas DataFrame

    :param args: [dict] a dictionary of query parameters. The default is no parameters which returns the full table.
    :return: A pandas DataFrame

    Usage::

        from pycax import tables
        datasets.getdf()
    """
    query = get(args=args, **kwargs)
    query.execute()
   
    return query.to_pandas()

class DatasetsResponse:
    """
    An CAX Datasets Response Object
    """

    def __init__(self, url, args):
        """
        Initialise the object parameters
        """
        # public members
        self.data = None
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
        return pd.DataFrame(self.data["tables"])
