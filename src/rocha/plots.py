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
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

from . import extremes

def maps(rasters, rows, cols, color, title, subtitles, labels, band = 1, figsize = (12, 12)):
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
    band : int
        Raster band.
    figsize : tuple of int
        Figure size as (width, height) in inches.
    """
    figure, axes = plt.subplots(rows, cols, sharex = True, sharey = True, figsize = figsize)

    # Normalize scale color with the global minimum and maximun rasters values.
    value_min, value_max = extremes.min_max(rasters, band)
    bounds = np.linspace(value_min, value_max, num = 11)
    norm = mpl.colors.BoundaryNorm(boundaries = bounds, ncolors = 256)

    for subplot, raster in enumerate(rasters):
        with rasterio.open(raster) as source:
            dataset = source.read(band, masked = True)

        # Axis to the subplot.
        row = subplot // cols
        col = subplot % cols
        axis = axes[row, col]

        image = axis.imshow(dataset, cmap = color, norm = norm)

    # Colorbar axis position and size by list [left, bottom, width, height].
    colorbar_axis = figure.add_axes([0.20, 0.05, 0.60, 0.02])
    figure.colorbar(image, cax = colorbar_axis, extend = 'both', orientation = 'horizontal')

    configuration(figure, axes, title, subtitles, labels)


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
        # Subplot coordinate axis label just the first column
        axis.set_ylabel(label, size='large', fontweight = 'bold')