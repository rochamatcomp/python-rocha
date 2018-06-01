# -*- coding: utf-8 -*-
"""
:mod:`crop` -- Raster and vector crop
=====================================

.. module:: crop
    :platform: Unix, Windows
    :synopsis: Crop the raster datasets by vector geometries.
.. moduleauthor:: Andre Rocha <rocha.matcomp@gmail.com>
"""
import affine
import fiona
import rasterio
import rasterio.mask

from . import paths
from . import drivers

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

def mask(geometries, raster):
    """
    Mask raster dataset by vector geometries.

    Parameters
    ----------
    geometries : str
        Vector geometries.
    raster : str
        Raster filename.

    Returns
    -------
    data : array
        Raster data.
    profile : dict
        Raster profile.
    """
    with rasterio.open(raster) as source:
        data, transform = rasterio.mask.mask(source, geometries, crop = True)

        # Update the mask
        data.mask = (data == source.nodata) | data.mask

        # Profile for cropped raster
        profile = source.profile.copy()
        profile.update({'height': data.shape[1],
                        'width': data.shape[2],
                        'transform': transform,
                        'affine': transform})

    return data, profile

def crop(geometries, raster, features = False):
    """
    Crop raster dataset by vector geometries.

    Parameters
    ----------
    geometries : str
        Vector geometries.

    raster : str
        Raster filename.

    features : bool
        Crop by foreach features. False: crop global, True: crop individual (default).

    Yields
    ------
    data : array
        Raster data.

    affine : affine
        Raster affine transform.

    meta : metadata
        Raster metadata.
    """
    if features:
        for geometry in geometries:
            shapes = [geometry]
            dataset = mask(shapes, raster)

            yield dataset
    else:
        shapes = [geometry for geometry in geometries]
        dataset = mask(shapes, raster)

        yield dataset

def multiples(vector, column, pattern, input_path, output_path, driver = 'GTiff'):
    """
    Crop the multiples rasters for each vector features.

    Find the rasters files by pattern and crops these by all features of the vector.
    The vector column name defines the property value to connect the raster output filenames with
    the vector features, in the end of those filenames.

    Parameters
    ----------
    vector : str
        Vector filename.
    column : str
        Column name.
    pattern : str
        Pattern like unix shell-style wildcards.
    input_path : str
        Path from raster input files.
    output_path : str
        Path to cropped raster output files.
    driver : str
        Driver code. Default GeoTIFF file format (GTiff).
        Code to output raster format.

    Yields
    ------
    data : array
        Raster data.
    profile : dict
        Raster profile.
    output_file : str
        Raster output filename.

    Notes
    -----
        The information of the GDAL raster formats, including the drivers codes,
        are available in: http://www.gdal.org/formats_list.html
    """
    # Vector geometries and properties as lists
    geoms = [geometry for geometry in geometries(vector)]
    props = [property for property in properties(vector)]

    # Raster files like pattern
    rasters = paths.find(input_path, pattern)

    for raster in rasters:
        dataset = crop(geoms, raster, features = True)

        for property, (data, profile) in zip(props, dataset):

            # Update the driver and file extension
            profile.update({'driver': driver})
            extension = f'.{drivers.extension(driver)}'

            # Vector column property as file label
            label = f'_{property[column]}'.lower()

            output_file = paths.output(raster, input_path, output_path, extra = label, output_extension = extension)

            yield data, profile, output_file