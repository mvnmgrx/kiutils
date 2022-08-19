from dataclasses import dataclass
from src.kiutils.schematic import Schematic
from src.kiutils.items.schitems import SchematicSymbol
from src.kiutils.items.common import Property
from src.kiutils.libraries import Library, LibTable

from tests.test_functions import to_file_and_compare, load_contents
from os import path

import unittest

TEST_BASE = path.join('tests', 'unittest-outputs')
SCHEMATIC_BASE = path.join(TEST_BASE, 'schematic')
LIBTABLE_BASE = path.join(TEST_BASE, 'libtable')

@dataclass
class TestData():
    """Data container to relay testcase-specific information to the report generator. Can be added 
    as a member to `unittest.TestCase` in each `test_XYZ()` function. The object will then be 
    available in `result._TestInfo()` classes constructor."""
    producedOutput: str | None = None
    expectedOutput: str | None = None
    ownDescription: str | None = None
    pathToTestFile: str | None = None

#    ___     _                   _   _    
#   / __| __| |_  ___ _ __  __ _| |_(_)__ 
#   \__ \/ _| ' \/ -_) '  \/ _` |  _| / _|
#   |___/\__|_||_\___|_|_|_\__,_|\__|_\__|
#         
class Tests_Schematic(unittest.TestCase):
    """Test cases for Schematics"""

    def setUp(self) -> None:
        """Set up LibTable tests"""
        self.testData = TestData()
        return super().setUp()
    
    def test_createEmptySchematic(self):
        """Tests that an empty schematic generates S-Expression as expected from KiCad"""
        schematic = Schematic()
        self.testData.pathToTestFile = path.join(SCHEMATIC_BASE, 'test_createEmptySchematic')
        self.assertTrue(to_file_and_compare(schematic, self.testData.pathToTestFile))

    def tearDown(self) -> None:
        if self.testData.pathToTestFile is None:
            raise Exception("Path to testfile must not be None!")
        self.testData.producedOutput = load_contents(f'{self.testData.pathToTestFile}.testoutput')
        self.testData.expectedOutput = load_contents(f'{self.testData.pathToTestFile}.expected')
        return super().tearDown()

#    _    _ _   _____     _    _     
#   | |  (_) |_|_   _|_ _| |__| |___ 
#   | |__| | '_ \| |/ _` | '_ \ / -_)
#   |____|_|_.__/|_|\__,_|_.__/_\___|
#                                    

class Tests_LibTable(unittest.TestCase):
    """Test cases for library tables"""

    def setUp(self) -> None:
        """Set up LibTable tests"""
        self.testData = TestData()
        return super().setUp()
    
    def test_parseFpLibTable(self):
        """Tests the correct parsing of an example `fp-lib-table`"""
        self.testData.pathToTestFile = path.join(LIBTABLE_BASE, 'test_parseFpLibTable')
        libtable = LibTable().from_file(f'{self.testData.pathToTestFile}.expected')
        self.assertTrue(to_file_and_compare(libtable, self.testData.pathToTestFile))

    def test_parseSymLibTable(self):
        """Tests the correct parsing of an example `sym-lib-table`"""
        self.testData.pathToTestFile = path.join(LIBTABLE_BASE, 'test_parseSymLibTable')
        libtable = LibTable().from_file(f'{self.testData.pathToTestFile}.expected')
        self.assertTrue(to_file_and_compare(libtable, self.testData.pathToTestFile))

    def test_addLibraryObjectToLibTable(self):
        """Tests adding a library object to a library table"""
        self.testData.pathToTestFile = path.join(LIBTABLE_BASE, 'test_addLibraryObjectToLibTable')
        libtable = LibTable(type='fp_lib_table')
        libtable.libs.append(Library(
            name = 'object1', 
            type = "KiCad",
            uri = '${KIPRJMOD}/my/library.pretty', 
            options = 'Some options with "quoted strings"',
            description = 'Some description with "quoted strings"'
        ))
        self.assertTrue(to_file_and_compare(libtable, self.testData.pathToTestFile))

    def test_addEmptyLibraryObjectToLibTable(self):
        """Tests adding an empty library object to a library table"""
        self.testData.pathToTestFile = path.join(LIBTABLE_BASE, 'test_addEmptyLibraryObjectToLibTable')
        libtable = LibTable(type='fp_lib_table')
        libtable.libs.append(Library())
        self.assertTrue(to_file_and_compare(libtable, self.testData.pathToTestFile))

    def tearDown(self) -> None:
        if self.testData.pathToTestFile is None:
            raise Exception("Path to testfile must not be None!")
        self.testData.producedOutput = load_contents(f'{self.testData.pathToTestFile}.testoutput')
        self.testData.expectedOutput = load_contents(f'{self.testData.pathToTestFile}.expected')
        return super().tearDown()

    # TODO: Tests with invalid type token