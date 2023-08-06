.. _hli:

hli module
==========

.. py:module:: pycax.hli

Usage
#####

.. code-block:: python

    from pycax import hli

    # Download one record as a data frame
    df = hli.getdf("NOSA", qargs={'limit': 1})
    id = df['popid'][0]
    # Download a data frame using a filter
    filt = {'popid': id}
    df = hli.getdf("NOSA", fargs=filt)
 
Methods:
########

.. autofunction:: get
.. autofunction:: getdf
.. autofunction:: return_tablename

