"""Unittests of library symbol related classes

Authors:
    (C) Marvin Mager - @mvnmgrx - 2022

License identifier:
    GPL-3.0
"""

import unittest
from os import path

from tests.testfunctions import to_file_and_compare, prepare_test, cleanup_after_test, TEST_BASE
from kiutils.symbol import SymbolLib, Symbol
from kiutils.misc.config import KIUTILS_CREATE_NEW_VERSION_STR

SYMBOL_BASE = path.join(TEST_BASE, 'symbol')

class Tests_Symbol(unittest.TestCase):
    """Test cases for Symbols"""

    def setUp(self) -> None:
        prepare_test(self)
        return super().setUp()

    def test_allSymbolPinVariations(self):
        """Tests the parsing of all pin types of a symbol in a symbol library"""
        self.testData.compareToTestFile = True
        self.testData.pathToTestFile = path.join(SYMBOL_BASE, 'test_allSymbolPinVariations')
        symbolLib = SymbolLib().from_file(self.testData.pathToTestFile)
        self.assertTrue(to_file_and_compare(symbolLib, self.testData))

    def test_allSymbolAlternatePins(self):
        """Tests the parsing of all alternate pin definitions of a symbol in a symbol library"""
        self.testData.compareToTestFile = True
        self.testData.pathToTestFile = path.join(SYMBOL_BASE, 'test_allSymbolAlternatePins')
        symbolLib = SymbolLib().from_file(self.testData.pathToTestFile)
        self.assertTrue(to_file_and_compare(symbolLib, self.testData))

    def test_symbolParameters(self):
        """Tests the parsing of a symbol's parameters in a symbol library"""
        self.testData.compareToTestFile = True
        self.testData.pathToTestFile = path.join(SYMBOL_BASE, 'test_symbolParameters')
        symbolLib = SymbolLib().from_file(self.testData.pathToTestFile)
        self.assertTrue(to_file_and_compare(symbolLib, self.testData))

    def test_symbolDemorganUnits(self):
        """Tests the parsing of a symbol's de-morgan unit represenations in a symbol library"""
        self.testData.compareToTestFile = True
        self.testData.pathToTestFile = path.join(SYMBOL_BASE, 'test_symbolDemorganUnits')
        symbolLib = SymbolLib().from_file(self.testData.pathToTestFile)
        self.assertTrue(to_file_and_compare(symbolLib, self.testData))

    def test_symbolDemorganSyItems(self):
        """Tests the parsing of a symbol' in a symbol library that has all SyItems in different
        de-morgan variations in it"""
        self.testData.compareToTestFile = True
        self.testData.pathToTestFile = path.join(SYMBOL_BASE, 'test_symbolDemorganSyItems')
        symbolLib = SymbolLib().from_file(self.testData.pathToTestFile)
        self.assertTrue(to_file_and_compare(symbolLib, self.testData))

    def test_bigSymbolLibrary(self):
        """Tests the parsing of a big symbol library with many symbols of different kinds in it"""
        self.testData.compareToTestFile = True
        self.testData.pathToTestFile = path.join(SYMBOL_BASE, 'test_bigSymbolLibrary')
        symbolLib = SymbolLib().from_file(self.testData.pathToTestFile)
        self.assertTrue(to_file_and_compare(symbolLib, self.testData))

    def test_createNewSymbolInEmptyLibrary(self):
        """Tests the ``create_new()`` function to create an empty symbol that is added to a 
        symbol library"""
        self.testData.compareToTestFile = True
        self.testData.pathToTestFile = path.join(SYMBOL_BASE, 'test_createNewSymbolInEmptyLibrary')
        
        # Create an empty symbol libraray
        symbolLib = SymbolLib(
            version = KIUTILS_CREATE_NEW_VERSION_STR,
            generator = 'kiutils'
        )

        # Add a symbol to it via create_new()
        symbol = Symbol().create_new(
            id = 'testsymbol',
            reference = 'U',
            value = 'testvalue'
        )
        symbolLib.symbols.append(symbol)

        self.assertTrue(to_file_and_compare(symbolLib, self.testData))

