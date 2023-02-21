# kiutils - CHANGELOG

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
           `KIUTILS_CREATE_NEW_VERSION_STR`

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
- Changed: `uuid` token in class `kiutils.schematic.Schematic()` is now optional - (PR #26)
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