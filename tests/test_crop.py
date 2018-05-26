# -*- coding: utf-8 -*-
"""
:mod:`crop` -- Tests raster and vector crop
===========================================

.. module:: crop
    :platform: Unix, Windows
    :synopsis: Tests of the crop the raster datasets for vector geometries.
.. moduleauthor:: Andre Rocha <rocha.matcomp@gmail.com>
"""

import fiona
import rasterio
import src.rocha.crop as crop

def test_column_string():
    """
    Test vector property as string.
    """
    vector = "data/regions.shp"
    column = "REGION"
    names = ["mid-west", "northeast", "southeast", "south"]

    properties = crop.properties(vector)

    results = [property[column].lower() for property in properties if isinstance(property[column], str)]
    assert results == names

def test_column_number():
    """
    Test vector property as number.
    """
    vector = "data/regions.shp"
    column = "ID"
    codes = [5, 2, 3, 4]

    properties = crop.properties(vector)

    results = [property[column] for property in properties if isinstance(property[column], (int, float))]
    assert results == codes

def test_geometry():
    """
    Test vector geometry.
    """

    vector = "data/regions.shp"
    subvectors = ["data/region_mid-west.shp", "data/region_northeast.shp", "data/region_southeast.shp", "data/region_south.shp"]

    geometries = crop.geometries(vector)

    for subvector, geometry in zip(subvectors, geometries):
        with fiona.open(subvector, layer = 0) as source:
            feature = next(source)

        assert feature["geometry"] == geometry

def test_crop_global():
    """
    Test crop raster for vector extern boundary.
    """

    vector = "data/regions.shp"
    raster = "data/forest.tif"

    geometries = crop.geometries(vector)
    results = crop.crop(geometries, raster, features = False)

    result, transform = next(results)

    with rasterio.open(raster) as source:
        data = source.read(1)
        affine = source.affine

    assert result.all() == data.all()
    assert transform == affine


def test_crop_individual():
    """
    Test crop raster for each vector feature boundary.
    """

    vector = "data/regions.shp"
    raster = "data/forest.tif"
    subrasters = ["data/forest_mid-west.tif", "data/forest_northeast.tif", "data/forest_southeast.tif", "data/forest_south.tif"]

    geometries = crop.geometries(vector)
    results = crop.crop(geometries, raster, features = True)

    for subraster, (result, transform) in zip(subrasters, results):
        with rasterio.open(subraster) as source:
            data = source.read(1)
            affine = source.affine

        assert result.all() == data.all()
        assert transform == affine