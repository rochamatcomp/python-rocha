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

def output(input_file, input_path, output_path, change = True, extra = None, begin = False, output_extension = None):
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
    output_extension : str
        Output file extension.
    """
    name, input_extension = os.path.splitext(input_file)
    dirname, basename = os.path.split(name)

    extension = output_extension if output_extension else input_extension

    if extra is None:
        filename = f'{basename}{extension}'
    else:
        if begin:
            filename = f'{extra}{basename}{extension}'
        else:
            filename = f'{basename}{extra}{extension}'

    if change:
        output_file = os.sep.join([output_path, filename])
    else:
        root = dirname.replace(input_path, output_path)
        output_file = os.sep.join([root, filename])

    return output_file