"""Unittests for misc stuff

Authors:
    (C) Marvin Mager - @mvnmgrx - 2022

License identifier:
    GPL-3.0
"""

import unittest
from os import path
from kiutils.schematic import Schematic

from tests.testfunctions import to_file_and_compare, prepare_test, TEST_BASE

MISC_BASE = path.join(TEST_BASE, 'misc')

class Tests_Misc(unittest.TestCase):
    """Misc test cases"""

    def setUp(self) -> None:
        prepare_test(self)
        return super().setUp()

    def test_quotesAndBackslashInSexpr(self):
        """Tests the correct parsing of all variants of quoted strings as well as of backslashes
        in said strings.

        Related issues:
            - [Pull request 73](https://github.com/mvnmgrx/kiutils/pull/73)
        """
        self.testData.pathToTestFile = path.join(MISC_BASE, 'test_quotesAndBackslashInSexpr')
        self.testData.compareToTestFile = True
        libtable = Schematic().from_file(self.testData.pathToTestFile)
        self.assertTrue(to_file_and_compare(libtable, self.testData))
