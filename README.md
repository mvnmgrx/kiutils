# KiUtils

[![PyPI version](https://img.shields.io/pypi/v/kiutils)](https://pypi.org/project/kiutils)
![Python version](https://img.shields.io/pypi/pyversions/kiutils)
[![License](https://img.shields.io/github/license/mvnmgrx/kiutils)](https://github.com/mvnmgrx/kiutils/blob/master/LICENSE)
![Last commit](https://img.shields.io/github/last-commit/mvnmgrx/kiutils)
[![Documentation Status](https://readthedocs.org/projects/kiutils/badge/?version=latest)](https://kiutils.readthedocs.io/en/latest/?badge=latest)

Simple and SCM-friendly KiCad file parser based on Python dataclasses for KiCad 6.0
and up. The following KiCad-related files are currently supported:
- `.kicad_pcb` - Board layouts
- `.kicad_sch` - Schematics
- `.kicad_mod` - Footprints
- `.kicad_sym` - Symbols and symbol libraries
- `.kicad_wks` - Worksheets
- `.kicad_dru` - Custom design rules
- `fp-lib-table` & `sym-lib-table` - Library tables

KiUtils implements a "pythonic" abstraction of the documentation found at the
[KiCad Developer Reference](https://dev-docs.kicad.org/en/file-formats/) and is
intended to work with an SCM like Git or SVN without breaking the layout of the
files when the Python script ran.

Parsing of the files is based on the S-Expression parser found in this library:
[GitLab: KiCad Library utilities](https://gitlab.com/kicad/libraries/kicad-library-utils)

## Prerequisites
The following is required to use `kiutils`:
- Python 3.7 or higher

## Installation
KiUtils is available on [PyPI](https://pypi.org/project/kiutils/). Use Python's `pip`
to install it:
```
pip install kiutils
```

## Documentation
Visit the [kiutils documentation](https://kiutils.readthedocs.io/) for more information on how to 
install, use and develop `kiutils`, as well as examples and general module documentation.

## Donate
If you found this module helpful for your project consider donating via
[PayPal](https://paypal.me/mrvnmgr). Thanks!