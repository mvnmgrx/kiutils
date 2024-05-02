"""
Author:
    (C) Marvin Mager - @mvnmgrx - 2022

License identifier:
    GPL-3.0

Major changes:
    14.02.2022 - created

Documentation taken from:
    https://dev-docs.kicad.org/en/file-formats/sexpr-intro/index.html#_symbols
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, List
from os import path
import re

from kiutils.items.common import Effects, Position, Property, Font
from kiutils.items.syitems import *
from kiutils.utils import sexpr
from kiutils.utils.strings import dequote
from kiutils.misc.config import KIUTILS_CREATE_NEW_VERSION_STR

@dataclass
class SymbolAlternativePin():
    pinName: str = ""
    """The ``pinName`` token defines the name of the alternative pin function"""

    electricalType: str = "input"
    """The ``electricalType`` defines the pin electrical connection. See symbol documentation for
    valid pin electrical connection types and descriptions."""

    graphicalStyle: str = "line"
    """The ``graphicalStyle`` defines the graphical style used to draw the pin. See symbol
    documentation for valid pin graphical styles and descriptions."""

    @classmethod
    def from_sexpr(cls, exp: list) -> SymbolAlternativePin:
        """Convert the given S-Expresstion into a SymbolAlternativePin object

        Args:
            - exp (list): Part of parsed S-Expression ``(alternate ...)``

        Raises:
            - Exception: When given parameter's type is not a list
            - Exception: When the first item of the list is not alternate

        Returns:
            - SymbolAlternativePin: Object of the class initialized with the given S-Expression
        """
        if not isinstance(exp, list):
            raise Exception("Expression does not have the correct type")

        if exp[0] != 'alternate':
            raise Exception("Expression does not have the correct type")

        object = cls()
        object.pinName = exp[1]
        object.electricalType = exp[2]
        object.graphicalStyle = exp[3]
        return object

    def to_sexpr(self, indent: int = 8, newline: bool = True) -> str:
        """Generate the S-Expression representing this object

        Args:
            - indent (int): Number of whitespaces used to indent the output. Defaults to 8.
            - newline (bool): Adds a newline to the end of the output. Defaults to True.

        Returns:
            - str: S-Expression of this object
        """
        indents = ' '*indent
        endline = '\n' if newline else ''

        return f'{indents}(alternate "{dequote(self.pinName)}" {self.electricalType} {self.graphicalStyle}){endline}'

@dataclass
class SymbolPin():
    """The ``pin`` token defines a pin in a symbol definition.

    Documentation:
        https://dev-docs.kicad.org/en/file-formats/sexpr-intro/index.html#_symbol_pin
    """

    electricalType: str = "input"
    """The ``electricalType`` defines the pin electrical connection. See documentation below for
    valid pin electrical connection types and descriptions."""

    graphicalStyle: str = "line"
    """The ``graphicalStyle`` defines the graphical style used to draw the pin. See documentation
    below for valid pin graphical styles and descriptions."""

    position: Position = field(default_factory=lambda: Position())
    """The ``position`` defines the X and Y coordinates and rotation angle of the connection point
    of the pin relative to the symbol origin position"""

    length: float = 0.254
    """The ``length`` token attribute defines the LENGTH of the pin"""

    name: str = ""
    """The ``name`` token defines a string containing the name of the pin"""

    nameEffects: Optional[Effects] = None
    """The optional ``nameEffects`` token define how the pin's name is displayed. This token is
    mandatory for KiCad v6 and was made optional since KiCad v7."""

    number: str = "0"
    """The ``number`` token defines a string containing the NUMBER of the pin"""

    numberEffects: Optional[Effects] = None
    """The optional ``numberEffects`` token define how the pin's number is displayed. This token is
    mandatory for KiCad v6 and was made optional since KiCad v7."""

    hide: bool = False      # Missing in documentation
    """The 'hide' token defines if the pin should be hidden"""

    alternatePins: List[SymbolAlternativePin] = field(default_factory=list)
    """The 'alternate' token defines one or more alternative definitions for the symbol pin"""

    @classmethod
    def from_sexpr(cls, exp: list) -> SymbolPin:
        """Convert the given S-Expresstion into a SymbolPin object

        Args:
            - exp (list): Part of parsed S-Expression ``(pin ...)``

        Raises:
            - Exception: When given parameter's type is not a list
            - Exception: When the first item of the list is not pin

        Returns:
            - SymbolPin: Object of the class initialized with the given S-Expression
        """
        if not isinstance(exp, list):
            raise Exception("Expression does not have the correct type")

        if exp[0] != 'pin':
            raise Exception("Expression does not have the correct type")

        object = cls()
        object.electricalType = exp[1]
        object.graphicalStyle = exp[2]
        for item in exp[3:]:
            if type(item) != type([]):
                if item == 'hide': object.hide = True
                else: continue
            if item[0] == 'at': object.position = Position().from_sexpr(item)
            if item[0] == 'length': object.length = item[1]
            if item[0] == 'name':
                object.name = item[1]
                if len(item) > 2:
                    object.nameEffects = Effects().from_sexpr(item[2])
            if item[0] == 'number':
                object.number = item[1]
                if len(item) > 2:
                    object.numberEffects = Effects().from_sexpr(item[2])
            if item[0] == 'alternate': object.alternatePins.append(SymbolAlternativePin().from_sexpr(item))
        return object

    def to_sexpr(self, indent: int = 4, newline: bool = True) -> str:
        """Generate the S-Expression representing this object

        Args:
            - indent (int): Number of whitespaces used to indent the output. Defaults to 4.
            - newline (bool): Adds a newline to the end of the output. Defaults to True.

        Returns:
            - str: S-Expression of this object
        """
        indents = ' '*indent
        endline = '\n' if newline else ''
        newLineAdded = False

        hide = ' hide' if self.hide else ''
        posA = f' {self.position.angle}' if self.position.angle is not None else ''
        nameEffects = f' {self.nameEffects.to_sexpr(newline=False)}' if self.nameEffects is not None else ''
        numberEffects = f' {self.numberEffects.to_sexpr(newline=False)}' if self.numberEffects is not None else ''

        expression =  f'{indents}(pin {self.electricalType} {self.graphicalStyle} (at {self.position.X} {self.position.Y}{posA}) (length {self.length}){hide}'
        
        # Since KiCad v7 nightly: Missing name and number effects print both other tokens into 
        # the same line.
        # Constrained in: schematic/since_v7/test_symbolPinOptionalTokens
        if self.nameEffects is None and self.numberEffects is None:
            expression += f' (name "{dequote(self.name)}") (number "{dequote(self.number)}")'
        else:
            expression += f'\n{indents}  (name "{dequote(self.name)}"{nameEffects})\n'
            expression += f'{indents}  (number "{dequote(self.number)}"{numberEffects})\n'
            newLineAdded = True

        # Alternative pins always generate a line break
        if self.alternatePins:
            if not newLineAdded:
                expression += '\n' 
            newLineAdded = True
            for alternativePin in self.alternatePins:
                expression += alternativePin.to_sexpr(indent+2)

        if newLineAdded:
            expression += f'{indents}){endline}'
        else:
            expression += f'){endline}'
        return expression

@dataclass
class Symbol():
    """The ``symbol`` token defines a symbol or sub-unit of a parent symbol. There can be zero or more
    ``symbol`` tokens in a symbol library file.

    Documentation:
        https://dev-docs.kicad.org/en/file-formats/sexpr-intro/index.html#_symbols
    """

    """Each symbol must have """
    @property
    def libId(self) -> str:
        """The ``lib_id`` token defines a unique "LIBRARY_ID" for each top level symbol in the
        library or a unique "UNIT_ID" for each unit embedded in a parent symbol. Library identifiers
        are only valid it top level symbols and unit identifiers are on valid as unit symbols inside
        a parent symbol. 
        
        The following conventions apply:
            - "LIBRARY_ID" (top-level symbol): ``[<libraryNickname>:]<entryName>`` (the library 
              nickname part is optional here)
            - "UNIT_ID" (child symbol): ``<entryName>_<unitId>_<styleId>``

        In ``kiutils``, the ``lib_id`` token is a combination of ``libraryNickname``, ``entryName``,
        ``unitId`` and ``styleId`` tokens. Setting the ``lib_id`` token will update all those tokens
        accordingly.

        Returns:
            - If the ``libraryNickname`` is set: ``<libraryNickname>:<entryName>``
            - If the ``libraryNickname`` is ``None``: ``<entryName>`` or ``<entryName>_<unitId>_<styleId>``,
              depending if these tokens are set.
        """
        if (self.unitId is not None and self.styleId is not None):
            unit_style_ids = f"_{self.unitId}_{self.styleId}"
        else:
            unit_style_ids = ""

        if self.libraryNickname:
            return f'{self.libraryNickname}:{self.entryName}'
        else:
            return f'{self.entryName}{unit_style_ids}'

    @libId.setter
    def libId(self, symbol_id: str):
        """Sets the ``lib_id`` token and parses its contents into the ``libraryNickname``,
        ``entryName``, ``unitId`` and ``styleId`` token. 

        See self.libId property description for more information.
        
        Args:
            - symbol_id (str): The symbol id in the following format: ``<libraryNickname>:<entryName>``,
              ``<entryName>_<unitId>_<styleId>`` or only ``<entryName>``, depending on if the symbol
              is a top-level symbol or a child symbol

        Raises:
            - Exception: If the given ID is neither a top-level nor a child symbol
        """
        # Try to parse the given ID
        parse_symbol_id = re.match(r"^(.+?):(.+?)$", symbol_id)
        if parse_symbol_id:
            # The symbol is a top-level symbol with a library nickname
            self.libraryNickname = parse_symbol_id.group(1)
            self.entryName = parse_symbol_id.group(2)
            self.unitId = None
            self.styleId = None
        else:
            parse_symbol_id = re.match(r"^(.+?)_(\d+?)_(\d+?)$", symbol_id)
            if parse_symbol_id:
                # The symbol is a child symbol
                self.libraryNickname = None
                self.entryName = parse_symbol_id.group(1)
                self.unitId = int(parse_symbol_id.group(2))
                self.styleId = int(parse_symbol_id.group(3))
            else:
                # The symbol is a top-level symbol without a library nickname
                self.libraryNickname = None
                self.entryName = symbol_id
                self.unitId = None
                self.styleId = None

        # Update units id to match parent id
        for unit in self.units:
            unit.entryName = self.entryName

    libraryNickname: Optional[str] = None
    """The optional ``libraryNickname`` token defines which symbol library this symbol belongs to
    and is a part of the ``id`` token"""
    
    entryName: str = None
    """The ``entryName`` token defines the actual name of the symbol and is a part of the ``id`` 
    token"""

    unitId: Optional[int] = None
    """The ``unitId`` token identifies which unit the symbol represents and is a part of 
    the ``id`` token"""

    styleId: Optional[int] = None
    """The ``styleId`` token indicates which body style the unit represents and is a part of the 
    ``id`` token"""

    extends: Optional[str] = None
    """The optional ``extends`` token attribute defines the "LIBRARY_ID" of another symbol inside the
    current library from which to derive a new symbol. Extended symbols currently can only have
    different symbol properties than their parent symbol."""

    hidePinNumbers: bool = False
    """The ``pin_numbers`` token defines the visibility setting of the symbol pin numbers for
    the entire symbol. If set to False, the all of the pin numbers in the symbol are visible."""

    pinNames: bool = False
    """The optional ``pinNames`` token defines the attributes for all of the pin names of the symbol.
    If the ``pinNames`` token is not defined, all symbol pins are shown with the default offset."""

    pinNamesHide: bool = False
    """The optional ``pinNamesOffset`` token defines the pin name of all pins should be hidden"""

    pinNamesOffset: Optional[float] = None
    """The optional ``pinNamesOffset`` token defines the pin name offset for all pin names of the
    symbol. If not defined, the pin name offset is 0.508mm (0.020")"""

    inBom: Optional[bool] = None
    """The optional ``inBom`` token, defines if a symbol is to be include in the bill of material
    output. If undefined, the token will not be generated in `self.to_sexpr()`."""

    onBoard: Optional[bool] = None
    """The ``onBoard`` token, defines if a symbol is to be exported from the schematic to the printed
    circuit board. If undefined, the token will not be generated in `self.to_sexpr()`."""

    # TODO: Describe this token
    isPower: bool = False           # Missing in documentation, added when "Als Spannungssymbol" is checked
    """The ``isPower`` token's documentation was not done yet .."""

    properties: List[Property] = field(default_factory=list)
    """The ``properties`` is a list of properties that define the symbol. The following properties are
    mandatory when defining a parent symbol: "Reference", "Value", "Footprint", and "Datasheet".
    All other properties are optional. Unit symbols cannot have any properties."""

    graphicItems: List = field(default_factory=list)
    """The ``graphicItems`` section is list of graphical arcs, circles, curves, lines, polygons, 
    rectangles, text and text boxes that define the symbol drawing. Possible items are defined in 
    ``kiutils.items.syitems``. This section can be empty if the symbol has no graphical items."""

    pins: List[SymbolPin] = field(default_factory=list)
    """The ``pins`` section is a list of pins that are used by the symbol. This section can be empty if
    the symbol does not have any pins."""

    units: List[Symbol] = field(default_factory=list)
    """The ``units`` can be one or more child symbol tokens embedded in a parent symbol"""

    @classmethod
    def from_sexpr(cls, exp: list) -> Symbol:
        """Convert the given S-Expression into a Symbol object

        Args:
            - exp (list): Part of parsed S-Expression ``(symbol ...)``

        Raises:
            - Exception: When given parameter's type is not a list
            - Exception: When the first item of the list is not symbol

        Returns:
            - Symbol: Object of the class initialized with the given S-Expression
        """
        if not isinstance(exp, list):
            raise Exception("Expression does not have the correct type")

        if exp[0] != 'symbol':
            raise Exception("Expression does not have the correct type")

        object = cls()
        object.libId = exp[1]
        for item in exp[2:]:
            if item[0] == 'extends': object.extends = item[1]
            if item[0] == 'pin_numbers':
                if item[1] == 'hide':
                    object.hidePinNumbers = True
            if item[0] == 'pin_names':
                object.pinNames = True
                for property in item[1:]:
                    if type(property) == type([]):
                        if property[0] == 'offset': object.pinNamesOffset = property[1]
                    else:
                        if property == 'hide': object.pinNamesHide = True
            if item[0] == 'in_bom': object.inBom = True if item[1] == 'yes' else False
            if item[0] == 'on_board': object.onBoard = True if item[1] == 'yes' else False
            if item[0] == 'power': object.isPower = True

            if item[0] == 'symbol': object.units.append(Symbol().from_sexpr(item))
            if item[0] == 'property': object.properties.append(Property().from_sexpr(item))

            if item[0] == 'pin': object.pins.append(SymbolPin().from_sexpr(item))
            if item[0] == 'arc': object.graphicItems.append(SyArc().from_sexpr(item))
            if item[0] == 'circle': object.graphicItems.append(SyCircle().from_sexpr(item))
            if item[0] == 'curve': object.graphicItems.append(SyCurve().from_sexpr(item))
            if item[0] == 'polyline': object.graphicItems.append(SyPolyLine().from_sexpr(item))
            if item[0] == 'rectangle': object.graphicItems.append(SyRect().from_sexpr(item))
            if item[0] == 'text': object.graphicItems.append(SyText().from_sexpr(item))
            if item[0] == 'text_box': object.graphicItems.append(SyTextBox().from_sexpr(item))

        return object

    @classmethod
    def create_new(cls, id: str, reference: str, value: str,
                        footprint: str = "", datasheet: str = "") -> Symbol:
        """Creates a new empty symbol as KiCad would create it

        Args:
            - id (str): ID token of the symbol
            - reference (str): Reference designator
            - value (str): Value of the ``value`` property
            - footprint (str): Value of the ``footprint`` property. Defaults to "" (empty string).
            - datasheet (str): Value of the ``datasheet`` property. Defaults to "" (empty string).

        Returns:
            - Symbol: New symbol initialized with default values
        """
        symbol = cls()
        symbol.inBom = True
        symbol.onBoard = True
        symbol.libId = id
        symbol.properties.extend(
            [
                Property(key = "Reference", value = reference, id = 0,
                         effects = Effects(font=Font(width=1.27, height=1.27))),
                Property(key = "Value", value = value, id = 1,
                         effects = Effects(font=Font(width=1.27, height=1.27))),
                Property(key = "Footprint", value = footprint, id = 2,
                         effects = Effects(font=Font(width=1.27, height=1.27), hide=True)),
                Property(key = "Datasheet", value = datasheet, id = 3,
                         effects = Effects(font=Font(width=1.27, height=1.27), hide=True))
            ]
        )
        return symbol

    def to_sexpr(self, indent: int = 2, newline: bool = True) -> str:
        """Generate the S-Expression representing this object

        Args:
            - indent (int): Number of whitespaces used to indent the output. Defaults to 2.
            - newline (bool): Adds a newline to the end of the output. Defaults to True.

        Returns:
            - str: S-Expression of this object
        """
        indents = ' '*indent
        endline = '\n' if newline else ''
        obtext, ibtext = '', ''

        if self.inBom is not None:
            ibtext = 'yes' if self.inBom else 'no'
        inbom = f' (in_bom {ibtext})' if self.inBom is not None else ''
        if self.onBoard is not None:
            obtext = 'yes' if self.onBoard else 'no'
        onboard = f' (on_board {obtext})' if self.onBoard is not None else ''
        power = f' (power)' if self.isPower else ''
        pnhide = f' hide' if self.pinNamesHide else ''
        pnoffset = f' (offset {self.pinNamesOffset})' if self.pinNamesOffset is not None else ''
        pinnames = f' (pin_names{pnoffset}{pnhide})' if self.pinNames else ''
        pinnumbers = f' (pin_numbers hide)' if self.hidePinNumbers else ''
        extends = f' (extends "{dequote(self.extends)}")' if self.extends is not None else ''

        expression =  f'{indents}(symbol "{dequote(self.libId)}"{extends}{power}{pinnumbers}{pinnames}{inbom}{onboard}\n'
        for item in self.properties:
            expression += item.to_sexpr(indent+2)
        for item in self.graphicItems:
            expression += item.to_sexpr(indent+2)
        for item in self.pins:
            expression += item.to_sexpr(indent+2)
        for item in self.units:
            expression += item.to_sexpr(indent+2)
        expression += f'{indents}){endline}'
        return expression

@dataclass
class SchematicLibSymbol(Symbol):
    """The ``symbol`` token defines a symbol or sub-unit of a parent symbol. There can be zero or more
    ``symbol`` tokens in a symbol library file.

    Documentation:
        https://dev-docs.kicad.org/en/file-formats/sexpr-intro/index.html#_symbols
    """

    """Each symbol must have """
    @property
    def libId(self) -> str:
        """The ``lib_id`` token defines a unique "LIBRARY_ID" for each top level symbol in the
        library or a unique "UNIT_ID" for each unit embedded in a parent symbol. Library identifiers
        are only valid it top level symbols and unit identifiers are on valid as unit symbols inside
        a parent symbol.

        The following conventions apply:
            - "LIBRARY_ID" (top-level symbol): ``[<libraryNickname>:]<entryName>`` (the library
              nickname part is optional here)

        In ``kiutils``, the ``lib_id`` token is a combination of ``libraryNickname``, ``entryName``,
        ``unitId`` and ``styleId`` tokens. Setting the ``lib_id`` token will update all those tokens
        accordingly.

        Returns:
            - If the ``libraryNickname`` is set: ``<libraryNickname>:<entryName>``
            - If the ``libraryNickname`` is ``None``: ``<entryName>``
              depending if these tokens are set.
        """
        if (self.unitId is not None and self.styleId is not None):
            unit_style_ids = f"_{self.unitId}_{self.styleId}"
        else:
            unit_style_ids = ""

        if self.libraryNickname:
            return f'{self.libraryNickname}:{self.entryName}'
        else:
            return f'{self.entryName}{unit_style_ids}'

    @libId.setter
    def libId(self, symbol_id: str):
        """Sets the ``lib_id`` token and parses its contents into the ``libraryNickname``,
        ``entryName`` and ``styleId`` token.

        See self.libId property description for more information.

        Args:
            - symbol_id (str): The symbol id in the following format: ``<libraryNickname>:<entryName>``
              or only ``<entryName>``, depending on if the symbol
              is a top-level symbol or a child symbol

        Raises:
            - Exception: If the given ID is neither a top-level nor a child symbol
        """
        # Try to parse the given ID
        parse_symbol_id = re.match(r"^(.+?):(.+?)$", symbol_id)
        if parse_symbol_id:
            # The symbol is a top-level symbol with a library nickname
            self.libraryNickname = parse_symbol_id.group(1)
            self.entryName = parse_symbol_id.group(2)
            self.unitId = None
            self.styleId = None
        else:
            # The symbol is a top-level symbol without a library nickname
            self.libraryNickname = None
            self.entryName = symbol_id
            self.unitId = None
            self.styleId = None

        # Update units id to match parent id
        for unit in self.units:
            unit.entryName = self.entryName



@dataclass
class SymbolLib():
    """A symbol library defines the common format of ``.kicad_sym`` files. A symbol library may contain
    zero or more symbols.

    Documentation:
        https://dev-docs.kicad.org/en/file-formats/sexpr-symbol-lib/
    """
    version: str = KIUTILS_CREATE_NEW_VERSION_STR
    """The ``version`` token attribute defines the symbol library version using the YYYYMMDD date format"""

    generator: Optional[str] = None
    """The ``generator`` token attribute defines the program used to write the file"""

    symbols: List[Symbol] = field(default_factory=list)
    """The ``symbols`` token defines a list of zero or more symbols that are part of the symbol library"""

    filePath: Optional[str] = None
    """The ``filePath`` token defines the path-like string to the library file. Automatically set when
    ``self.from_file()`` is used. Allows the use of ``self.to_file()`` without parameters."""

    @classmethod
    def from_file(cls, filepath: str, encoding: Optional[str] = None) -> SymbolLib:
        """Load a symbol library directly from a KiCad footprint file (`.kicad_sym`) and sets the
        ``self.filePath`` attribute to the given file path.

        Args:
            - filepath (str): Path or path-like object that points to the file
            - encoding (str, optional): Encoding of the input file. Defaults to None (platform
                                        dependent encoding).

        Raises:
            - Exception: If the given path is not a file

        Returns:
            - SymbolLib: Object of the SymbolLib class initialized with the given KiCad symbol library
        """
        if not path.isfile(filepath):
            raise Exception("Given path is not a file!")

        with open(filepath, 'r', encoding=encoding) as infile:
            item = cls.from_sexpr(sexpr.parse_sexp(infile.read()))
            item.filePath = filepath
            return item

    @classmethod
    def from_sexpr(cls, exp: list) -> SymbolLib:
        """Convert the given S-Expresstion into a SymbolLib object

        Args:
            - exp (list): Part of parsed S-Expression ``(kicad_symbol_lib ...)``

        Raises:
            - Exception: When given parameter's type is not a list
            - Exception: When the first item of the list is not kicad_symbol_lib

        Returns:
            - SymbolLib: Object of the class initialized with the given S-Expression
        """
        if not isinstance(exp, list):
            raise Exception("Expression does not have the correct type")

        if exp[0] != 'kicad_symbol_lib':
            raise Exception("Expression does not have the correct type")

        object = cls()

        for item in exp[1:]:
            if item[0] == 'version': object.version = item[1]
            if item[0] == 'generator': object.generator = item[1]
            if item[0] == 'symbol': object.symbols.append(Symbol().from_sexpr(item))
        return object

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

    def to_sexpr(self, indent: int = 0, newline: bool = True) -> str:
        """Generate the S-Expression representing this object

        Args:
            - indent (int): Number of whitespaces used to indent the output. Defaults to 0.
            - newline (bool): Adds a newline to the end of the output. Defaults to True.

        Returns:
            - str: S-Expression of this object
        """
        indents = ' '*indent
        endline = '\n' if newline else ''

        expression =  f'{indents}(kicad_symbol_lib (version {self.version}) (generator {self.generator})\n'
        for item in self.symbols:
            expression += f'{indents}{item.to_sexpr(indent+2)}'
        expression += f'{indents}){endline}'
        return expression
