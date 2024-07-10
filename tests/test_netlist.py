"""Unittests of netlist related classes

Authors:
    (C) Ashton Snelgrove - @yashton - 2024

License identifier:
    GPL-3.0
"""

import unittest
import os
import tempfile
from tests.testfunctions import to_file_and_compare, prepare_test, cleanup_after_test, TEST_BASE
from kiutils.netlist import Netlist
from kiutils.utils import sexpr

NETLIST_BASE = os.path.join(TEST_BASE, 'netlist')

class Tests_Netlist(unittest.TestCase):
    """Test cases for Netlists"""

    def setUp(self) -> None:
        prepare_test(self)
        return super().setUp()

    def test_givenExample(self):
        """Tests the parsing of the example given in the documentation."""

        self.testData.compareToTestFile = True
        self.testData.pathToTestFile = os.path.join(NETLIST_BASE, 'example.net')
        netlist = Netlist().from_file(self.testData.pathToTestFile)
        result = Netlist().from_sexpr(sexpr.parse_sexp(netlist.to_sexpr()))
        self.assertNetlistEqual(netlist, result)

    def test_hierarchical(self):
        """Tests the parsing of the example given in the documentation."""

        self.testData.compareToTestFile = True
        self.testData.pathToTestFile = os.path.join(NETLIST_BASE, 'hierarchical.net')
        netlist = Netlist().from_file(self.testData.pathToTestFile)
        result = Netlist().from_sexpr(sexpr.parse_sexp(netlist.to_sexpr()))
        self.assertNetlistEqual(netlist, result)

    def assertNetlistEqual(self, netlist, result):
        # Note this asserts order is preserved
        self.assertEqual(netlist.design, result.design)
        for given, got in zip(netlist.components, result.components):
            self.assertComponentEqual(given, got)
        for given, got in zip(netlist.libparts, result.libparts):
            self.assertPartEqual(given, got)
        for given, got in zip(netlist.libraries, result.libraries):
            self.assertEqual(given, got)
        for given, got in zip(netlist.nets, result.nets):
            self.assertNetEqual(given, got)
        # Global check in case more detailed comparisons miss something
        self.assertEqual(given, got)

    def assertNetEqual(self, given, got):
        self.assertEqual(given.code, got.code)
        self.assertEqual(given.name, got.name)
        for left, right in zip(given.nodes, got.nodes):
            self.assertEqual(left, right)

    def assertComponentEqual(self, given, got):
        self.assertEqual(given.ref, got.ref)
        self.assertEqual(given.value, got.value)
        self.assertEqual(given.libsource, got.libsource)
        self.assertEqual(given.sheetpath, got.sheetpath)
        self.assertEqual(given.tstamps, got.tstamps)
        for left, right in zip(given.fields, got.fields):
            self.assertEqual(left, right)
        for left, right in zip(given.properties, got.properties):
            self.assertEqual(left, right)

    def assertPartEqual(self, given, got):
        self.assertEqual(given.lib, got.lib)
        self.assertEqual(given.part, got.part)
        for left, right in zip(given.footprints, got.footprints):
            self.assertEqual(left, right)
        for left, right in zip(given.fields, got.fields):
            self.assertEqual(left, right)
        for left, right in zip(given.pins, got.pins):
            self.assertEqual(left, right)
