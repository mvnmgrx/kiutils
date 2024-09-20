# kiutils - CHANGELOG

## v1.4.9 - 10.09.2024
- Fixed: support for KiCad 8: Updated handling to accommodate renaming of `tstamp` to `uuid`.
- Added: Net name association for GrPoly in graphic items on the board.

## v1.4.8 - 03.02.2024

### Non-breaking changes
- Fixed: Missing parenthesis for gr_curve items (PR #110)
- Fixed: Text `knockout` setting not parsed (PR #111)

## v1.4.7 - 23.10.2023

### Non-breaking changes
- Fixed: No quotes for DRC rules "severity" token (PR #108)

## v1.4.6 - 23.10.2023

### Non-breaking changes
- Added: Parsing of schematic sheet file properties (PR #106)

## v1.4.5 - 04.10.2023

### Non-breaking changes
- Added: Parsing of footprint `net_tie_pad_groups` token (PR #105)

## v1.4.4 - 17.08.2023

### Non-breaking changes
- Added: Parsing of footprint `private_layers` token (PR #103)
- Added: Parsing of 3d-model `opacity` token (PR #98)
- Added: Parsing of footprint attribute's `allow_missing_courtyard` token (PR #101)
- Fixed: Legacy footprints with only digits as name are now correctly parsed (PR #91)

## v1.4.3 - 15.07.2023

### Non-breaking changes
- Fixed: 3D model `hide` property not parsed (PR #97)

## v1.4.2 - 09.06.2023

### Non-breaking changes
- Added: Support for `bus_alias` tokens (PR #92)

## v1.4.1 - 22.04.2023

### Non-breaking changes
- Fixed: Zones on only outer layers produce wrong S-Expression for the `layer` token (PR #89)

## v1.4.0 - 27.03.2023
This release adds initial KiCad v7 support.

### Breaking changes
- Changed: Removed `SyFill` in favour of `Fill` tokens everywhere - (PR #76)

### Non-breaking changes
- Added: Parsing new sheet names - (PR #59)
- Added: `Arc`, `Rectangle` and `Circle` tokens - (PR #76)
- Added: `Schematic.shapes` to hold arcs, rectangles and circles - (PR #76)
- Added: `GrTextBox`, `FpTextBox`, `SyTextBox` and `TextBox` tokens - (PR #76)
- Added: `SchematicSymbol.dnp` token - (PR #77)
- Added: `fields_autoplaced` token to all kinds of lables - (PR #77)
- Added: `NetclassFlag` token - (PR #80)
- Added: `Property.showName` token - (PR #80)
- Added: `Rule.severity` token for design rules - (PR #84)
- Added: `plotOnAllLayersSelection`, `dashedLineDashRatio` and `dashedLineGapRatio` tokens 
         in `PlotSettings` - (PR #85)
- Added: `RenderCache` token for supported text items - (PR #87)
- Added: `ProjectInstance` tokens for schematic symbols and hierarchical sheets - (PR #88)
- Changed: Strokes are now parsed less strictly - (PR #57)
- Changed: Default value of `Stroke.type` from "dash" to "default" - (PR #63)
- Changed: `Stroke.color` is now optional - (PR #63)
- Changed: `Stroke.type` is now optional - (PR #82)
- Changed: `Schematic.tstamp` is now optional - (PR #63)
- Changed: `Property.id` is now optional - (PR #78)
- Changed: `SymbolPin.nameEffects` and `SymbolPin.numberEffects` are now optional - (PR #82)
- Changed: `PlotSettings.svgUseInch` and `PlotSettings.excludeEdgeLayer` are now optional - (PR #85)
- Fixed: Regex parser not correctly handling backslashes in quoted strings - (PR #82)
- Fixed: `DesignRules.from_sexpr()` not parsing version token - (PR #84)

## v1.3.0 - 21.02.2023
### Breaking changes
- Changed: The ID token API was consolidated - (PR #54)
  - `SchematicSymbol`: `self.libraryIdentifier` renamed to `self.libId`
  - `Symbol`: `self.id` renamed to `self.libId`
  - `Footprint`: `self.libraryLink` renamed to `self.libId`
  - Setting and getting `self.libId` will update some subtokens of these classes. Check the documentation
    for more information on this.
- Changed: `Footprint.create_new()`'s parameter `library_link` renamed to `library_id` - (PR #54)
- Changed: `SymbolLib.version` is now a non-optional token that defaults to the config entry
           `KIUTILS_CREATE_NEW_VERSION_STR` - (PR #55)

### Non-breaking changes
- Added: API for lib_name token in `SchematicSymbol` called `self.libName` - (PR #54)
- Added: Tokens `self.entryName` and `self.libraryNickname` for classes `Symbol`, `SchematicSymbol`
         and `Footprint`. These tokens are part of the `libId` token and will be changed when setting 
         it. - (PR #41)
- Added Tokens `self.unitId` and `self.styleId` for `Symbol` class. These tokens are part of the 
        `libId` token and will be changed when setting it. - (PR #41)
- Added: All `from_file` and `to_file` methods got a new optional parameter `encoding` to change 
         the default encoding when reading/writing files. - (PR #50)
- Added: New `active` token in `LibTable` class - (PR #51)
- Added: CONTRIBUTING.md - (PR #52)
- Added: Missing `filePath` attribute in `DesignRules` class - (PR #45)
- Fixed: Return type of `LibTable.create_new()` - (PR #45)
- Fixed: `Position.to_sexpr()` having no parameters - (PR #45)
- Changed: Most parts of the docu were refactored - (PR #45)
- Removed: Unused `size` token in class `Connection()` - (PR #45)
- Removed: Unused `stroke` token in class `Image()` - (PR #45)
- Removed: Some tokens that were defined twice - (PR #45)

## v1.2.1 - 21.11.2022
- Fixed: Broken package config did not included every source file while building the module - (PR #38) 

## v1.2.0 - 20.11.2022
- Added: Support for Python 3.11 on all platforms
- Added: `create_new()` API for all classes that serve files (schematic, board, etc) - (PR #33)
- Added: Checked `self.stroke` to be None in all `FpItems` classes when generating its S-Expression - (PR #36)
- Fixed: Default values of mutable class members are now set correctly using a dataclass field with 
         a default_factory to ensure unique references for each new class object - (PR #35)
- Fixed: Made VSCode automatic test discovery work - (PR #34)
- Changed: Documentation on `Jusitfy.to_sexpr()`s return value - (PR #37)

## v1.1.4 - 10.09.2022
- Added: Support for older Python versions (v3.7 to v3.10 are now supported) - (PR #30)
- Added: Automatic test report generation in test framework - (PR #21)
- Added: Sphinx-compatible documentation in `docs/` folder and on 
         [https://kiutils.readthedocs.io](https://kiutils.readthedocs.io) - (PR #29)
- Changed: Replaced relative imports with absolute imports in the module structure - (PR #24)
- Changed: Migrated test framework to Python's `unittest` - (PR #21)
- Changed: `unit` token in class `kiutils.items.schitems.SchematicSymbol()` is now optional - (PR #26)
- Changed: `tstamp` token in class `kiutils.schematic.Schematic()` is now optional - (PR #26)
- Changed: Order of how newlines are generated in `kiutils.schematic.Schematic().to_sexpr()` - (PR #26)
- Fixed: `angle` set to 0.0 (was `None`) when creating a new `kiutils.items.common.Property()` object (PR #27, fixes #19)
- Fixed: Footprint attributes object (`kiutils.footprint.Attributes()`) missing when certain 
         "Manufacturing Attributes" are set - (PR #28)

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