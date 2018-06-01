# -*- coding: utf-8 -*-
"""
:mod:`paths` -- Test paths manipulation
=======================================

.. module:: paths
    :platform: Unix, Windows
    :synopsis: Paths manipulation and files discovery.
.. moduleauthor:: Andre Rocha <rocha.matcomp@gmail.com>
"""
import os
from src.rocha import paths

def test_full_path():
    """
    Test find full path of the files.
    """
    path = 'data'
    pattern = '*region*.shp'
    files = ['data/regions.shp',
             'data/output/region_mid-west.shp',
             'data/output/region_northeast.shp',
             'data/output/region_southeast.shp',
             'data/output/region_south.shp']

    current = os.getcwd()
    filenames = [os.sep.join([current, file]) for file in files]

    results = paths.find(path, pattern, relative = False)
    names = [name for name in results]

    assert names == filenames

def test_relative_path():
    """
    Test find relative path of the files.
    """
    path = 'data'
    pattern = '*region*.shp'
    filenames = ['data/regions.shp',
                 'data/output/region_mid-west.shp',
                 'data/output/region_northeast.shp',
                 'data/output/region_southeast.shp',
                 'data/output/region_south.shp']

    results = paths.find(path, pattern, relative = True)
    names = [name for name in results]

    assert names == filenames

def test_output_same_structure():
    """
    Test output filename with the same directory structure as input filename.
    """
    input_path = 'data/inputs'
    output_path = 'data/outputs'
    input_file = 'data/inputs/south/raster.tif'
    output_file = 'data/outputs/south/raster.tif'

    result = paths.output(input_file, input_path, output_path, change = False)

    assert result == output_file

def test_output_change_root():
    """
    Test output filename with output path as root path.

    Output filename with a simple directory structure.
    """
    input_path = 'data/inputs'
    output_path = 'data/outputs'
    input_file = 'data/inputs/south/raster.tif'
    output_file = 'data/outputs/raster.tif'

    result = paths.output(input_file, input_path, output_path, change = True)

    assert result == output_file

def test_output_change_extra_end():
    """
    Test output filename with the extra name in the ending, and changed strutucture.
    """
    input_path = 'data/inputs'
    output_path = 'data/outputs'
    input_file = 'data/inputs/south/raster.tif'
    output_file = 'data/outputs/raster_south.tif'
    extra = '_south'

    result = paths.output(input_file, input_path, output_path, change = True, extra = extra, begin = False)

    assert result == output_file

def test_output_change_extra_begin():
    """
    Test output filename with the extra name in the beginning, and changed strutucture.
    """
    input_path = 'data/inputs'
    output_path = 'data/outputs'
    input_file = 'data/inputs/south/raster.tif'
    output_file = 'data/outputs/south_raster.tif'
    extra = 'south_'

    result = paths.output(input_file, input_path, output_path, change = True, extra = extra, begin = True)

    assert result == output_file

def test_output_same_extra_end():
    """
    Test output filename with the extra name in the ending, and the same strutucture.
    """
    input_path = 'data/inputs'
    output_path = 'data/outputs'
    input_file = 'data/inputs/south/raster.tif'
    output_file = 'data/outputs/south/raster_south.tif'
    extra = '_south'

    result = paths.output(input_file, input_path, output_path, change = False, extra = extra, begin = False)

    assert result == output_file

def test_output_same_extra_begin():
    """
    Test output filename with the extra name in the beginning, and the same strutucture.
    """
    input_path = 'data/inputs'
    output_path = 'data/outputs'
    input_file = 'data/inputs/south/raster.tif'
    output_file = 'data/outputs/south/south_raster.tif'
    extra = 'south_'

    result = paths.output(input_file, input_path, output_path, change = False, extra = extra, begin = True)

    assert result == output_file

def test_output_change_extension():
    """
    Test output filename with another extension, and changed strutucture.
    """
    input_path = 'data/inputs'
    output_path = 'data/outputs'
    input_file = 'data/inputs/south/raster.tif'
    output_file = 'data/outputs/raster.asc'
    extension = '.asc'

    result = paths.output(input_file, input_path, output_path, change = True, output_extension = extension)

    assert result == output_file

def test_output_same_extension():
    """
    Test output filename with another extension, and the same strutucture.
    """
    input_path = 'data/inputs'
    output_path = 'data/outputs'
    input_file = 'data/inputs/south/raster.tif'
    output_file = 'data/outputs/south/raster.asc'
    extension = '.asc'

    result = paths.output(input_file, input_path, output_path, change = False, output_extension = extension)

    assert result == output_file