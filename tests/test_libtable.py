"""Unittests of library table related classes

Authors:
    (C) Marvin Mager - @mvnmgrx - 2022

License identifier:
    GPL-3.0
"""

import unittest
from os import path

from tests.testfunctions import to_file_and_compare, prepare_test, cleanup_after_test, TEST_BASE
from kiutils.libraries import LibTable, Library

LIBTABLE_BASE = path.join(TEST_BASE, 'libtable')

class Tests_LibTable(unittest.TestCase):
    """Test cases for library tables"""

    def setUp(self) -> None:
        prepare_test(self)
        return super().setUp()

    def test_parseFpLibTable(self):
        """Tests the correct parsing of an example `fp-lib-table`"""
        self.testData.pathToTestFile = path.join(LIBTABLE_BASE, 'test_parseFpLibTable')
        libtable = LibTable().from_file(f'{self.testData.pathToTestFile}.expected')
        self.assertTrue(to_file_and_compare(libtable, self.testData))

    def test_parseSymLibTable(self):
        """Tests the correct parsing of an example `sym-lib-table`"""
        self.testData.pathToTestFile = path.join(LIBTABLE_BASE, 'test_parseSymLibTable')
        libtable = LibTable().from_file(f'{self.testData.pathToTestFile}.expected')
        self.assertTrue(to_file_and_compare(libtable, self.testData))

    def test_addLibraryObjectToLibTable(self):
        """Tests adding a library object to a library table"""
        self.testData.pathToTestFile = path.join(LIBTABLE_BASE, 'test_addLibraryObjectToLibTable')
        libtable = LibTable(type='fp_lib_table')
        libtable.libs.append(Library(
            name = 'object1',
            type = "KiCad",
            uri = '${KIPRJMOD}/my/library.pretty',
            options = 'Some options with "quoted strings"',
            description = 'Some description with "quoted strings"',
            active = False
        ))
        self.assertTrue(to_file_and_compare(libtable, self.testData))

    def test_addEmptyLibraryObjectToLibTable(self):
        """Tests adding an empty library object to a library table"""
        self.testData.pathToTestFile = path.join(LIBTABLE_BASE, 'test_addEmptyLibraryObjectToLibTable')
        libtable = LibTable(type='fp_lib_table')
        libtable.libs.append(Library())
        self.assertTrue(to_file_and_compare(libtable, self.testData))

    def test_createNewLibTable(self):
        """Tests the ``create_new()`` function to create a new library table"""
        self.testData.compareToTestFile = True
        self.testData.pathToTestFile = path.join(LIBTABLE_BASE, 'test_createNewLibTable')
        libtable = LibTable.create_new()
        self.assertTrue(to_file_and_compare(libtable, self.testData))

    # TODO: Tests with invalid type token