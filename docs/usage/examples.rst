Examples
========

These examples show how the module is intended to be used.

Loading and saving a board
--------------------------

.. code-block:: python

   from kiutils.board import Board

   board = Board().from_file("path/to/board.kicad_pcb")

   # Do stuff ...

   board.to_file()


Changing title and revision in schematic
----------------------------------------

.. code-block:: python

   from kiutils.schematic import Schematic

   schematic = Schematic().from_file("path/to/schematic.kicad_sch")
   schematic.titleBlock.title = "This is schematic xyz"
   schematic.titleBlock.revision = "B"
   schematic.to_file()

Loading and adding footprint to board
-------------------------------------

Here a footprint is loaded from a `.kicad_mod` file and added to a board:

.. code-block:: python

   from kiutils.board import Board
   from kiutils.footprint import Footprint
   from kiutils.items.common import Position
   from kiutils.items.fpitems import FpText

   from os import path

   # Get current working directory
   tests_path = path.join(path.dirname(path.realpath(__file__)), 'tests')

   # Load board file and footprint file
   board = Board().from_file(path.join(tests_path, "example-project/example/example.kicad_pcb"))
   footprint = Footprint().from_file(path.join(tests_path, "example-project/example/C_0805.kicad_mod"))

   # Set new footprint's position
   footprint.position = Position(X=127.0, Y=85.0)

   # Change identifier to C105
   for item in footprint.graphicItems:
       if isinstance(item, FpText):
           if item.type == 'reference':
               item.text = "C105"

   # Append footprint to board and save board
   board.footprints.append(footprint)
   board.to_file()

Adding vias to board
--------------------

This example adds two vias on the normal axis at the end of each segment:

.. code-block:: python

   from cmath import sqrt
   from kiutils.board import Board
   from kiutils.items.brditems import Via, Segment
   from kiutils.items.common import Position

   from os import path

   # Get current working directory
   tests_path = path.join(path.dirname(path.realpath(__file__)), 'tests')

   # Load board file
   board = Board().from_file(path.join(tests_path, "example-project/example/example.kicad_pcb"))

   # Iterate through segments, arcs and vias ..
   for item in board.traceItems:
       if isinstance(item, Segment):
           # Calculate normal on end point of segment
           nvec = Position(-(item.end.Y - item.start.Y), item.end.X - item.start.X)
           nvec_inverse_len = 1/sqrt(nvec.X**2 + nvec.Y**2).real
           unit_normal = Position(nvec_inverse_len * nvec.X, nvec_inverse_len * nvec.Y)

           # Compute positions of new vias
           next_via_1 = Position(item.end.X + (unit_normal.X * 2), item.end.Y + (unit_normal.Y * 2))
           next_via_2 = Position(item.end.X - (unit_normal.X * 2), item.end.Y - (unit_normal.Y * 2))

           # Append vias to trace items list of board
           board.traceItems.append(Via(position=next_via_1, layers=["F.Cu", "B.Cu"], size=1.0, drill=0.6))
           board.traceItems.append(Via(position=next_via_2, layers=["F.Cu", "B.Cu"], size=1.0, drill=0.6))

   # Write changes back to board file
   board.to_file()

Adding a schematic symbol
-------------------------

This example shows how a schematic symbol might be added from a symbol library into a schematic:

.. code-block:: python

   from kiutils.schematic import Schematic, SymbolInstance, SchematicSymbol
   from kiutils.symbol import SymbolLib  
   from kiutils.items.common import Property, Position
   
   # Load the symbol library  
   symbol_lib = SymbolLib().from_file('/usr/share/kicad/symbols/Device.kicad_sym')  
   
   # Find the symbol in the library  
   symbol = None  
   for s in symbol_lib.symbols:  
      if s.entryName == 'R_Small_US':  
         symbol = s  
         break  
   
   if symbol is None:  
      raise ValueError('Symbol not found in library')  

   
   # Create a new schematic  
   schematic = Schematic.create_new()  
   
   # Add the symbol to the schematic  
   schematic.libSymbols.append(symbol)  

   schematic_symbol = SchematicSymbol()
   schematic_symbol.libName = 'R_Small_US'
   schematic_symbol.libId = 'Device:R_Small_US' 
   schematic_symbol.position = Position(X=0, Y=0, angle=0)

   schematic_symbol.properties.append(Property(key='Reference', value='R?', id=0))
   schematic_symbol.properties.append(Property(key='Value', value='R_Small_US', id=1))  

   schematic.schematicSymbols.append(schematic_symbol)  

   # Save the schematic to a file  
   schematic.to_file('path_to_save_schematic.kicad_sch')  


