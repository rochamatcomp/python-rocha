# -*- coding: utf-8 -*-
"""
:mod:`crop` -- Tests raster and vector crop
===========================================

.. module:: crop
    :platform: Unix, Windows
    :synopsis: Tests of the crop the raster datasets by vector geometries.
.. moduleauthor:: Andre Rocha <rocha.matcomp@gmail.com>
"""

import src.rocha.crop as crop

def test_column_string():
    """
    Test vector property as string.
    """
    vector = "data/regions.shp"
    column = "REGION"
    names = ["mid-west", "northeast", "southeast", "south"]

    properties = crop.prop(vector, column)

    for name in properties:
        if isinstance(name, str):
            assert name.lower() in names
        else:
            message = f'The vector property should be str, but is {type(name)}'
            raise AssertionError(message)

def test_column_number():
    """
    Test vector property as number.
    """
    vector = "data/regions.shp"
    column = "ID"
    codes = [5, 2, 4, 3]

    properties = crop.prop(vector, column)

    for code in properties:
        if isinstance(code, (int, float)):
            assert code in codes
        else:
            message = f'The vector property should be int or float, but is {type(code)}'
            raise AssertionError(message)