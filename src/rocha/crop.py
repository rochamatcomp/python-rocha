# -*- coding: utf-8 -*-
"""
:mod:`crop` -- Raster and vector crop
=====================================

.. module:: crop
    :platform: Unix, Windows
    :synopsis: Crop the raster datasets by vector geometries.
.. moduleauthor:: Andre Rocha <rocha.matcomp@gmail.com>
"""

import fiona
import rasterio
import rasterio.mask

def properties(vector, layer = 0):
    """
    Vector property data.

    Vector property from column value from layer.

    Parameters
    ----------
    vector : str
        Vector filename.
    layer : int or str
        Vector layer index or layer name (the default is 0 for the first layer).

    Yields
    ------
    values : dict of {str : int, float, str or date}
        Feature properties from all column.
    """
    with fiona.open(vector, layer = layer) as source:
        for feature in source:
            values = feature["properties"]

            yield values

def geometries(vector, layer = 0):
    """
    Vector spatial data.

    Vector spatial from layer geometry as type and coordinates.

    Parameters
    ----------
    vector : str
        Vector filename.
    layer : int or str
        Vector layer index or layer name (the default is 0 for the first layer).

    Yields
    ------
    geometries : dict
        Geometries as type and coordinates.
    """
    with fiona.open(vector, layer = layer) as source:
        for feature in source:
            geometry = feature["geometry"]

            yield geometry