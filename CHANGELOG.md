# kiutils - CHANGELOG

## v1.1.2 - xx.xx.xxxx
- Added: Support for track arcs at `kiutils.items.brditems.Arc()`

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