Importing Mouser Schematics/footprints/models .zips to Kicad
--------------------
you'll need an extra python file colored_terminal.py
.. code-block:: python
        # Small libary to add some colors to the consol output as well as a last line clear function
        # import with: from colored_terminal import *
        import sys

        def print_with_color(color_code, *args, indent=0):
            if indent:
                indent = " " * indent
            else:
                indent = ""
            print(f"\033[{color_code}m{indent}", end="")
            print(*args, end="")
            print("\033[0m", end="")
            sys.stdout.flush()


        def print_yellow(*args, indent = 0):
            print_with_color("33", *args, indent=indent)


        def print_black(*args, indent = 0):
            print_with_color("30", *args, indent=indent)


        def print_red(*args, indent = 0):
            print_with_color("31", *args, indent=indent)


        def print_green(*args, indent = 0):
            print_with_color("32", *args, indent=indent)


        def print_blue(*args, indent = 0):
            print_with_color("34", *args, indent=indent)


        def print_magenta(*args, indent = 0):
            print_with_color("35", *args, indent=indent)


        def print_cyan(*args, indent = 0):
            print_with_color("36", *args, indent=indent)


        def print_white(*args, indent = 0):
            print_with_color("37", *args, indent=indent)


        def clear_console_line():
            """clears the last line in the console"""
            print("\033[2K\033[G", end="", flush=True)

