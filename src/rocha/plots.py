# -*- coding: utf-8 -*-
"""
:mod:`plots` -- Raster and vector plots
=======================================

.. module:: plots
    :platform: Unix, Windows
    :synopsis: Plots the raster datasets and the vector geometries.
.. moduleauthor:: Andre Rocha <rocha.matcomp@gmail.com>
"""
import rasterio
from rasterio.plot import show
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

from . import extremes

def maps(rasters, rows, cols, title, subtitles, labels, color, bar, band = 1, figsize = (12, 12)):
    """
    Plot the rasters files as image maps.

    Parameters
    ----------
    rasters : list of str
        Raster filenames.
    rows : int
        Rows quantity.
    cols : int
        Columns quantity.
    title : str
        Figure title.
    subtitles : list of str
        Subplot subtitles in the first row.
    labels : list of str
        Coordinate axis labels in the first column.
    color : str
        Color name.
    band : int
        Raster band.
    figsize : tuple of int
        Figure size as (width, height) in inches.
    color : :class:`matplotlib.colors.Colormap` object

    bar : str
        Colorbar position as `last`, `all` or `global`

    Returns
    -------
    figure : :class:`matplotlib.figure.Figure` object.
    """
    figure, axes = plt.subplots(rows, cols, sharex = True, sharey = True, figsize = figsize)

    # Normalize scale color with the global minimum and maximun rasters values.
    value_min, value_max = extremes.min_max(rasters, band)
    bounds = np.linspace(value_min, value_max, num = 11)
    norm = mpl.colors.BoundaryNorm(boundaries = bounds, ncolors = 256)

    for subplot, raster in enumerate(rasters):
        with rasterio.open(raster) as source:
            # Axis to the subplot.
            row = subplot // cols
            col = subplot % cols
            axis = axes[row, col]

            show(source, ax = axis, cmap = color, norm = norm)

    colorbar(figure, axes, bar)
    configuration(figure, axes, title, subtitles, labels)

    return figure


def colorbar(figure, axes, bar):
    """
    Colorbar whose height or width in sync with the master axes.

    Parameters
    ----------
    figure : :class:`matplotlib.figure.Figure` object.

    axis : :class:`matplotlib.axes.Axes` object.

    bar : str
        Colorbar position as `last`, `all` or `global`
    """
    if bar == 'last':
        for axis in axes[:, -1]:
            # Subplot colorbar just for the last column
            images = axis.images

            if len(images) > 0:
                figure.colorbar(images[0], ax = axis, extend = 'both', orientation = 'vertical')
    elif bar == 'all':
        for row in axes:
            for axis in row:
                images = axis.images

                if len(images) > 0:
                    figure.colorbar(images[0], ax = axis, extend = 'both', orientation = 'vertical')
    elif bar == 'global':
        # Colorbar axis position and size by list [left, bottom, width, height]
        colorbar_axis = figure.add_axes([0.20, 0.05, 0.60, 0.02])

        if len(axes) > 0 and len(axes[0]) > 0:
            # Color and scale references from first image
            axis = axes[0][0]
            images = axis.images

            if len(images) > 0:
                figure.colorbar(images[0], cax = colorbar_axis, extend = 'both', orientation = 'horizontal')
    else:
        print('Warning: colorbar reference must be last, all or global.')

def configuration(figure, axes, title, subtitles, labels):
    """
    Configuration of the text elements to the figure and axes.

    Parameters
    ----------
    figure : :class:`matplotlib.figure.Figure` object.

    axes : array of Axes objects.
        Axes object is a :class:`matplotlib.axes.Axes` object.
    title : str
        Figure title.
    subtitles : list of str
        Subplot subtitles in the first row.
    labels : list of str
        Coordinate axis labels in the first column.
    """
    figure.suptitle(title, fontsize = 16)

    for axis, subtitle in zip(axes[0, :], subtitles):
        # Subplot title just for the first row
        axis.set_title(subtitle, fontweight = 'bold')

    for axis, label in zip(axes[:, 0], labels):
        # Subplot coordinate axis label just for the first column
        axis.set_ylabel(label, size='large', fontweight = 'bold')