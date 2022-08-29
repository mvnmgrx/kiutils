"""Unittests of board related classes

Authors:
    (C) Marvin Mager - @mvnmgrx - 2022

License identifier:
    GPL-3.0
"""

import unittest
from os import path

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

    def tearDown(self) -> None:
        cleanup_after_test(self.testData)
        return super().tearDown()
