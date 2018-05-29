# -*- coding: utf-8 -*-
"""
:mod:`drivers` -- Tests raster drivers
======================================

.. module:: drivers
    :platform: Unix, Windows
    :synopsis: Handle the raster drivers informations.
.. moduleauthor:: Andre Rocha <rocha.matcomp@gmail.com>
"""
import src.rocha.drivers as drivers

def test_valid_driver():
    """
    Test valid driver.

    Valid raster format available in: http://www.gdal.org/formats_list.html
    """
    code = 'GTiff'
    name = 'GeoTIFF'
    extension = 'tif'
    help_topic = 'http://www.gdal.org/frmt_gtiff.html'
    mime_type = 'image/tiff'

    results = drivers.metadata(code)

    assert results == (name, extension, help_topic, mime_type)

def test_invalid_driver():
    """
    Test invalid driver.
    """
    code = 'Tiff'
    results = drivers.metadata(code)

    assert results is None

def test_dont_raster_handles():
    """
    Test invalid driver.
    """
    code = 'CSV'
    results = drivers.metadata(code)

    assert results is None