here goes the main code:
.. code-block:: python
        from pathlib import Path
        from kiutils.symbol import SymbolLib # https://kiutils.readthedocs.io/en/latest/module/kiutils.html#kiutils.footprint.Footprint.position
        from kiutils.footprint import Footprint# https://kiutils.readthedocs.io/en/latest/module/kiutils.html#kiutils.footprint.Footprint.position
        from kiutils.items.common import Position
        import sys
        import re
        import zipfile
        import shutil
        from colored_terminal import *

        if __name__ == '__main__':
            print_magenta("<Kicad Tool to import shematic, footprint and 3D Model from mouser to libary>\n\n")
            
            # handles argvs
            if len(sys.argv) != 3:
                print_yellow(f"  too little arguments: ({len(sys.argv)})\n")
                print_yellow("  start this tool with these arguments:\n")
                print_yellow("  [path_zip] [path_libary_folder]\n")
                sys.exit()
            
            PATH_ZIP = Path(sys.argv[1]) # path to zip where symbols to copy are
            PATH_LIBRARY_DIR = Path(sys.argv[2]) # path to libary where footprint should go
            PATH_LIBRARY_SYMBOLS = Path() # path to simbol libary
            PATH_LIBARY_PRETTY = Path() #path to footprint.pretty in libary
            PATH_TEMP_DIR = PATH_LIBRARY_DIR / "temporary" # temporaty folder to export ZIP to
            PATH_SYMBOL_2COPY = Path() # path to symbols which y wanna copy
            
            print_magenta(f'>extracting zip\n')
            # Extract zip contents to temporary directory
            with zipfile.ZipFile(PATH_ZIP, "r") as zip_ref:
                zip_ref.extractall(PATH_TEMP_DIR)
            print("\n",end='')
            
            print_magenta(f'>searching for target symbol/footprints\n')
            # search for a kicad symbol libary
            sym_dirs = list(PATH_LIBRARY_DIR.rglob("*.kicad_sym"))
            print_cyan(f' target symbol libary:')
            if len(sym_dirs):
                PATH_LIBRARY_SYMBOLS = sym_dirs[0]
                print_white(f'"{sym_dirs[0]}"\n')
            else:
                if PATH_TEMP_DIR.exists() and PATH_TEMP_DIR.is_dir():
                    shutil.rmtree(PATH_TEMP_DIR)
                raise Exception("ERROR: Not found")
            
            # search for a footprint folder
            pretty_dirs = [
                p for p in PATH_LIBRARY_DIR.rglob("*") if p.is_dir() and p.name.endswith(".pretty")
            ]
            print_cyan(f' target footprints:')
            if len(pretty_dirs):
                # found footprint folder
                print_white(f' "{pretty_dirs[0]}"\n')
                PATH_LIBARY_PRETTY = pretty_dirs[0]
            else:
                # creates footprint folder
                PATH_LIBARY_PRETTY = PATH_LIBRARY_DIR / (PATH_SYMBOL_2COPY.stem + ".pretty")
                PATH_LIBARY_PRETTY.mkdir(parents=True, exist_ok=True)
                print_white(f'created "{PATH_LIBARY_PRETTY}"\n')

            # search for a source kicad symbol libary in Source
            sym_dirs = list(PATH_TEMP_DIR.rglob("*.kicad_sym"))
            print_cyan(f' source symbol libary:')
            if len(sym_dirs):
                PATH_SYMBOL_2COPY = sym_dirs[0]
                print_white(f'"{sym_dirs[0]}"\n')
            else:
                if PATH_TEMP_DIR.exists() and PATH_TEMP_DIR.is_dir():
                    shutil.rmtree(PATH_TEMP_DIR)
                raise Exception("Nothing found\n")
            print("\n",end='')
            
            print_magenta(f'>copying symbol libary\n')
            # copys Symbol to libary
            # print(PATH_SYMBOL_2COPY)
            symbolLibrary = SymbolLib.from_file(PATH_LIBRARY_SYMBOLS)
            symbolToCopy = SymbolLib.from_file(PATH_SYMBOL_2COPY)
                    
            print_cyan(f" length target symbol libary: {len(symbolLibrary.symbols)}\n")
                
            for symbol in symbolToCopy.symbols:
                print_cyan(f' found symbol to insert: ')
                print_white(f'"{symbol.entryName}"\n')
                if any(s.entryName == symbol.entryName for s in symbolLibrary.symbols):
                    print_yellow("-> already in the library. Skipping.\n")
                else:
                    print("-> writes symbol to libary")
                    symbolLibrary.symbols.append(symbolToCopy.symbols[0])
                
            # overwrites existing libary
            print_cyan(f' new length of target libary: {len(symbolLibrary.symbols)}\n')
            symbolLibrary.to_file(PATH_LIBRARY_SYMBOLS)
            print("\n",end='')

            print_magenta(f'>Copying footprint\n')
            # copys Footprint
            print_cyan(f' copies footprint:')
            for model_file in PATH_TEMP_DIR.rglob("*.kicad_mod"):
                print(f'"{model_file.name}"')
                fp = Footprint.from_file(model_file)  # load from source
                for model in fp.models:
                    print_white(f'  -adjusted 3D model path')
                    print_white(f' from "{model.path}" | ')
                    model.path = "${KIPRJMOD}/libary/3D/" + model.path
                    print_white(f'to "{model.path}"')
                dest_path = PATH_LIBARY_PRETTY / model_file.name
                fp.to_file(dest_path) 
            print("\n",end='')
            print("\n",end='')
            
            print_magenta(f'>Copying 3D files\n')
            PATH_LIBARY_3D_DIR = PATH_LIBRARY_DIR / "3D"
            PATH_LIBARY_3D_DIR.mkdir(parents=True, exist_ok=True)
            foundOne = False
            print_cyan(f' copies 3D_model:')
            # print_yellow(f'path: "{PATH_TEMP_DIR}"\n')
            for model_file in PATH_TEMP_DIR.rglob("*.stp"):
                print(f'"{model_file.name}"',end='')
                shutil.copy2(model_file, PATH_LIBARY_3D_DIR / model_file.name)
                foundOne = True
            if not foundOne:
                print_red(f' didn t found a 3D model')
            print("\n",end='')
            print("\n",end='')

            # deletes temp
            print_magenta("<delete temp\n")
            if PATH_TEMP_DIR.exists() and PATH_TEMP_DIR.is_dir():
                shutil.rmtree(PATH_TEMP_DIR)
            print("\n",end='')
            
            print_magenta("<finished\n")
            

