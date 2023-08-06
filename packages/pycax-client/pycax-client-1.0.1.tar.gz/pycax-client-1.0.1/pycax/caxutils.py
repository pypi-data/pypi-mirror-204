"""
Utility functions for internal use across various modules.
"""
from urllib.parse import urlencode

import requests
import pkgutil
import pycax

cax_baseurl = "https://api.streamnet.org/api/v1/"

cax_api_key = "7A2F1EA9-4882-49E8-B23D-7DC202C2ACA5"

class NoResultException(Exception):
    """
    Thrown when query returns no results.
    """

    pass


def build_api_url(url, args):
    """
    Builds the API URL based on the base url and the arguments
    """
    return url + "?" + urlencode({k: v for k, v in args.items() if v is not None})

def make_ua():
    return {
        "user-agent": "python-requests/"
        + requests.__version__
        + ",pycax/"
        + pycax.__version__
    }

def cax_GET(url, args, **kwargs):
    """
    Handles technical details of sending GET request to the API
    """
    args['XApiKey']=cax_api_key
    out = requests.get(url, params=args, headers=make_ua(), **kwargs)
    out.raise_for_status()
    stopifnot(out.headers["content-type"])
    return out.json()
    

def stopifnot(x, ctype="application/json;charset=utf-8"):
    if x != ctype:
        raise NoResultException("content-type did not equal " + str(ctype))

def stop(x):
    raise ValueError(x)

def as_list(x):
    if type(x) is list:
        return x
    else:
        return [x]

def get_data(filename):
    # Read the data file
    data = pkgutil.get_data('pycax', 'data/' + filename)

    # Return the data
    return data
