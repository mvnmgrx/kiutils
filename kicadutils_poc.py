from kiutils.board import Board
from kiutils.schematic import Schematic

from os.path import join

basepath = 'D:/etc/versanode/vn-mcu-board'

board = Board().from_file(join(basepath, 'vn-mcu.kicad_pcb'))
board.to_file(join(basepath, 'vn-mcu.kicad_pcb.testoutput'))
schematic = Schematic().from_file(join(basepath, 'vn-mcu.kicad_sch'))
schematic.to_file(join(basepath, 'vn-mcu.kicad_sch.testoutput'))

print("olla")