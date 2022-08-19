from src.kiutils.schematic import Schematic
from src.kiutils.items.schitems import SchematicSymbol
from src.kiutils.items.common import Property
from src.kiutils.libraries import Library, LibTable

from tests.test_functions import to_file_and_compare
from os import path

import unittest
import HtmlTestRunner

TEST_BASE = path.join('tests', 'unittest-outputs')
SCHEMATIC_BASE = path.join(TEST_BASE, 'schematic')
LIBTABLE_BASE = path.join(TEST_BASE, 'libtable')

class Tests_Schematic(unittest.TestCase):
    """Test cases for Schematics"""

    def test_createEmptySchematic(self):
        """Tests that an empty schematic generates S-Expression as expected from KiCad"""
        schematic = Schematic()
        resultPath = path.join(SCHEMATIC_BASE, 'test_createEmptySchematic')
        self.assertTrue(to_file_and_compare(schematic, resultPath))


class Tests_LibTable(unittest.TestCase):
    """Test cases for library tables"""
    
    def test_parseFpLibTable(self):
        """Tests the correct parsing of an example `fp-lib-table`"""
        libpath = path.join(LIBTABLE_BASE, 'test_parseFpLibTable')
        libtable = LibTable().from_file(f'{libpath}.expected')
        self.assertTrue(to_file_and_compare(libtable, libpath))

    def test_parseSymLibTable(self):
        """Tests the correct parsing of an example `sym-lib-table`"""
        libpath = path.join(LIBTABLE_BASE, 'test_parseSymLibTable')
        libtable = LibTable().from_file(f'{libpath}.expected')
        self.assertTrue(to_file_and_compare(libtable, libpath))

    def test_addLibraryObjectToLibTable(self):
        """Tests adding a library object to a library table"""
        libpath = path.join(LIBTABLE_BASE, 'test_addLibraryObjectToLibTable')
        libtable = LibTable(type='fp_lib_table')

        libtable.libs.append(Library(
            name = 'object1', 
            type = "KiCad",
            uri = '${KIPRJMOD}/my/library.pretty', 
            options = 'Some options with "quoted strings"',
            description = 'Some description with "quoted strings"'
        ))

        self.assertTrue(to_file_and_compare(libtable, libpath))

    def test_addEmptyLibraryObjectToLibTable(self):
        """Tests adding an empty library object to a library table"""
        libpath = path.join(LIBTABLE_BASE, 'test_addEmptyLibraryObjectToLibTable')
        libtable = LibTable(type='fp_lib_table')
        libtable.libs.append(Library())
        self.assertTrue(to_file_and_compare(libtable, libpath))

    # TODO: Tests with invalid type token