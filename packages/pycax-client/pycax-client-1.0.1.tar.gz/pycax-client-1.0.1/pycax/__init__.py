"""
pycax library
~~~~~~~~~~~~~~~~~~~~~

pycax is a Python client for CAX.

Example usage:

# Import entire library
import pycax
# or import modules as needed
## hli
from pycax import hli
## tables
from pycax import tables
## datasets (a table of the available data sets)
from pycax import datasets
## utils
from pycax import utils

## use advanced logging
### setup first
import requests
import logging
import httplib as http_client
http_client.HTTPConnection.debuglevel = 1
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True
### then make request
#from pycax import hli
#hli.get(fargs={'popid': 7})
"""

try:
    from ._version import __version__
except ImportError:
    __version__ = "unknown"

__title__ = "pycax"
__author__ = "Eli Holmes and Mari Williams"
__license__ = "MIT"

from .hli import hli
from .datasets import datasets
from .tables import tables

__all__ = [
    "hli",
    "datasets",
    "tables",
]
