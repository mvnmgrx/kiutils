Getting started
===============

The most relevant classes can be imported like this:

.. code-block:: python

   from kiutils.board import Board
   from kiutils.libraries import LibTable
   from kiutils.schematic import Schematic
   from kiutils.footprint import Footprint
   from kiutils.symbol import SymbolLib
   from kiutils.wks import WorkSheet
   from kiutils.dru import DesignRules

Every class has at at least the following functions:

- ``to_sexpr(..)``: Generate KiCad S-Expression that describes the object
- ``from_sexpr(..)``: Initialize the object with data found in given S-Expression. Wrong S-Expression
  supplied yields an exception.

If the class is intended to access files (such as board files, schematics, libraries, etc.), the
following functions are available:

- ``create_new(..)``: Creates a new object with its members populated in a similar way as KiCad would do it
- ``from_file(..)``: Creates a new object and initializes it with data found in given file
- ``to_file(..)``: Generate KiCad S-Expression that describes the object and write it to the given file

The files in the root directory are intended to be used in a Python script as they contain the main
functionality of the module. Documentation can be found in the source files itself. Use VSCode for
development as it shows docstring documentation by default when hovering over functions and members
of the module.

Simple examples
---------------

These examples use the ``Board()`` class as an example. The procedure is the same for all file-serving
classes in ``kiutils``.

Create a new object and dump it to a file that KiCad can use (be sure to get the file extension
correctly! (``.kicad_pcb`` in this case)):

.. code-block:: python

   from kiutils.board import Board

   board = Board.create_new()
   # Do stuff ..
   board.to_file('/my/fancy/project/title.kicad_pcb')

Parse an already existing object, do some changes and reexport it:

.. code-block:: python

   from kiutils.board import Board

   board = Board.from_file('/my/fancy/project/title.kicad_pcb')
   # Do stuff ..
   board.to_file()

Note that the latter example omitted the path when calling ``to_file()``. The file path used when
opening the original file will be used in this case. It is still possible to change the export
path to somewhere different.

Check the :doc:`examples` section for other stuff that can be done with ``kiutils``!