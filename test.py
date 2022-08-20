"""Some simple tests for the classes that read and write to files

Author:
    (C) Marvin Mager - @mvnmgrx - 2022

License identifier:
    GPL-3.0
"""
import unittest

from tests.board import *
from tests.designrules import *
from tests.footprint import *
from tests.libtable import *
from tests.schematic import *
from tests.symbol import *
from tests.worksheets import *
from tests.reporter.runner import HTMLTestRunner

if __name__ == "__main__":
    unittest.main(testRunner=HTMLTestRunner(
        combine_reports = True,
        verbosity = 3,
        report_title = 'KiUtils Unittest Report',
        report_name = 'KiUtils_Testreport',
        open_in_browser = True
    ))