pycax |version|
===============

.. |pypi| 

|docs| |coverage|

Python client for the `StreamNet REST API
<https://www.streamnet.org/resources/exchange-tools/rest-api-documentation/>`__.

`Source on GitHub at nwfsc-math-bio/pycax <https://github.com/nwfsc-math-bio/pycax>`__

Other CAX clients:

* R: `rCAX`, `nwfsc-math-bio/rCAX <https://nwfsc-math-bio.github.io/rCAX>`__

Installation
============

.. 
   from pypi

   .. code-block:: console

    pip install pycax-client

dev version

.. code-block:: console

    pip install git+git://github.com/nwfsc-math-bio/pycax.git#egg=pycax-client

Examples
===========

* user_guide `Jupyter notebook <https://github.com/nwfsc-math-bio/pycax/tree/main/notebooks>`

Library API
===========

``pycax`` is split up into modules for the list of tables (/ca/tables) and individual tables (/ca?table_id=...).

* ``datasets`` - The tables available for download with metadata.
* ``tables`` - Download an individual table given its name (as in the datasets table)
* ``hli`` - Download a HLI table in either "XPort" (default) or base format. "XPort" is the same as the CAP Tabular Query.

For accessing the HLI tables, you only need to import the `hli` module. A maximum of 1000 rows of data are downloaded (by default).
Typically you will want to filter the query by passing in `fargs` as dictionary with the column name values. For example,
`{'popid': 7}` would return popid equal to 7 only.

Examples of functions returning the data as a pandas data frame are shown.

HLI module
##########

.. code-block:: python

    from pycax import hli

    res = hli.getdf("NOSA", tabletype="xport", fargs={'popid':  7})
    res.head()


Tables module
#############

.. code-block:: python

    from pycax import tables

    res = tables.getdf("EscData", fargs={'popid':  7})
    res.head()

Datasets module
###############

.. code-block:: python

    from pycax import datasets

    res = datasets.getdf()
    res['name', 'id'].head()

Meta
====

* License: MIT

.. |pypi| image:: https://img.shields.io/pypi-client/v/pycax-client.svg
   :target: https://pypi.python.org/pypi-client/pycax

.. |docs| image:: https://github.com/nwfsc-math-bio/pycax/actions/workflows/deploy-docs.yml/badge.svg
   :target: https://nwfsc-math-bio.github.io/pycax
   
.. |coverage| image:: https://nwfsc-math-bio.github.io/pycax/coverage.svg
   :target: https://nwfsc-math-bio.github.io/pycax/_codecoverage/index.html



Contents
========

.. toctree::
   :maxdepth: 2

   hli
   tables
   datasets
   changelog_link

License
=======

MIT


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
