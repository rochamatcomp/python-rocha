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
    driver = gdal.GetDriverByName(code)

    if driver is None:
        message = f'Invalid driver code. Checks the valid code from: http://www.gdal.org/formats_list.html'
        print(message)

        return None


    if driver.GetMetadataItem(gdal.DCAP_RASTER) is None:
        message = f'Driver don\'t handles raster data. Checks the code of the raster formats from: http://www.gdal.org/formats_list.html'
        print(message)

        return None

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