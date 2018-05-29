# -*- coding: utf-8 -*-
"""
:package:`rocha` -- Raster and vector manipulation
==================================================

.. package:: rocha
    :platform: Unix, Windows
    :synopsis:
.. packageauthor::
"""

import setuptools

def readme():
    with open('README.md') as source:
        return source.read()

setuptools.setup(name='rocha',
    version='0.1',
    description='Raster and vector manipulation.',
    long_description='Manipulation of the raster datasets and vector geometries.',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering :: GIS'
    ],
    keywords='funniest joke comedy flying circus',
    url='https://github.com/rochamatcomp/python-rocha',
    author='Andre Rocha',
    author_email='<rocha.matcomp@gmail.com>',
    license='MIT',
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
    include_package_data=True,
    install_requires=[
        'rasterio',
        'fiona'
    ],
    zip_safe=False)