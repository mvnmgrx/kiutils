from kiutils.footprint import Footprint
from kiutils.symbol import SymbolLib
from kiutils.schematic import Schematic
from kiutils.board import Board
from kiutils.libraries import LibTable
import time
from os import path

import filecmp

global_passed = True

def test_from_file(cls, filepath: str) -> bool:
    global global_passed
    outpath = f'{filepath}.testoutput'
    passed = True
    rtext = ''
    start = time.time()
    try:
        item = cls.from_file(filepath)
    except:
        rtext = 'Could not construct'
        passed = False
    
    if passed:
        try:
            item.to_file(outpath)
        except:
            rtext = 'Could not save'
            passed = False
    end = time.time()

    if passed:
        passed = filecmp.cmp(filepath, outpath)
        if not passed:
            rtext = 'Input/output not equal'

    result = '✅' if passed else '❌'
    rtext = 'Success' if passed else rtext
    if global_passed:
        global_passed = passed
    print(f'{result} - {end-start:.3f}s - Testing {str(cls)} for case {path.basename(filepath)}. result: {rtext}')

# Get current working directory
tests_path = path.join(path.dirname(path.realpath(__file__)), 'tests')

test_from_file(LibTable, path.join(tests_path, 'kicad-project', 'fp-lib-table'))
test_from_file(LibTable, path.join(tests_path, 'kicad-project', 'sym-lib-table'))

test_from_file(Schematic, path.join(tests_path, 'kicad-project', 'test.kicad_sch'))

test_from_file(Board, path.join(tests_path, 'kicad-project', 'test.kicad_pcb'))

test_from_file(Footprint, path.join(tests_path, 'kicad-project', 'Library.pretty', 'test.kicad_mod'))
test_from_file(Footprint, path.join(tests_path, 'test_fp_all.kicad_mod'))

test_from_file(SymbolLib, path.join(tests_path, 'kicad-project', 'test.kicad_sym'))
test_from_file(SymbolLib, path.join(tests_path, 'test_sym_demorgan.kicad_sym'))
test_from_file(SymbolLib, path.join(tests_path, 'test_sym_demorgan_syitems.kicad_sym'))
test_from_file(SymbolLib, path.join(tests_path, 'test_sym_parameters.kicad_sym'))
test_from_file(SymbolLib, path.join(tests_path, 'test_sym_pins.kicad_sym'))

if global_passed:
    print("KiTools tests done")
else:
    print("KiTools tests done, but some tests failed!")