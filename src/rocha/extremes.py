# -*- coding: utf-8 -*-
"""
:mod:`extreme` -- Raster extremes
=================================

.. module:: extreme
    :platform: Unix, Windows
    :synopsis: Extremes of the raster datasets.
.. moduleauthor:: Andre Rocha <rocha.matcomp@gmail.com>
"""
import operator
import numpy.ma as ma
from rocha import paths

def hotspots(dataset, relate, threshold, nodata):
    """
    Hotspots by comparation with threshold value.

    Parameters
    ----------
    dataset : array
        Raster data.
    relate : str
        Symbol to compare the data with threshold value.
    threshold : int or float
        Threshold value.
    nodata : int or float
        Nodata value.

    Returns
    -------
    data : array
        Hotspot raster data.

    Notes
    -----
    To save the hotspot raster data is necessary to updating the profile nodata value before to save.
    """
    # Inverse operation, to masking data
    operations_inverse = {
        '>': operator.le,  # <=
        '<': operator.ge,  # >=
        '>=': operator.lt, # <
        '<=': operator.gt, # >
        '==': operator.ne,  # !=
        '!=': operator.eq  # ==
    }

    if relate not in operations_inverse:
        return None

    # Define the compare operation
    compare = operations_inverse[relate]

    # Fill out the data masked with nodata value and mask the raster dataset, by comparison with threshold
    dataset[compare(dataset, threshold)] = nodata
    dataset.fill_value = nodata
    data = ma.masked_where(compare(dataset, threshold), dataset)

    return data