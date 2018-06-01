# -*- coding: utf-8 -*-
"""
:mod:`extreme` -- Tests raster extremes
=======================================

.. module:: extreme
    :platform: Unix, Windows
    :synopsis: Tests of the raster extremes.
.. moduleauthor:: Andre Rocha <rocha.matcomp@gmail.com>
"""
import rasterio
import numpy as np
import numpy.ma as ma

from src.rocha import extremes

def test_hotspot():
    """
    Test hotspot of raster dataset.
    """
    raster = 'data/atlantic_forest.tif'
    output = 'data/atlantic_forest_hotspots.tif'
    threshold = 0.6996560782009352

    with rasterio.open(raster) as source:
        dataset = source.read(masked = True)
        nodata = source.nodata

    result = extremes.hotspots(dataset, '>', threshold, nodata)

    with rasterio.open(output) as source:
        data = source.read(masked = True)

    assert result.all() == data.all()