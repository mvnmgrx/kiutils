# KiUtils

[![PyPI version](https://img.shields.io/pypi/v/kiutils)](https://pypi.org/project/kiutils)
![Python version](https://img.shields.io/pypi/pyversions/kiutils)
[![License](https://img.shields.io/github/license/mvnmgrx/kiutils)](https://github.com/mvnmgrx/kiutils/blob/master/LICENSE)
![Last commit](https://img.shields.io/github/last-commit/mvnmgrx/kiutils)

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
- Python 3.10 or higher

## Installation and Usage
KiUtils is available on [PyPI](https://pypi.org/project/kiutils/). Use Python's `pip`
to install it:
```
pip install kiutils
```

The most relevant classes can then be imported like this:
```python
from kiutils.board import Board
from kiutils.libraries import LibTable
from kiutils.schematic import Schematic
from kiutils.footprint import Footprint
from kiutils.symbol import SymbolLib
from kiutils.wks import WorkSheet
from kiutils.dru import DesignRules
```
Check the [Structure]() section on all importable classes or the [Examples]() section for code snippets.

## Structure
The module features the following classes:
```python
+ kiutils/
  + items/
  | + brditems.py
  | | - GeneralSettings()   # General information about a board
  | | - LayerToken()        # Intermediate type for layers in a board
  | | - StackupLayer()      # Setting of a single layer in the stack up
  | | - Stackup()           # Board stack up settings
  | | - PlotSettings()      # Plotting and printing setting
  | | - SetupData()         # Current settings used by a board
  | | - Segment()           # Track segment on a board
  | | - Arc()               # Arc on a board
  | | - Via()               # Via on a board
  | | - Target()            # Target markers
  | |
  | + common.py
  | | - Position()          # Position and rotation of an object
  | | - Coordinate()        # Three-dimentional position
  | | - ColorRGBA()         # RGBA Color
  | | - Stroke()            # Outline of graphical objects
  | | - Font()              # Font that defines how text is shown
  | | - Justify()           # Justification of a text object
  | | - Effects()           # Effects that define how a text is displayed
  | | - Net()               # Number and name of a net
  | | - Group()             # Group of items
  | | - PageSettings()      # Page size and orientation
  | | - TitleBlock()        # Contents of a page's title block
  | | - Property()          # Key-value property
  | |
  | + dimensions.py
  | | - DimensionFormat()   # Text format of a dimension
  | | - DimensionStyle()    # Graphical style of a dimension
  | | - Dimension()         # A dimension in the board
  | |
  | + fpitems.py
  | | - FpText()            # Text in a footprint
  | | - FpTextBox()         # Text box in a footprint
  | | - FpLine()            # Line in a footprint
  | | - FpRect()            # Rectangle in a footprint
  | | - FpCircle()          # Circle in a footprint
  | | - FpArc()             # Arc in a footprint
  | | - FpPoly()            # Polygon in a footprint
  | | - FpCurve()           # Curve in a footprint
  | |
  | + gritems.py
  | | - GrText()            # Text graphical item
  | | - GrTextBox()         # Text box graphical item
  | | - GrLine()            # Line graphical item
  | | - GrRect()            # Rectangle graphical item
  | | - GrCircle()          # Circle graphical item
  | | - GrArc()             # Arc graphical item
  | | - GrPoly()            # Polygon graphical item
  | | - GrCurve()           # Curve graphical item
  | |
  | + schitems.py
  | | - Junction()          # Junction (connection) between two lines
  | | - NoConnect()         # No connect symbol
  | | - BusEntry()          # Entry to a bus section
  | | - Connection()        # Defines wires or busses in a schematic
  | | - Image()             # Base64 encoded image
  | | - PolyLine()          # Line with multiple nodes
  | | - Text()              # Text in a schematic
  | | - LocalLabel()        # Local track label
  | | - GlobalLabel()       # Global track label
  | | - HierarchicalLabel() # Hierarchical track label
  | | - SchematicSymbol()   # Symbol embedded into schematic
  | | - HierarchicalPin()   # Hierarchical pin
  | | - HierarchicalSheet() # Hierarchical sheet definition
  | | - HierarchicalSheetInstance() # Hierarchical sheet instance
  | | - SymbolInstance()    # Instance of an embedded symbol
  | |
  | + syitems.py
  | | - SyFill()            # Filled zone in a symbol
  | | - SyArc()             # Arc in a symbol
  | | - SyCircle()          # Circle in a symbol
  | | - SyCurve()           # Curve in a symbol
  | | - SyPolyLine()        # Line with multiple nodes in a symbol
  | | - SyRect()            # Rectangle in a symbol
  | | - SyText()            # Text in a symbol
  | |
  | + zones.py
  |   - KeepoutSettings()   # Keep out zone settings
  |   - FillSettings()      # Settings on how a zone is filled
  |   - ZonePolygon()       # List of coordinates that define part of a zone
  |   - FilledPolygon()     # Polygons used to fill a zone
  |   - FillSegments()      # Segments used to fill a zone (KiCad 4 stuff..)
  |   - Hatch()             # Zone hatching settings
  |   - Zone()              # A zone in a board or in a footprint
  |
  + board.py
  | - Board()               # Board files (.kicad_pcb)
  |
  + footprint.py
  | - Attributes()          # List of attributes of a footprint
  | - Model()               # 3D Model
  | - DrillDefinition()     # Drill mark of a footprint pad
  | - PadOptions()          # Settings for custom pads
  | - Pad()                 # A footprint pad
  | - Footprint()           # Footprint files (.kicad_mod)
  |
  + libraries.py
  | - Library()             # Library table entry
  | - LibTable()            # Library table file (fp-lib-table or sym-lib-table)
  |
  + schematic.py
  | - Schematic()           # Schematic files (.kicad_sch)
  |
  + symbol.py
  | - SymbolPin()           # Pin in a symbol
  | - Symbol()              # Symbol itself
  | - SymbolLib()           # Symbol library file (.kicad_sym)
  |
  + wks.py
  | - WksFontSize()         # Font size of worksheet texts
  | - WksFont()             # Font properties of worksheet texts
  | - WksPosition()         # Item positions on worksheets
  | - Line()                # Lines on worksheets
  | - Rect()                # Rectangles on worksheets
  | - Polygon()             # Polys (Not implemented as the GUI does not support this)
  | - Bitmap()              # Image in a worksheet
  | - TbText()              # Title bock text on a worksheet
  | - TextSize()            # Standard text size on a worksheet
  | - Setup()               # Worksheet configuration infos
  | - WorkSheet()           # The worksheet file (.kicad_wks)
  |
  + dru.py
    - Constraint()          # A constraint of a design rule
    - Rule()                # A single design rule itself
    - DesignRules()         # The custom design rules file (.kicad_dru)
```

Every class has at at least the following functions:
- `to_sexpr(..)`: Generate KiCad S-Expression that describes the object
- `from_sexpr(..)`: Initialize the object with data found in given S-Expression.
  Wrong S-Expression supplied yields an exception.

If the class is intended to access files (such as board files, schematics,
libraries, etc.), the following functions are available:
- `from_file(..)`: Initialize the object with data found in given file
- `to_file(..)`: Generate KiCad S-Expression that describes the object and
  write it to the given file

The files in the root directory are intended to be used in a Python script
as they contain the main functionality of the module. Documentation can be found
in the source files itself. Use VSCode for development as it shows docstring
documentation by default when hovering over functions and members of the
module.

## Known Issues
- **Footprint:** Whitespaces in the items section do sometimes not correspond
  correctly to those generated by KiCad. This will be picked up by an SCM as a
  change even though no changes were initially made. This seems to be a bug in
  KiCad itself, as it sometimes sets the whitespaces before those tokens
  correctly and sometimes not.
- **Schematic:** Sometimes KiCad inserts blank lines between wires, bus entries
  and polylines which are not picked up by the parser. Same problem as above
  with SCMs.
- **Backwards compatibility:** KiCad <6 file formats can be parsed, but will
  be converted to KiCad 6 style S-Expression upon saving. It was observed that
  e.g. footprints of an older version will experience conversion errors in some
  features that KiCad 6 now handles differently (see `fp_arc` as an example).
  It is in the user's hands to decide on how to deal with this, but support
  for converting correctly to KiCad 6 formats may be added in the future.
  Please create an issue with a snippet of what you are trying to parse when
  stumbling upon such a situation.
- **Design rules:** Support for custom design rules was implemented without a 
  proper documentation. Thus it might be subject to bugs or changes. It 
  furthermore may not exactly place the items associated with a custom design 
  rule (constraints, layers, etc) in the same order as the user once put them 
  when parsing and writing back `.kicad_dru` files

## Examples
These examples show how the module is intended to be used.

### Loading and saving a board
```python
from kiutils.board import Board

board = Board().from_file("path/to/board.kicad_pcb")

# Do stuff ...

board.to_file()
```

### Changing title and revision in schematic
```python
from kiutils.schematic import Schematic

schematic = Schematic().from_file("path/to/schematic.kicad_sch")
schematic.titleBlock.title = "This is schematic xyz"
schematic.titleBlock.revision = "B"
schematic.to_file()
```

### Loading and adding footprint to board
Here a footprint is loaded from a `.kicad_mod` file and added to a board:
```python
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
```

### Adding vias to board
This example adds two vias on the normal axis at the end of each segment:
```python
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
```

## Donate
If you found this module helpful for your project consider donating via
[PayPal](https://paypal.me/mrvnmgr). Thanks!