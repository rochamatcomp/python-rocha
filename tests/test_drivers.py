# -*- coding: utf-8 -*-
"""
:mod:`drivers` -- Tests raster drivers
======================================

.. module:: drivers
    :platform: Unix, Windows
    :synopsis: Handle the raster drivers informations.
.. moduleauthor:: Andre Rocha <rocha.matcomp@gmail.com>
"""
import pytest
import src.rocha.drivers as drivers

def test_valid_driver():
    """
    Test valid driver.

    Valid raster format available in: http://www.gdal.org/formats_list.html
    """
    code = 'GTiff'

    result = drivers.validate(code)

    assert result is not None

def test_invalid_driver():
    """
    Test invalid driver.
    """
    code = 'Tiff'

    with pytest.raises(ValueError, match = '.*driver.*') as info:
        results = drivers.validate(code)

def test_dont_raster_handles():
    """
    Test invalid driver.
    """
    code = 'CSV'

    with pytest.raises(ValueError, match = '.*handle.*') as info:
        results = drivers.validate(code)

def test_valid_metadata():
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

def test_invalid_metadata():
    """
    Test invalid driver.
    """
    code = 'Tiff'

    with pytest.raises(ValueError, match = '.*driver.*') as info:
        results = drivers.validate(code)

def test_dont_raster_handles_metadata():
    """
    Test invalid driver.
    """
    code = 'CSV'

    with pytest.raises(ValueError, match = '.*handle.*') as info:
        results = drivers.validate(code)

def test_valid_extension():
    """
    Test valid extension file.
    """
    code = 'GTiff'
    extension = 'tif'

    result = drivers.extension(code)

    assert result == extension

def test_valid_extension_list():
    """
    Test valid extension file, from list of extensions.
    """
    code = 'GTiff'
    extension = 'tiff'

    results = drivers.extension(code, main = False)

    assert extension in results
