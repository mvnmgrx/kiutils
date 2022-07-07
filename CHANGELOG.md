# kiutils - CHANGELOG

## v1.1.3 - 07.07.2022
- Fixed: Stacked dielectrics in PCB layer stack are now parsed correctly as `StackupSubLayer` item

## v1.1.2 - 30.06.2022
- Added: Support for track arcs at `kiutils.items.brditems.Arc()`
- Fixed: Redundant line break in a footprint's pad section with a schematic symbol assigned (aka 
         net, pinfunction or pintype token set) as well as at least the solder_paste_margin_ratio 
         token set 

## v1.1.1 - 27.06.2022
- Added: Support for custom design rules (`.kicad_dru`)
- Added: Support for custom worksheets (`.kicad_wks`)

## v1.1.0 - 16.06.2022
- Added: Support for Python Package Index (PyPI)
- Changed: Source directory for development moved from `kiutils/` to `src/kiutils/`

## v1.0.1 - 15.06.2022
- Added: Dimension, DimensionStyle, DimensionFormat classes for dimensions (measurements in PCB)
- Added: Target class for board target markers
- Added: Support for dimensions and target markers in Board class
- Added: Prerequisites in docu
- Fixed: Correct parsing of footprints with empty `attr` field (see #2)
- Fixed: Quoted strings funcion now handles integers that may be parsed from older KiCad versions 
         correctly (see #3)
- Fixed: Symbol pin's `alternate` field was missing and is now parsed correctly (see #4)
- Fixed: Footprint `libraryLink` attribute was missing (see #5)

## v1.0.0 - 19.03.2022
- Initial version