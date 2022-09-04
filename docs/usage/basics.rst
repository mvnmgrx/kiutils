Basics
======

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

- ``from_file(..)``: Initialize the object with data found in given file
- ``to_file(..)``: Generate KiCad S-Expression that describes the object and write it to the given file

The files in the root directory are intended to be used in a Python script as they contain the main 
functionality of the module. Documentation can be found in the source files itself. Use VSCode for 
development as it shows docstring documentation by default when hovering over functions and members 
of the module.