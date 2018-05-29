# -*- coding: utf-8 -*-
"""
:mod:`crop` -- Tests raster and vector crop
===========================================

.. module:: crop
    :platform: Unix, Windows
    :synopsis: Tests of the crop the raster datasets for vector geometries.
.. moduleauthor:: Andre Rocha <rocha.matcomp@gmail.com>
"""
import affine
import fiona
import rasterio
from rocha import crop

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
    subvectors = ["data/output/region_mid-west.shp",
                  "data/output/region_northeast.shp",
                  "data/output/region_southeast.shp",
                  "data/output/region_south.shp"]

    geometries = crop.geometries(vector)

    for subvector, geometry in zip(subvectors, geometries):
        with fiona.open(subvector, layer = 0) as source:
            feature = next(source)

        assert feature["geometry"] == geometry

def test_mask():
    """
    Test crop raster for vector extern boundary.
    """
    vector = "data/regions.shp"
    raster = "data/forest.tif"

    geometries = crop.geometries(vector)
    shapes = [geometry for geometry in geometries]
    result, profile = crop.mask(shapes, raster)

    with rasterio.open(raster, 'r') as source:
        data = source.read(1)
        metadata = source.profile.copy()

        transform = metadata['transform']
        metadata.update({'transform': affine.Affine.from_gdal(transform[0],
                                                              transform[1],
                                                              transform[2],
                                                              transform[3],
                                                              transform[4],
                                                              transform[5])})

    assert result.all() == data.all()
    assert profile == metadata

def test_crop_global():
    """
    Test crop raster for vector extern boundary.
    """
    vector = "data/regions.shp"
    raster = "data/forest.tif"

    geometries = crop.geometries(vector)
    results = crop.crop(geometries, raster, features = False)

    result, profile = next(results)

    with rasterio.open(raster) as source:
        data = source.read()
        metadata = source.profile.copy()

        transform = metadata['transform']
        metadata.update({'transform': affine.Affine.from_gdal(transform[0],
                                                              transform[1],
                                                              transform[2],
                                                              transform[3],
                                                              transform[4],
                                                              transform[5])})

    assert result.all() == data.all()
    assert profile == metadata


def test_crop_individual():
    """
    Test crop raster for each vector feature boundary.
    """
    vector = "data/regions.shp"
    raster = "data/forest.tif"
    subrasters = ["data/output/forest_mid-west.tif",
                  "data/output/forest_northeast.tif",
                  "data/output/forest_southeast.tif",
                  "data/output/forest_south.tif"]

    geometries = crop.geometries(vector)
    results = crop.crop(geometries, raster, features = True)

    for subraster, (result, profile) in zip(subrasters, results):
        with rasterio.open(subraster) as source:
            data = source.read()
            metadata = source.profile.copy()

            transform = metadata['transform']
            metadata.update({'transform': affine.Affine.from_gdal(transform[0],
                                                                transform[1],
                                                                transform[2],
                                                                transform[3],
                                                                transform[4],
                                                                transform[5])})

        assert result.all() == data.all()
        assert profile == metadata

def test_multiples():
    """
    Test the multiples crops.
    """
    input_path = 'data'
    output_path = 'data/output'
    pattern = '*forest.tif'
    vector = 'data/regions.shp'
    driver = 'GTiff'
    column = 'REGION'

    subrasters = ["data/output/forest_mid-west.tif",
                  "data/output/forest_northeast.tif",
                  "data/output/forest_southeast.tif",
                  "data/output/forest_south.tif"]

    results = crop.multiples(vector, column, pattern, input_path, output_path, driver)

    for subraster, (result, profile, filename) in zip(subrasters, results):
        with rasterio.open(subraster) as source:
            data = source.read()
            metadata = source.profile.copy()

            transform = metadata['transform']
            metadata.update({'transform': affine.Affine.from_gdal(transform[0],
                                                                transform[1],
                                                                transform[2],
                                                                transform[3],
                                                                transform[4],
                                                                transform[5])})

        assert result.all() == data.all()
        assert profile == metadata
        assert filename == subraster