# -*- coding: utf-8 -*-
"""
:mod:`drivers` -- Raster drivers
================================

.. module:: drivers
    :platform: Unix, Windows
    :synopsis: Handle the raster drivers informations.
.. moduleauthor:: Andre Rocha <rocha.matcomp@gmail.com>
"""
from osgeo import gdal

def validate(code):
    """
    Raster driver validate code.

    Parameters
    ----------
    code : str
        Driver code.

    Notes
    -----
        The information of the GDAL raster formats, including the drivers codes,
        are available in: http://www.gdal.org/formats_list.html
    """
    driver = gdal.GetDriverByName(code)
    notes = 'Checks the valid code for raster formats in: http://www.gdal.org/formats_list.html'

    if driver is None:
        message = 'Invalid driver code.'
        raise ValueError(message, code, notes)

    if driver.GetMetadataItem(gdal.DCAP_RASTER) is None:
        name = driver.GetMetadataItem(gdal.DMD_LONGNAME)
        message = 'Driver don\'t handles raster data.'
        raise ValueError(message, code, name, notes)

    return driver

def metadata(code):
    """
    Raster driver metadata.

    Raster driver metadata from driver code.

    Parameters
    ----------
    code : str
        Driver code.

    Notes
    -----
        The information of the GDAL raster formats, including the drivers codes,
        are available in: http://www.gdal.org/formats_list.html
    """
    driver = validate(code)

    # The descriptive name for the file format
    name = driver.GetMetadataItem(gdal.DMD_LONGNAME)

    # The main extension used for files of this type
    extension = driver.GetMetadataItem(gdal.DMD_EXTENSION)

    # The help topic for this driver
    topic = driver.GetMetadataItem(gdal.DMD_HELPTOPIC)
    help_topic = f'http://www.gdal.org/{topic}'

    # The standard mime type for this file format
    mime_type = driver.GetMetadataItem(gdal.DMD_MIMETYPE)

    return name, extension, help_topic, mime_type

def extension(code, main = True):
    """
    Raster driver metadata.

    Raster driver metadata from driver code.

    Parameters
    ----------
    code : str
        Driver code.

    Notes
    -----
        The information of the GDAL raster formats, including the drivers codes,
        are available in: http://www.gdal.org/formats_list.html
    """
    driver = validate(code)

    # The extensions used for files of this type
    extensions = driver.GetMetadataItem(gdal.DMD_EXTENSIONS).split()

    if main and len(extensions) > 0:
        return extensions[0]

    return extensions