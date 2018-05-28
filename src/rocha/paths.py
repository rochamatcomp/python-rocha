# -*- coding: utf-8 -*-
"""
:mod:`paths` -- Paths manipulation
==================================

.. module:: paths
    :platform: Unix, Windows
    :synopsis: Paths manipulation and files discovery.
.. moduleauthor:: Andre Rocha <rocha.matcomp@gmail.com>
"""
import os
import fnmatch

def find(path, pattern, relative = True):
    """
    Path from the files like pattern.

    Parameters
    ----------
    path : str
        Pathname root.
    pattern : str
        Pattern like unix shell-style wildcards.
    relative : bool
        Absolute or relative path. False: absolute path, True: relative path.

    Yields
    ------
    list of str
        List of file path.
    """
    for (root, _, files) in os.walk(path):
        for name in fnmatch.filter(files, pattern):
            if relative:
                yield os.sep.join([root, name])
            else:
                yield os.path.abspath(os.sep.join([root, name]))

def output(input_file, input_path, output_path, change = True, extra = None, begin = False):
    """
    Output filename from input filename.

    Parameters
    ----------
    input_file : str
        Input filename
    input_path : str
        Path from input file
    output_path : str
        Path to output file
    change : bool
        Change the directory structure.

        False: the same directory structure as input filename.
        True: change the directory structure, output path as root path (default).
    extra : str
        Extra name.
    begin : bool
        Add the extra name in the beginning of the output filename.

        False: extra name in the ending (default).
        True: extra name in the beginning.
    """
    if extra is None:
        filename = input_file
    else:
        name, extension = os.path.splitext(os.path.basename(input_file))

        if begin:
            filename = f'{extra}{name}{extension}'
        else:
            filename = f'{name}{extra}{extension}'

    if change:
        output_file = os.sep.join([output_path, os.path.basename(filename)])
    else:
        output_file = filename.replace(input_path, output_path)

    return output_file