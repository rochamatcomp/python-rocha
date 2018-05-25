# rocha
``rocha`` is a Python module for manipulate geospatial raster datasets based on vector geometries.

conda create --help

conda create --name rocha --channel conda-forge python --yes
conda create -n rocha -c conda-forge python -y

### Environment by file
conda create --name rocha --channel conda-forge --file environment.yml --yes

### Adding channel
conda config --add channels conda-forge

The following NEW packages will be INSTALLED:

    ca-certificates
    certifi
    ncurses
    openssl
    pip
    python
    readline
    setuptools
    sqlite
    tk
    wheel
    xz
    zlib

To activate this environment, use

    $ conda activate rocha

To deactivate an active environment, use

    $ conda deactivate


# Glossary
`$`
    The default command prompt of the shell, for normal user.

`#`
    The default command prompt of the shell, for root user.

`>>>`
    The default Python prompt of the interactive shell. Often seen for code examples which can be executed interactively in the interpreter.

`...`
    The default Python prompt of the interactive shell when entering code for an indented code block or within a pair of matching left and right delimiters (parentheses square brackets or curly braces).