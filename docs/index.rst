.. kiutils documentation master file, created by
   sphinx-quickstart on Sun Sep  4 18:35:39 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to kiutils's documentation!
===================================

This is the documentation to the ``kiutils`` python module for parsing files of the KiCad EDA.

- View on Github: `mvnmgrx/kiutils <https://github.com/mvnmgrx/kiutils>`_

``kiutils`` is simple and SCM-friendly KiCad file parser based on Python dataclasses for KiCad 6.0
and up. 

It implements a "pythonic" abstraction of the documentation found at the
`KiCad Developer Reference <https://dev-docs.kicad.org/en/file-formats/>`_ and is intended to work 
with an SCM like Git or SVN without breaking the layout of the files when the Python script ran.

.. toctree::
   :maxdepth: 2
   :caption: Usage

   usage/installation
   usage/getting-started
   usage/examples
   usage/development

.. toctree::
   :maxdepth: 2
   :caption: Misc

   misc/known-issues

.. toctree::
   :maxdepth: 2
   :caption: Module documentation

   module/kiutils
   module/kiutils.items
   module/kiutils.utils
   module/kiutils.misc



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
