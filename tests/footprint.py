"""Unittests of footprint related classes

Authors:
    (C) Marvin Mager - @mvnmgrx - 2022

License identifier:
    GPL-3.0
"""

import unittest
from os import path

from tests.testfunctions import to_file_and_compare, prepare_test, cleanup_after_test, TEST_BASE
from kiutils.footprint import Footprint

FOOTPRINT_BASE = path.join(TEST_BASE, 'footprint')

class Tests_Footprint(unittest.TestCase):
    """Test cases for Footprints"""

    def setUp(self) -> None:
        prepare_test(self)
        return super().setUp()

    def test_allFootprintItems(self):
        """Tests the parsing of all available footprint items"""
        self.testData.pathToTestFile = path.join(FOOTPRINT_BASE, 'test_allFootprintItems')
        footprint = Footprint().from_file(self.testData.pathToTestFile)
        self.assertTrue(to_file_and_compare(footprint, self.testData))

    def test_footprintPadNewLines(self):
        """Tests the ability of the parser to create the correct new-line breaks when using
        exotic footprint pad combinations"""
        self.testData.compareToTestFile = True
        self.testData.pathToTestFile = path.join(FOOTPRINT_BASE, 'test_footprintPadNewLines')
        footprint = Footprint().from_file(self.testData.pathToTestFile)
        self.assertTrue(to_file_and_compare(footprint, self.testData))

    def test_footprintEmptyAttributes(self):
        """Tests the correct parsing of a footprint with empty `Attributes` field

        </p><b>Note:</b> Some earlier versions of KiCad seemed to include the `(attr ..)` token in footprints even
        when no attributes are set (or when using standard attributes). This test includes an empty 
        attribute token in the footprint and expects it to be gone after parsing. </p>
        """
        self.testData.pathToTestFile = path.join(FOOTPRINT_BASE, 'test_footprintEmptyAttributes')
        footprint = Footprint().from_file(self.testData.pathToTestFile)
        self.assertTrue(to_file_and_compare(footprint, self.testData))

    def tearDown(self) -> None:
        cleanup_after_test(self.testData)
        return super().tearDown()