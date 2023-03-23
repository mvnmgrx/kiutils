"""Unittests of design-rules related classes

Authors:
    (C) Marvin Mager - @mvnmgrx - 2022

License identifier:
    GPL-3.0
"""

import unittest
from os import path

from tests.testfunctions import to_file_and_compare, prepare_test, cleanup_after_test, TEST_BASE
from kiutils.dru import DesignRules

DESIGNRULE_BASE = path.join(TEST_BASE, 'designrules')

class Tests_DesignRules(unittest.TestCase):
    """Test cases for Design Rules"""

    def setUp(self) -> None:
        prepare_test(self)
        return super().setUp()

    def test_allDesignRuleItems(self):
        """Tests the parsing of all available design rule items"""
        self.testData.compareToTestFile = True
        self.testData.pathToTestFile = path.join(DESIGNRULE_BASE, 'test_allDesignRuleItems')
        dru = DesignRules.from_file(self.testData.pathToTestFile)
        self.assertTrue(to_file_and_compare(dru, self.testData))

    def test_createNewDesignRules(self):
        """Tests the ``create_new()`` function to create a new set of design rules"""
        self.testData.compareToTestFile = True
        self.testData.pathToTestFile = path.join(DESIGNRULE_BASE, 'test_createNewDesignRules')
        dru = DesignRules.create_new()
        self.assertTrue(to_file_and_compare(dru, self.testData))

class Tests_DesignRules_Since_V7(unittest.TestCase):
    """Test cases for Design Rules since KiCad v7"""

    def setUp(self) -> None:
        prepare_test(self)
        return super().setUp()

    def test_severityToken(self):
        """Tests the parsing the new severity token"""
        self.testData.compareToTestFile = True
        self.testData.pathToTestFile = path.join(DESIGNRULE_BASE, 'since_v7', 'test_severityToken')
        dru = DesignRules.from_file(self.testData.pathToTestFile)
        self.assertTrue(to_file_and_compare(dru, self.testData))
