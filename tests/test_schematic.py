"""Unittests of schematic related classes

Authors:
    (C) Marvin Mager - @mvnmgrx - 2022

License identifier:
    GPL-3.0
"""

import unittest
from os import path
from kiutils.items.schitems import HierarchicalSheetInstance

from tests.testfunctions import to_file_and_compare, prepare_test, cleanup_after_test, TEST_BASE
from kiutils.schematic import Schematic
from kiutils.items.common import Property

SCHEMATIC_BASE = path.join(TEST_BASE, 'schematic')

class Tests_Schematic(unittest.TestCase):
    """Test cases for Schematics"""

    def setUp(self) -> None:
        prepare_test(self)
        return super().setUp()

    def test_addPropertyToSchematicSymbol(self):
        """Adds a new property to an already existing symbol in the schematic and verifies the
        correct initial values for the Property() class."""
        self.testData.pathToTestFile = path.join(SCHEMATIC_BASE, 'test_addPropertyToSchematicSymbol')
        schematic = Schematic().from_file(self.testData.pathToTestFile)
        schematic.schematicSymbols[0].properties.append(
            Property(key='Property3', value='I was added from "outside" of KiCad', id=6)
        )
        self.assertTrue(to_file_and_compare(schematic, self.testData))

    def test_createEmptySchematic(self):
        """Tests that an empty schematic generates S-Expression as expected from KiCad

        Note: This test currently disregards an empty ``(symbol_instances)`` token as it seems that this
        only exists when empty KiCad schematics are created. This is what should be expected for
        empty schematics:

        <pre><code>
        (kicad_sch (version 20211123) (generator kicad-python-tools)
            (paper "A4")
            (lib_symbols)
            (symbol_instances)
        )
        </code</pre>"""
        schematic = Schematic.create_new()
        self.testData.pathToTestFile = path.join(SCHEMATIC_BASE, 'test_createEmptySchematic')
        self.assertTrue(to_file_and_compare(schematic, self.testData))

    def test_schematicWithAllPrimitives(self):
        """Tests the parsing of a schematic with all primitives (lines, traces, busses, connections,
        images, etc)"""
        self.testData.pathToTestFile = path.join(SCHEMATIC_BASE, 'test_schematicWithAllPrimitives')
        schematic = Schematic().from_file(self.testData.pathToTestFile)
        self.assertTrue(to_file_and_compare(schematic, self.testData))

    def test_hierarchicalSchematicWithAllPrimitives(self):
        """Tests the parsing of a hierarchical schematic with all primitives (lines, traces, busses,
        connections, images, etc)"""
        self.testData.pathToTestFile = path.join(SCHEMATIC_BASE, 'test_hierarchicalSchematicWithAllPrimitives')
        schematic = Schematic().from_file(self.testData.pathToTestFile)
        self.assertTrue(to_file_and_compare(schematic, self.testData))

    def test_renameSymbolIdTokenInSchematic(self):
        """Tests if renaming (setting and unsetting) schematic symbols as well as normal symbols 
        using their ID token works as expected. Checks that the ``Value`` property does not change."""
        self.testData.pathToTestFile = path.join(SCHEMATIC_BASE, 'test_renameSymbolIdTokenInSchematic')
        schematic = Schematic().from_file(self.testData.pathToTestFile)
        schematic.libSymbols[0].libId = "RenamedSwitch:SW_Coded_New"        # Setting library nickname
        schematic.libSymbols[1].libId = "Unset_Lib_Id"                      # Unsetting library nickname
        schematic.schematicSymbols[0].libId = "SwitchRenamed:SW_Coded_2"    # Setting library nickname
        schematic.schematicSymbols[1].libId = "Unset_Lib_Id"                # Unsetting library nickname
        self.assertTrue(to_file_and_compare(schematic, self.testData))

    def test_setSymbolLibNameToken(self):
        """Tests if setting and unsetting the lib_name token generates the correct S-Expression"""
        self.testData.pathToTestFile = path.join(SCHEMATIC_BASE, 'test_setSymbolLibNameToken')
        schematic = Schematic().from_file(self.testData.pathToTestFile)
        schematic.schematicSymbols[0].libName = f"{schematic.schematicSymbols[0].entryName}_1"
        schematic.schematicSymbols[1].libName = None
        self.assertTrue(to_file_and_compare(schematic, self.testData))

    def test_parseStrokeTokens(self):
        """Tests the correct parsing of the Stroke token (with and without the color token)
         
        See:
            https://github.com/mvnmgrx/kiutils/pull/57
        """
        self.testData.compareToTestFile = True
        self.testData.pathToTestFile = path.join(SCHEMATIC_BASE, 'test_parseStrokeTokens')
        schematic = Schematic().from_file(self.testData.pathToTestFile)
        self.assertTrue(to_file_and_compare(schematic, self.testData))

