.. _tables:

tables module
=============

.. py:module:: pycax.tables

.. autoclass:: TablesResponse

Usage
#####

.. code-block:: python

    from pycax import tables

    query = tables.get("NOSA", qargs={'limit': 2})
    query.execute()
    query.data  # Returns the data
    query.api_url  # Returns the API URL
    query.to_pandas()  # Returns a pandas DataFrame

    # Download one record as a data frame
    df = tables.getdf("NOSA", qargs={'limit': 1})
    id = df['popid'][0]
    # Download a data frame using a filter. Here only return popid = 7
    filt = {'popid': id}
    df = tables.getdf("NOSA", fargs=filt)

Methods:
########

.. autofunction:: get
.. autofunction:: getdf
.. autofunction:: tableid
.. autofunction:: dict_to_json