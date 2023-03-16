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
from kiutils.utils.sexpr import parse_sexp

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

        # Create an empty symbol library
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

    def test_renameParentIdUsingIdToken(self):
        """Rename symbol inside library using the id token setter and verify all units are renamed
        correctly as well as the ``Value`` property stayed the same."""
        self.testData.pathToTestFile = path.join(SYMBOL_BASE, 'test_renameParentIdUsingIdToken')
        symbolLib = SymbolLib().from_file(self.testData.pathToTestFile)
        symbolLib.symbols[0].libId = 'ExampleLibrary:AD2023'    # Setting library nickname
        symbolLib.symbols[1].libId = 'AD2023'                   # Unsetting library nickname
        self.assertTrue(to_file_and_compare(symbolLib, self.testData))

    def test_createNewTopLevelSymbolFromChild(self):
        """Take a child symbol, rename its library id and make a new top-level symbol out of it.
        Tests if resetting both ``unitId`` and ``styleId`` works."""
        self.testData.pathToTestFile = path.join(SYMBOL_BASE, 'test_createNewTopLevelSymbolFromChild')
        symbolLib = SymbolLib().from_file(self.testData.pathToTestFile)

        # Copy the symbol
        childSymbol = Symbol.from_sexpr(parse_sexp(symbolLib.symbols[0].units[0].to_sexpr()))

        # Rename it and save it as a new top-level symbol to the library
        childSymbol.libId = "SomeNewName:AD2023"
        symbolLib.symbols.append(childSymbol)
        self.assertTrue(to_file_and_compare(symbolLib, self.testData))

    def test_mergeLibraries(self):
        """Merge the symbols of two symbol libraries together"""
        self.testData.pathToTestFile = path.join(SYMBOL_BASE, 'test_mergeLibraries')
        symbolLib1 = SymbolLib().from_file(self.testData.pathToTestFile)
        symbolLib2 = SymbolLib().from_file(path.join(SYMBOL_BASE, 'test_symbolDemorganSyItems'))
        for symbol in symbolLib2.symbols:
            symbolLib1.symbols.insert(0, symbol)
        self.assertTrue(to_file_and_compare(symbolLib1, self.testData))

    def test_symbolIdParser(self):
        """Tests edge cases of parsing the symbol ID token and checks if the ID was split into
        its parts correctly

        Related issues:
            - [Pull request 73](https://github.com/mvnmgrx/kiutils/pull/73)
        """
        self.testData.pathToTestFile = path.join(SYMBOL_BASE, 'test_symbolIdParser')
        self.testData.compareToTestFile = True
        symbolLib = SymbolLib().from_file(self.testData.pathToTestFile)
        self.assertTrue(to_file_and_compare(symbolLib, self.testData))

class Tests_Symbol_Since_V7(unittest.TestCase):
    """Test cases for Symbols since KiCad 7"""

    def setUp(self) -> None:
        prepare_test(self)
        return super().setUp()

    def test_textBoxAllVariants(self):
        """Tests all variants of the ``text_box`` token for text boxes in symbols"""
        self.testData.compareToTestFile = True
        self.testData.pathToTestFile = path.join(SYMBOL_BASE, 'since_v7', 'test_textBoxAllVariants')
        symbolLib = SymbolLib().from_file(self.testData.pathToTestFile)
        self.assertTrue(to_file_and_compare(symbolLib, self.testData))

    def test_rectangleAllVariants(self):
        """Tests all variants of the ``rectangle`` token for rectangles in symbols"""
        self.testData.compareToTestFile = True
        self.testData.pathToTestFile = path.join(SYMBOL_BASE, 'since_v7', 'test_rectangleAllVariants')
        symbolLib = SymbolLib().from_file(self.testData.pathToTestFile)
        self.assertTrue(to_file_and_compare(symbolLib, self.testData))

    def test_circleAllVariants(self):
        """Tests all variants of the ``circle`` token for circles in symbols"""
        self.testData.compareToTestFile = True
        self.testData.pathToTestFile = path.join(SYMBOL_BASE, 'since_v7', 'test_circleAllVariants')
        symbolLib = SymbolLib().from_file(self.testData.pathToTestFile)
        self.assertTrue(to_file_and_compare(symbolLib, self.testData))

    def test_arcAllVariants(self):
        """Tests all variants of the ``arc`` token for arcs in symbols"""
        self.testData.compareToTestFile = True
        self.testData.pathToTestFile = path.join(SYMBOL_BASE, 'since_v7', 'test_arcAllVariants')
        symbolLib = SymbolLib().from_file(self.testData.pathToTestFile)
        self.assertTrue(to_file_and_compare(symbolLib, self.testData))