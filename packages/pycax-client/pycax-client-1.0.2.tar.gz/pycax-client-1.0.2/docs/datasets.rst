.. _datasets:

datasets module
===============

.. py:module:: pycax.datasets

.. autoclass:: DatasetsResponse

Usage
#####

.. code-block:: python

    from pycax import datasets

    query = datasets.get()  # Build the Query
    query.execute()  # Execute the Query
    query.data  # Returns the data

    # or return a data frame directly
    df = datasets.getdf()
    df.head()

Methods:
########

.. autofunction:: get
.. autofunction:: getdf
