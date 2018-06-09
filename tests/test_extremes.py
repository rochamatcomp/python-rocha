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

from src.rocha import paths
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

def test_limits():
    """
    Test rasters minimum and maximum values for each file.
    """
    values_min = [-47.164523294078,
                 -38.156690778818,
                 -49.476265733386,
                 -67.341787619557,
                 -58.670952135006,
                 -81.968584509983,
                 -40.882100744325,
                 -48.449972234068,
                 -42.138962499961,
                 -30.837406733355,
                 -49.920177880745,
                 -56.948878267812]

    values_max = [29.552618422328,
                 68.555008124737,
                 33.18806002876,
                 -10.30071953103,
                 0.78961871286549,
                 6.5030381149153,
                 55.246224002166,
                 69.638073392539,
                 94.044943529601,
                 84.034367323136,
                 69.26120559526,
                 86.193456962634]

    path = 'data/relatives'
    pattern = '*.tif'

    rasters = paths.find(path, pattern)

    results = [result for result in extremes.limits(rasters)]
    results_min, results_max = zip(*results)

    np.testing.assert_allclose(sorted(results_min), sorted(values_min))
    np.testing.assert_allclose(sorted(results_max), sorted(values_max))

def test_min_max():
    """
    Test rasters minimum and maximum values for all files.
    """
    value_min = -81.968584509983
    value_max = 94.044943529601

    path = 'data/relatives'
    pattern = '*.tif'

    rasters = paths.find(path, pattern)

    result_min, result_max = extremes.min_max(rasters)

    np.testing.assert_allclose(result_min, value_min)
    np.testing.assert_allclose(result_max, value_max)