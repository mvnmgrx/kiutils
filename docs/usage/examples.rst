Examples
========

These examples show how the module is intended to be used.

Loading and saving a board
--------------------------

.. code-block:: python

   from kiutils.board import Board

   board = Board().from_file("path/to/board.kicad_pcb")

   # Do stuff ...

   board.to_file()


Changing title and revision in schematic
----------------------------------------

.. code-block:: python

   from kiutils.schematic import Schematic

   schematic = Schematic().from_file("path/to/schematic.kicad_sch")
   schematic.titleBlock.title = "This is schematic xyz"
   schematic.titleBlock.revision = "B"
   schematic.to_file()

Loading and adding footprint to board
-------------------------------------

Here a footprint is loaded from a `.kicad_mod` file and added to a board:

.. code-block:: python

   from kiutils.board import Board
   from kiutils.footprint import Footprint
   from kiutils.items.common import Position
   from kiutils.items.fpitems import FpText

   from os import path

   # Get current working directory
   tests_path = path.join(path.dirname(path.realpath(__file__)), 'tests')

   # Load board file and footprint file
   board = Board().from_file(path.join(tests_path, "example-project/example/example.kicad_pcb"))
   footprint = Footprint().from_file(path.join(tests_path, "example-project/example/C_0805.kicad_mod"))

   # Set new footprint's position
   footprint.position = Position(X=127.0, Y=85.0)

   # Change identifier to C105
   for item in footprint.graphicItems:
       if isinstance(item, FpText):
           if item.type == 'reference':
               item.text = "C105"

   # Append footprint to board and save board
   board.footprints.append(footprint)
   board.to_file()

Adding vias to board
--------------------

This example adds two vias on the normal axis at the end of each segment:

.. code-block:: python

   from cmath import sqrt
   from kiutils.board import Board
   from kiutils.items.brditems import Via, Segment
   from kiutils.items.common import Position

   from os import path

   # Get current working directory
   tests_path = path.join(path.dirname(path.realpath(__file__)), 'tests')

   # Load board file
   board = Board().from_file(path.join(tests_path, "example-project/example/example.kicad_pcb"))

   # Iterate through segments, arcs and vias ..
   for item in board.traceItems:
       if isinstance(item, Segment):
           # Calculate normal on end point of segment
           nvec = Position(-(item.end.Y - item.start.Y), item.end.X - item.start.X)
           nvec_inverse_len = 1/sqrt(nvec.X**2 + nvec.Y**2).real
           unit_normal = Position(nvec_inverse_len * nvec.X, nvec_inverse_len * nvec.Y)

           # Compute positions of new vias
           next_via_1 = Position(item.end.X + (unit_normal.X * 2), item.end.Y + (unit_normal.Y * 2))
           next_via_2 = Position(item.end.X - (unit_normal.X * 2), item.end.Y - (unit_normal.Y * 2))

           # Append vias to trace items list of board
           board.traceItems.append(Via(position=next_via_1, layers=["F.Cu", "B.Cu"], size=1.0, drill=0.6))
           board.traceItems.append(Via(position=next_via_2, layers=["F.Cu", "B.Cu"], size=1.0, drill=0.6))

   # Write changes back to board file
   board.to_file()
