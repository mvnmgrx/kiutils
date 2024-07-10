"""Class to manage KiCad eeschema netlist export

Author:
    (C) Ashton Snelgrove - @yashton - 2024

License identifier:
    GPL-3.0

Major changes:
    10.07.2024 - created

Documentation taken from:
    https://docs.kicad.org/master/en/eeschema/eeschema.html#netlist-export
    https://docs.kicad.org/master/en/eeschema/eeschema.html#intermediate-netlist-structure
"""
from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional, List, Union
from kiutils.utils import sexpr
from kiutils.items.netitems import *
from os import path

@dataclass
class Netlist():
    version: str = ""
    design: NetlistDesign = field(default_factory=lambda: NetlistDesign())
    components: List[NetlistComponent] = field(default_factory=list)
    libraries: List[NetlistLibrary] = field(default_factory=list)
    libparts: List[NetlistLibpart] = field(default_factory=list)
    nets: List[NetlistNet] = field(default_factory=list)

    @classmethod
    def from_sexpr(cls, exp: list):
        """Convert the given S-Expression into a Netlist object

        Args:
            - exp (list): Part of parsed S-Expression ``(netlist ...)``

        Raises:
            - Exception: When given parameter's type is not a list
            - Exception: When the first item of the list is not netlist

        Returns:
            - Netlist: Object of the class initialized with the given S-Expression
        """
        if not isinstance(exp, list):
            raise Exception("Expression does not have the correct type")

        if exp[0] != 'export':
            raise Exception(f"Expression does not have the correct type: '{exp[0]}'")

        object = cls()
        for item in exp[1:]:
            if item[0] == 'version': object.version = item[1]
            elif item[0] == 'design': object.design = NetlistDesign.from_sexpr(item)
            elif item[0] == 'components':
                for comp in item[1:]:
                    object.components.append(NetlistComponent().from_sexpr(comp))
            elif item[0] == 'libraries':
                for lib in item[1:]:
                    object.libraries.append(NetlistLibrary().from_sexpr(lib))
            elif item[0] == 'libparts':
                for symbol in item[1:]:
                    object.libparts.append(NetlistLibpart().from_sexpr(symbol))
            elif item[0] == 'nets':
                for symbol in item[1:]:
                    object.nets.append(NetlistNet().from_sexpr(symbol))
            else: raise Exception(f"Unexpected list item '{item[0]}'")
        return object

    @classmethod
    def from_file(cls, filepath: str, encoding: Optional[str] = None):
        """Load a netlist directly from a KiCad netlist export file and sets the
        ``self.filePath`` attribute to the given file path.

        Args:
            - filepath (str): Path or path-like object that points to the file
            - encoding (str, optional): Encoding of the input file. Defaults to None (platform
                                        dependent encoding).

        Raises:
            - Exception: If the given path is not a file

        Returns:
            - Netlist: Object of the Netlist class initialized with the given netlist
        """
        if not path.isfile(filepath):
            raise Exception("Given path is not a file!")

        with open(filepath, 'r', encoding=encoding) as infile:
            item = cls.from_sexpr(sexpr.parse_sexp(infile.read()))
            item.filePath = filepath
            return item

    def to_file(self, filepath = None, encoding: Optional[str] = None):
        """Save the object to a file in S-Expression format

        Args:
            - filepath (str, optional): Path-like string to the file. Defaults to None. If not set,
                                        the attribute ``self.filePath`` will be used instead.
            - encoding (str, optional): Encoding of the output file. Defaults to None (platform
                                        dependent encoding).

        Raises:
            - Exception: If no file path is given via the argument or via `self.filePath`
        """
        if filepath is None:
            if self.filePath is None:
                raise Exception("File path not set")
            filepath = self.filePath

        with open(filepath, 'w', encoding=encoding) as outfile:
            outfile.write(self.to_sexpr())

    def to_sexpr(self, indent=0, newline=True) -> str:
        """Generate the S-Expression representing this object

        Args:
            - indent (int): Number of whitespaces used to indent the output. Defaults to 0.
            - newline (bool): Adds a newline to the end of the output. Defaults to True.

        Returns:
            - str: S-Expression of this object
        """
        indents = ' '*indent
        endline = '\n' if newline else ''

        expression =  f'{indents}(export (version "{dequote(self.version)}")\n'
        if self.design is not None:
            expression += self.design.to_sexpr(indent+2)
        if self.components:
            expression += '\n'
            expression += '  (components\n'
            for item in self.components:
                expression += item.to_sexpr(indent+4)
            expression += '  )\n'
        if self.libparts:
            expression += '\n'
            expression += '  (libparts\n'
            for item in self.libparts:
                expression += item.to_sexpr(indent+4)
            expression += '  )\n'
        if self.libraries:
            expression += '\n'
            expression += '  (libraries\n'
            for item in self.libraries:
                expression += item.to_sexpr(indent+4)
            expression += '  )\n'
        if self.nets:
            expression += '\n'
            expression += '  (nets\n'
            for item in self.nets:
                expression += item.to_sexpr(indent+4)
            expression += '  )\n'
        expression += f'{indents}){endline}'
        return expression
