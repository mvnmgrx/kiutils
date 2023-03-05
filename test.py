"""Some simple tests for the classes that read and write to files

Author:
    (C) Marvin Mager - @mvnmgrx - 2022

License identifier:
    GPL-3.0
"""
import unittest

import os
import sys

PROJECT_PATH = os.getcwd()
SOURCE_PATH = os.path.join(
    PROJECT_PATH, "src"
)
sys.path.append(SOURCE_PATH)

from tests.test_board import *
from tests.test_designrules import *
from tests.test_footprint import *
from tests.test_libtable import *
from tests.test_schematic import *
from tests.test_symbol import *
from tests.test_worksheets import *
from tests.test_misc import *
from tests.reporter.runner import HTMLTestRunner

if __name__ == "__main__":
    unittest.main(testRunner=HTMLTestRunner(
        combine_reports = True,
        verbosity = 3,
        report_title = 'KiUtils Unittest Report',
        report_name = 'KiUtils_Testreport',
        open_in_browser = True
    ))