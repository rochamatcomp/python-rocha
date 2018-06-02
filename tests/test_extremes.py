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

def test_area_geographic():
    """
    Test area for geographic coordinate system as square degrees.
    """
    raster = 'data/geographic.tif'
    area = 0.25

    result = extremes.area(raster)

    assert result == area

def test_area_projected():
    """
    Test area for projected coordinate system as square meters.
    """
    raster = 'data/projected.tif'
    area = 2970864583.066144

    result = extremes.area(raster)

    assert result == area

def test_area_reprojected():
    """
    Test area for reprojected coordinate system as square meters.
    """
    raster = 'data/geographic.tif'
    area = 2970864583.066144

     # Reproject SIRGAS 2000 Project 23S
    crs = 'EPSG:31983'

    result = extremes.area(raster, crs)

    assert result == area

def test_area_reprojected_factor():
    """
    Test area for reprojected coordinate system as square kilometers.
    """
    raster = 'data/geographic.tif'
    area = 2970.864583066144

    # Reproject SIRGAS 2000 Project 23S
    crs = 'EPSG:31983'

    result = extremes.area(raster, crs, 1e-6)

    assert result == area

def test_area_reprojected_file():
    """
    Test area for reprojected coordinate system as square meters by file.
    """
    projected = 'data/projected.tif'
    geographic = 'data/geographic.tif'
    area = 2970864583.066144

    # Reproject SIRGAS 2000 Project 23S
    crs = 'EPSG:31983'

    area = extremes.area(projected)
    result = extremes.area(geographic, crs)

    assert result == area

def test_total_geographic():
    """
    Test total valid area for geographic coordinate system as square degrees.
    """
    raster = 'data/hotspots_geographic.tif'
    total = 26.5

    result = extremes.total(raster)

    assert result == total

def test_total_projected():
    """
    Test total valid area for projected coordinate system as square meters.
    """
    raster = 'data/hotspots_projected.tif'
    total = 317882510388.0774

    result = extremes.total(raster)

    assert result == total

def test_total_reprojected():
    """
    Test total valid area for reprojected file as square meters.
    """
    raster = 'data/hotspots_geographic.tif'
    #total = 317882510388.0774
    total = 314911645805.0113 # Don't reproject data, just area.

    # Reproject SIRGAS 2000 Project 23S
    crs = 'EPSG:31983'

    result = extremes.total(raster, crs)

    assert result == total