Sorting pins of a symbol
--------------------------

.. code-block:: python
        from kiutils.symbol import SymbolLib # https://kiutils.readthedocs.io/en/latest/module/kiutils.html#kiutils.footprint.Footprint.position
        from kiutils.items.common import Position
        import sys
        import re
        from colored_terminal import *

        SPACE_BETWEEN_PIN_X = 1.27*20
        SPACE_BETWEEN_PIN_Y = 1.27*2
            
        if __name__ == "__main__":
            print_yellow("<Kicad Tool to group symbol pins>\n")
            if len(sys.argv) != 3:
                if not (len((sys.argv)) >= 3 and int(sys.argv[2]) == -1):
                    print(f"too little arguments: ({len(sys.argv)})")
                    print("start this tool with these arguments:")
                    print("[libary_path] [nr_symbol]")
                    print("- filepath to libary")
                    print(
                        "- choose [number] wich simbols pins y wanna regroup. Set to -1 to just show the list"
                    )
                    sys.exit()

            # Load the symbol library
            filepath = sys.argv[1]
            lib = SymbolLib.from_file(filepath)

            print_cyan("Found Symbols:\n")
            # Print available symbols
            for nr, symbol in enumerate(lib.symbols):
                print(f"  [{nr}] Symbol name: {symbol.entryName}")

            # select symbol from libary
            number = sys.argv[2]
            if not number.isnumeric():
                print("please enter number")
                sys.exit()
            if int(number) == -1:
                sys.exit()
            selectedIc = lib.symbols[int(number)]

            print_cyan("Selected IC:\n")
            print(f"Symbol name: {selectedIc.entryName}")
            print(f"Amount of pins: {len(selectedIc.pins)}")
            if len(selectedIc.pins) == 0:
                print_red(
        f'Error:\n\
          go to {filepath}\n\
          find {selectedIc.entryName}\n\
          go to pin section\n\
          delete (above pins) the complete line "(symbol "{selectedIc.entryName} (in_bom yes) (on_board yes)"\n\
          as well as the matching brackets at the end.\n'
                )
                sys.exit()
                sys.exit()
            print("Properties:")
            for prop in selectedIc.properties:
                print(f"  {prop.key} = {prop.value}")

            # groups pins
            PinDictory = {}
            for pin in selectedIc.pins:
                groupName = pin.name[:3]  # grouping logic
                if groupName not in PinDictory:
                    PinDictory[groupName] = []
                PinDictory[groupName].append(pin)

            # sort groups
            def natural_key(pin):
                # extract prefix letters and numeric suffix for sorting
                match = re.match(r"([a-zA-Z]+)(\d+)", pin.name)
                if match:
                    prefix, num = match.groups()
                    return (prefix, int(num))
                else:
                    return (pin.name, 0)  # fallback

            sortedPinDictionary = {}
            for groupName, pinList in PinDictory.items():
                pinList.sort(key=natural_key)
                sortedPinDictionary[groupName] = pinList
            PinDictory = sortedPinDictionary

            # # changes coordinates from these pins
            for x, (groupName, pinList) in enumerate(PinDictory.items()):
                # try:
                for y, pin in enumerate(pinList):
                    pin.position.X = x * SPACE_BETWEEN_PIN_X
                    pin.position.Y = -y * SPACE_BETWEEN_PIN_Y - SPACE_BETWEEN_PIN_Y
                    pin.position.angle = 0
                    
            # saved modified file
            filepath = sys.argv[1]
            lib.to_file(filepath)

            print_yellow("conversion succesful\n")
