"""Unittests of board related classes

Authors:
    (C) Marvin Mager - @mvnmgrx - 2022

License identifier:
    GPL-3.0
"""

import unittest
from os import path
from kiutils.footprint import Attributes

from tests.testfunctions import to_file_and_compare, prepare_test, cleanup_after_test, TEST_BASE
from kiutils.board import Board

BOARD_BASE = path.join(TEST_BASE, 'board')

class Tests_Board(unittest.TestCase):
    """Test cases for Boards"""

    def setUp(self) -> None:
        prepare_test(self)
        return super().setUp()

    def test_boardTraceArcs(self):
        """Tests the parser's handling of traces with arcs"""
        self.testData.compareToTestFile = True
        self.testData.pathToTestFile = path.join(BOARD_BASE, 'test_boardTraceArcs')
        board = Board().from_file(self.testData.pathToTestFile)
        self.assertTrue(to_file_and_compare(board, self.testData))

    def test_boardStackup32LayerDielectricsVias(self):
        """Tests the parsing of a board with 32 layers, all different dielectric layers and all
        available via combinations"""
        self.testData.compareToTestFile = True
        self.testData.pathToTestFile = path.join(BOARD_BASE, 'test_boardStackup32LayerDielectricsVias')
        board = Board().from_file(self.testData.pathToTestFile)
        self.assertTrue(to_file_and_compare(board, self.testData))

    def test_boardWithAllPrimitives(self):
        """Tests the parsing of a board containting all primitives (traces, texts, forms, dimensions,
        markers, polygons, etc)"""
        self.testData.pathToTestFile = path.join(BOARD_BASE, 'test_boardWithAllPrimitives')
        board = Board().from_file(self.testData.pathToTestFile)
        self.assertTrue(to_file_and_compare(board, self.testData))

    def test_allFpManufacturingAttributes(self):
        """Tests the parsing of a board with footprints that feature all combinations of
        manufacturing attributes. Tests all possible combinations of the following:
        <ul>
            <li>Board Only: True / False</li>
            <li>Exclude from BOM: True / False</li>
            <li>excludeFromPosFiles: True / False</li>
            <li>Type: SMD, THT, Other</li>
        </ul>

        Furthermore tests if the Attributes() object of a footprint is correctly created even
        when the parsed footprint has no (attr ...) token in its S-Expression."""
        self.testData.compareToTestFile = True
        self.testData.pathToTestFile = path.join(BOARD_BASE, 'test_allFpManufacturingAttributes')
        board = Board().from_file(self.testData.pathToTestFile)

        # Test parsing
        self.assertTrue(to_file_and_compare(board, self.testData))

        # Test that attributes object is created, even when an empty attribute list is present in
        # parsed footprint
        attr = Attributes(boardOnly=False, excludeFromBom=False, excludeFromPosFiles=False, type=None)
        self.assertEqual(attr, board.footprints[11].attributes,
            msg="Parsing of footprint without `attr` field does not yield expected Attributes() object")

    def test_createEmptyBoard(self):
        """Tests the behavior when creating an empty board"""
        self.testData.compareToTestFile = True
        self.testData.pathToTestFile = path.join(BOARD_BASE, 'test_createEmptyBoard')
        board = Board().create_new()
        self.assertTrue(to_file_and_compare(board, self.testData))

    def test_footprintPadNewLines(self):
        """Renames the libId token (setting and unsetting) of footprints on a board"""
        self.testData.pathToTestFile = path.join(BOARD_BASE, 'test_renameFootprintIdToken')
        board = Board().from_file(self.testData.pathToTestFile)
        board.footprints[0].libId = "I_was_renamed:BUS_PCIexpress_x1"
        board.footprints[1].libId = "I_was_added:BUS_PCIexpress_x1"
        self.assertTrue(to_file_and_compare(board, self.testData))

    def test_pcbPlotParams(self):
        """Tests the parsing of board plot params"""
        self.testData.compareToTestFile = True
        self.testData.pathToTestFile = path.join(BOARD_BASE, 'test_pcbPlotParams')
        board = Board().from_file(self.testData.pathToTestFile)
        self.assertTrue(to_file_and_compare(board, self.testData))

    def test_zoneOnOuterLayersOnly(self):
        """Tests the parsing of a zone that is only on the outer board layers (F.Cu and B.Cu). 
        Regression test for bug in PR #89."""
        self.testData.compareToTestFile = True
        self.testData.pathToTestFile = path.join(BOARD_BASE, 'test_zoneOnOuterLayersOnly')
        board = Board().from_file(self.testData.pathToTestFile)
        self.assertTrue(to_file_and_compare(board, self.testData))

class Tests_Board_Since_V7(unittest.TestCase):
    """Test cases for Boards since KiCad 7"""

    def setUp(self) -> None:
        prepare_test(self)
        return super().setUp()

    def test_textBoxAllVariants(self):
        """Tests all variants of the ``text_box`` token for text boxes in PCBs"""
        self.testData.compareToTestFile = True
        self.testData.pathToTestFile = path.join(BOARD_BASE, 'since_v7', 'test_textBoxAllVariants')
        board = Board().from_file(self.testData.pathToTestFile)
        self.assertTrue(to_file_and_compare(board, self.testData))

    def test_imageWithLayerToken(self):
        """Tests the new ``layer`` token for images in PCBs"""
        self.testData.compareToTestFile = True
        self.testData.pathToTestFile = path.join(BOARD_BASE, 'since_v7', 'test_imageWithLayerToken')
        board = Board().from_file(self.testData.pathToTestFile)
        self.assertTrue(to_file_and_compare(board, self.testData))

    def test_pcbPlotParams(self):
        """Tests the parsing of board plot params since KiCad v7"""
        self.testData.compareToTestFile = True
        self.testData.pathToTestFile = path.join(BOARD_BASE, 'since_v7', 'test_pcbPlotParams')
        board = Board().from_file(self.testData.pathToTestFile)
        self.assertTrue(to_file_and_compare(board, self.testData))
        
    def test_textsWithRenderCaches(self):
        """Tests text elements with the ``render_cache`` token"""
        self.testData.compareToTestFile = True
        self.testData.pathToTestFile = path.join(BOARD_BASE, 'since_v7', 'test_textsWithRenderCaches')
        board = Board().from_file(self.testData.pathToTestFile)
        self.assertTrue(to_file_and_compare(board, self.testData))