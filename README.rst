========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations| |
.. |docs| image:: https://readthedocs.org/projects/pybpod-gui-plugin-emulator/badge/?style=flat
    :target: https://readthedocs.org/projects/pybpod-gui-plugin-emulator
    :alt: Documentation Status

.. |version| image:: https://img.shields.io/pypi/v/pybpod-gui-plugin-emulator.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/pybpod-gui-plugin-emulator

.. |wheel| image:: https://img.shields.io/pypi/wheel/pybpod-gui-plugin-emulator.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/pybpod-gui-plugin-emulator

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/pybpod-gui-plugin-emulator.svg
    :alt: Supported versions
    :target: https://pypi.org/project/pybpod-gui-plugin-emulator

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/pybpod-gui-plugin-emulator.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/pybpod-gui-plugin-emulator


.. end-badges

Emulator for PyBpod to work with the Bpod's State Machine ports.

* Free software: MIT license

Installation
============

::

    pip install pybpod-gui-plugin-emulator

Documentation
=============


https://pybpod-gui-plugin-emulator.readthedocs.io/


Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
