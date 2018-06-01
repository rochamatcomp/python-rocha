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

    # Define the compare inverse operation
    compare = operations_inverse[relate]

    # Define the selection data by comparison with threshold
    selection = compare(dataset, threshold)

    # Fill out the selected data with nodata value and mask the raster dataset
    dataset[selection] = nodata
    dataset.fill_value = nodata
    data = ma.masked_where(selection, dataset)

    return data