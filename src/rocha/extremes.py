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
import rasterio
from rasterio.warp import calculate_default_transform


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

def transform(raster, crs = None):
    """
    Affine transformation for the raster file by coordinate reference system code.

    Parameters
    ----------
    raster : str
        Raster filename
    crs : str
        Coordinate reference system code.

    Notes
    -----
    The CRS code can be accesible from:

    SIRGAS 2000 geographic
    http://spatialreference.org/ref/epsg/4674/

    WGS 84 geographic
    http://spatialreference.org/ref/epsg/4326/


    SIRGAS 2000 projected

    EPSG:31965: SIRGAS 2000 / UTM zone 11N, ... , EPSG:31976: SIRGAS 2000 / UTM zone 22N
    EPSG:31977: SIRGAS 2000 / UTM zone 17S, ... , EPSG:31985: SIRGAS 2000 / UTM zone 25S

    WGS 84 projected

    EPSG:32601: WGS 84 / UTM zone 1N, ... , EPSG:32660: WGS 84 / UTM zone 60N
    EPSG:32701: WGS 84 / UTM zone 1S, ... , EPSG:32760: WGS 84 / UTM zone 60S
    """
    width = None
    height = None

    with rasterio.open(raster) as source:
        # Define the affine matrix transform
        if crs is None:
            transform = source.profile['affine']
        else:
            destiny_crs = rasterio.crs.CRS({'init': crs})

            if destiny_crs == source.crs:
                transform = source.profile['affine']
            else:
                # Reproject
                transform, width, height = calculate_default_transform(source.crs,
                                                            destiny_crs,
                                                            source.width,
                                                            source.height,
                                                            *source.bounds)

    return transform, width, height

def area(raster, crs = None, factor = 1):
    """"
    Calculate the raster valid area.

    The coordinate system defines the area unit.
    For the geographic coordinates the default unit is the square degree.
    For the projected coordinates the default unit is the square meter.

    Parameters
    ----------
    raster : str
        Raster filename
    crs : str
        Coordinate reference system code.
    factor : int or float
        Multiplicative factor to the area.
    """
    affine, _, _ = transform(raster, crs)

    # Pixel width (pixel resolution of the abscissa axis)
    xres = affine[0]

    # Pixel height (pixel resolution of the ordinate axis)
    yres = affine[4]

    # Area in square unit (approximate by reprojection)
    area = abs(xres * yres) * factor

    return round(area, 15)

def total(raster, crs = None, factor = 1):
    """
    Calcule the total valid area.

    Parameters
    ----------
    raster : str
        Raster filename
    crs : str
        Coordinate reference system code.
    factor : int or float
        Multiplicative factor to the area.
    """
    square = area(raster, crs, factor)

    affine, width, height = transform(raster, crs)

    with rasterio.open(raster) as source:
        dataset = source.read(masked = True)
        profile = source.profile.copy()

    print(width, height, affine, profile)

    # Raster valid values
    data = dataset[~dataset.mask]
    count = len(data)

    total = count * square

    return total