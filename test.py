"""Some simple tests for the classes that read and write to files

Author:
    (C) Marvin Mager - @mvnmgrx - 2022

License identifier:
    GPL-3.0
"""
from logging.handlers import RotatingFileHandler
import time
from os import path
import filecmp
import logging

from src.kiutils.footprint import Footprint
from src.kiutils.symbol import SymbolLib
from src.kiutils.schematic import Schematic
from src.kiutils.board import Board
from src.kiutils.libraries import LibTable
from src.kiutils.wks import WorkSheet
from src.kiutils.dru import DesignRules

global_passed = True

def test_compare(cls, test_file: str, compare_file: str):
    """Main test function to test an item`s `.to_sexpr()` method

    Args:
        test_file (str): Path or path-like object to the test case input
        compare_file (str): Path or path-like object to the test case output, which may
        be the same as the input file

    Raises:
        Exception: Exception text containing the cause of the test failing

    The test passed if no exception was raised. Otherwise the test always failed.
    """
    global global_passed
    log = logging.getLogger(__name__)
    # Construct the item to be tested
    log.info(f'Constructing {cls} from {test_file} and comparing with {compare_file}..')
    try:
        item = cls.from_file(test_file)
    except Exception as ex:
        log.error(f'Could not construct. Exception: {ex}')
        global_passed = False
        raise Exception("Could not construct")

    # Write parsed item to .testoutput file
    try:
        item.to_file(f'{test_file}.testoutput')
    except Exception as ex:
        log.error(f'Could not save. Exception: {ex}')
        global_passed = False
        raise Exception("Could not save")

    # Compare with the given compare file:
    passed = filecmp.cmp(f'{test_file}.testoutput', compare_file)
    if not passed:
        log.error(f'Input/output not as expected! Check differences of {test_file}.testoutput to {compare_file}!')
        global_passed = False
        raise Exception("Input/output not as expected")

def assert_compare(cls, test_file: str):
    """Instantiates the item `cls` with a given test file as input and test for comparison 
    the item's output as well as a file containing the expected output for the test

    Args:
        test_file (str): Path or path-like object to the test file

    The file containing the expected test output must be located in the same folder as given by 
    `test_file`. It furthermore has to have the following name: `{test_file}.expected`. The 
    function will then construct the item `cls` with the input given in `test_file`, generate 
    the output by calling `cls.to_sexpr()` and comparing it with the file containting the 
    expected test output.

    The test fails if the output of `cls.to_sexpr()` differs from `{test_file}.expected`
    """
    rtext = "Success"
    start = time.time()
    try:
        test_compare(cls, test_file, f'{test_file}.expected')
        result = '✅'
    except Exception as ex:
        rtext = str(ex)
        result = '❌'
        
    end = time.time()
    print(f'{result} - {end-start:.3f}s - Testing {str(cls)} to equality for case {path.basename(test_file)}. result: {rtext}')

def assert_equality(cls, test_file: str):
    """Instantiates the item `cls` with a given test file as input and test for comparison 
    the item's output as well as the input file itself

    Args:
        test_file (str): Path or path-like object to the test file

    The function will then construct the item `cls` with the input given in `test_file`, 
    generate the output by calling `cls.to_sexpr()` and comparing it with the original 
    input `test_file`

    The test fails if the output of `cls.to_sexpr()` differs from `{test_file}`
    """
    rtext = "Success"
    start = time.time()
    try:
        test_compare(cls, test_file, test_file)
        result = '✅'
    except Exception as ex:
        rtext = str(ex)
        result = '❌'
        
    end = time.time()
    print(f'{result} - {end-start:.3f}s - Testing {str(cls)} to compare for case {path.basename(test_file)}. result: {rtext}')

if __name__ == "__main__":
    # Initialize logger
    format = logging.Formatter("%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(format)
    # stream_handler.setFormatter(format)
    # logger.addHandler(stream_handler)

    file_handler = RotatingFileHandler("test.log", maxBytes = 10e6, backupCount = 1)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(format)
    logger.addHandler(file_handler)

    logger.info("KiUtils tests starting..")
    # Get current working directory
    tests_path = path.join(path.dirname(path.realpath(__file__)), 'tests')

    # Test KiCad test project
    assert_equality(LibTable,  path.join(tests_path, 'kicad-project', 'fp-lib-table'))
    assert_equality(LibTable,  path.join(tests_path, 'kicad-project', 'sym-lib-table'))
    assert_compare(Schematic,  path.join(tests_path, 'kicad-project', 'test.kicad_sch'))
    assert_compare(Board,      path.join(tests_path, 'kicad-project', 'test.kicad_pcb'))
    assert_equality(Footprint, path.join(tests_path, 'kicad-project', 'Library.pretty', 'test.kicad_mod'))
    assert_equality(SymbolLib, path.join(tests_path, 'kicad-project', 'test.kicad_sym'))

    # Other test cases
    assert_compare(Footprint,  path.join(tests_path, 'test_fp_all.kicad_mod'))
    assert_equality(Footprint, path.join(tests_path, 'test_fp_empty_attr.kicad_mod'))
    assert_equality(SymbolLib, path.join(tests_path, 'test_sym_demorgan.kicad_sym'))
    assert_equality(SymbolLib, path.join(tests_path, 'test_sym_demorgan_syitems.kicad_sym'))
    assert_equality(SymbolLib, path.join(tests_path, 'test_sym_parameters.kicad_sym'))
    assert_equality(SymbolLib, path.join(tests_path, 'test_sym_pins.kicad_sym'))
    assert_equality(SymbolLib, path.join(tests_path, 'test_sym_alternate_pins.kicad_sym'))
    assert_equality(WorkSheet, path.join(tests_path, 'test_wks_all.kicad_wks'))
    assert_equality(DesignRules, path.join(tests_path, 'test_dru_all.kicad_dru'))
    assert_equality(Footprint, path.join(tests_path, 'test_fp_pad_newlines.kicad_mod'))
    assert_equality(Board,     path.join(tests_path, 'test_pcb_trace_arcs.kicad_pcb'))
    assert_equality(Board,     path.join(tests_path, 'test_pcb_stackup_dielectrics_32layer_vias.kicad_pcb'))

    print("\n---------------------\n")

    if global_passed:
        print("✅ KiUtils tests done, all green ✅")
    else:
        print("❌❌ KiUtils tests done, but some tests failed! Check 'test.log' for more information ❌❌")