class Tests_Schematic_Since_V7(unittest.TestCase):
    """Schematic related test cases since KiCad 7"""

    def setUp(self) -> None:
        prepare_test(self)
        return super().setUp()

    def test_textBoxAllVariants(self):
        """Tests all variants of the ``text_box`` token for text boxes in schematics"""
        self.testData.compareToTestFile = True
        self.testData.pathToTestFile = path.join(SCHEMATIC_BASE, 'since_v7', 'test_textBoxAllVariants')
        schematic = Schematic().from_file(self.testData.pathToTestFile)
        self.assertTrue(to_file_and_compare(schematic, self.testData))

    def test_rectangleAllVariants(self):
        """Tests all variants of the ``rectangle`` token for rectangles in schematics"""
        self.testData.compareToTestFile = True
        self.testData.pathToTestFile = path.join(SCHEMATIC_BASE, 'since_v7', 'test_rectangleAllVariants')
        schematic = Schematic().from_file(self.testData.pathToTestFile)
        self.assertTrue(to_file_and_compare(schematic, self.testData))

    def test_circleAllVariants(self):
        """Tests all variants of the ``circle`` token for circles in schematics"""
        self.testData.compareToTestFile = True
        self.testData.pathToTestFile = path.join(SCHEMATIC_BASE, 'since_v7', 'test_circleAllVariants')
        schematic = Schematic().from_file(self.testData.pathToTestFile)
        self.assertTrue(to_file_and_compare(schematic, self.testData))

    def test_arcAllVariants(self):
        """Tests all variants of the ``arc`` token for arcs in schematics"""
        self.testData.compareToTestFile = True
        self.testData.pathToTestFile = path.join(SCHEMATIC_BASE, 'since_v7', 'test_arcAllVariants')
        schematic = Schematic().from_file(self.testData.pathToTestFile)
        self.assertTrue(to_file_and_compare(schematic, self.testData))

    def test_schematicWithAllPrimitives(self):
        """Tests the parsing of a schematic with all primitives (lines, traces, busses, connections,
        images, etc) for KiCad 7"""
        self.testData.compareToTestFile = True
        self.testData.pathToTestFile = path.join(SCHEMATIC_BASE, 'since_v7', 'test_schematicWithAllPrimitives')
        schematic = Schematic().from_file(self.testData.pathToTestFile)
        self.assertTrue(to_file_and_compare(schematic, self.testData))

    def test_netclassFlags(self):
        """Tests the parsing netclass flags for KiCad 7"""
        self.testData.compareToTestFile = True
        self.testData.pathToTestFile = path.join(SCHEMATIC_BASE, 'since_v7', 'test_netclassFlags')
        schematic = Schematic().from_file(self.testData.pathToTestFile)
        self.assertTrue(to_file_and_compare(schematic, self.testData))

    def test_symbolPinOptionalTokens(self):
        """Tests the parsing of the optional name and number effects on symbol pins since KiCad v7.
        Came up in PR #73."""
        self.testData.compareToTestFile = True
        self.testData.pathToTestFile = path.join(SCHEMATIC_BASE, 'since_v7', 'test_symbolPinOptionalTokens')
        schematic = Schematic().from_file(self.testData.pathToTestFile)
        self.assertTrue(to_file_and_compare(schematic, self.testData))

    def test_strokeOptionalTokens(self):
        """Tests the parsing of the optional tokens on strokes since KiCad v7.
        Came up in PR #73."""
        self.testData.compareToTestFile = True
        self.testData.pathToTestFile = path.join(SCHEMATIC_BASE, 'since_v7', 'test_strokeOptionalTokens')
        schematic = Schematic().from_file(self.testData.pathToTestFile)
        self.assertTrue(to_file_and_compare(schematic, self.testData))
