"""KiCad Release Dates

Author:
    (C) Uli Bartels - @ulibartels - 2026

License identifier:
    GPL-3.0

Major changes:
    14.06.2026 - created
"""

# Version numbers can be used to test whether a schematic file was created using a specific KiCAD release (file version == KICAD_n_VERSION), whether it was created using an earlier version (file version < KICAD_n_VERSION) or a later version (file version > KICAD_n_VERSION). This way kiutils output can be configured to generate valid files for a specific version of KiCAD.

# Version can be looked up at: https://gitlab.com/kicad/code/kicad/-/blob/master/eeschema/sch_file_versions.h
KICAD_8_VERSION_NUMBER = 20231120
KICAD_9_VERSION_NUMBER = 20241209