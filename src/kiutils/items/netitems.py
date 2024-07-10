"""Defines items used in KiCad eeschema netlist export

Author:
    (C) Ashton Snelgrove - @yashton - 2024

License identifier:
    GPL-3.0

Major changes:
    10.07.2024 - created

Documentation taken from:
    https://docs.kicad.org/master/en/eeschema/eeschema.html#intermediate-netlist-structure
"""
from dataclasses import dataclass, field
from typing import Optional, List, Union
from kiutils.utils import sexpr
from kiutils.utils.strings import dequote
from os import path

@dataclass
class NetlistTitleBlock():
    company: Optional[str] = None
    title: Optional[str] = None
    name: Optional[str] = None
    rev: Optional[str] = None
    date: Optional[str] = None
    source: str = ""
    comments: List[str] = field(default_factory=lambda: [None for _ in range(0,9)])

    @classmethod
    def from_sexpr(cls, exp: list):
        """Convert the given S-Expression into a Schematic object

        Args:
            - exp (list): Part of parsed S-Expression ``(title_block ...)``

        Raises:
            - Exception: When given parameter's type is not a list
            - Exception: When the first item of the list is not title_block

        Returns:
            - Schematic: Object of the class initialized with the given S-Expression
        """
        if not isinstance(exp, list):
            raise Exception("Expression does not have the correct type")

        if exp[0] != 'title_block':
            raise Exception(f"Expression does not have the correct type: '{exp[0]}'")

        object = cls()
        for item in exp[1:]:
            if item[0] == 'title' and len(item) > 1: object.title = item[1]
            elif item[0] == 'company' and len(item) > 1: object.company = datetime.strptime(item[1])
            elif item[0] == 'rev' and len(item) > 1: object.rev = item[1]
            elif item[0] == 'date' and len(item) > 1: object.date = item[1]
            elif item[0] == 'source': object.source = item[1]
            elif item[0] == 'comment':
                index = -1
                for sub in item[1:]:
                    if sub[0] == "number":
                        index = int(sub[1]) - 1
                    if sub[0] == "value":
                        comment = sub[1]
                if index == -1:
                    raise Exception("Missing comment number")
                object.comments[index] = comment
        return object

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

        expression =  f'{indents}(title_block\n'
        if self.title is not None:
            expression += f'{indents}  (title "{dequote(self.title)}")\n'
        else:
            expression += f'{indents}  (title)\n'

        if self.company is not None:
            expression += f'{indents}  (company "{dequote(self.company)}")\n'
        else:
            expression += f'{indents}  (company)\n'

        if self.rev is not None:
            expression += f'{indents}  (rev "{dequote(self.rev)}")\n'
        else:
            expression += f'{indents}  (rev)\n'

        if self.date is not None:
            expression += f'{indents}  (date "{dequote(self.date)}")\n'
        else:
            expression += f'{indents}  (date)\n'

        expression += f'{indents}  (source "{dequote(self.source)}")\n'
        for i, comment in enumerate(self.comments):
            expression += f'{indents}  (comment (number "{i+1}") (value "{dequote(comment)}"))\n'

        expression += f'{indents}){endline}'
        return expression

@dataclass
class NetlistSheet():
    """A hierarchical sheet in the design"""
    number: str = ""
    """Sheet numeric identifier"""

    name: str = ""
    """Sheet name"""

    tstamps: str = ""
    """Unique identifier of the sheet"""

    title_block: NetlistTitleBlock = field(default_factory=lambda: NetlistTitleBlock())
    """Title block with renderable sheet information"""

    @classmethod
    def from_sexpr(cls, exp: list):
        """Convert the given S-Expression into a Schematic object

        Args:
            - exp (list): Part of parsed S-Expression ``(sheet ...)``

        Raises:
            - Exception: When given parameter's type is not a list
            - Exception: When the first item of the list is not sheet

        Returns:
            - Schematic: Object of the class initialized with the given S-Expression
        """
        if not isinstance(exp, list):
            raise Exception("Expression does not have the correct type")

        if exp[0] != 'sheet':
            raise Exception(f"Expression does not have the correct type: '{exp[0]}'")

        object = cls()
        for item in exp[1:]:
            if item[0] == 'number': object.number = item[1]
            elif item[0] == 'name': object.name = item[1]
            elif item[0] == 'tstamps': object.tstamps = item[1]
            elif item[0] == 'title_block':
                object.title_block = NetlistTitleBlock().from_sexpr(item)
        return object

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

        expression =  f'{indents}(sheet'
        expression += f' (number "{dequote(self.number)}")'
        expression += f' (name "{dequote(self.name)}")'
        expression += f' (tstamps "{dequote(self.tstamps)}")\n'
        expression += self.title_block.to_sexpr(indent+2)
        expression += f'{indents}){endline}'
        return expression

@dataclass
class NetlistDesign():
    """The header section of the export. This section can be considered a comment.

    Documentation:
    https://docs.kicad.org/master/en/eeschema/eeschema.html#the-nets-section
    """

    source: str = ""
    """The ``source`` is the filename of the original schematic file"""

    date: str = ""
    """The timestamp of the export.
       The date format found in a local example on Linux is almost ISO8601 format, but seems to be missing the colon in the timezone. The date format in the eeschema documentation is more like the output of the unix `date` command. Without clear documentation of expected format, this is left as a string."""

    tool: str = ""
    """Identifier for the toola and version that did the export (usually eeschema)"""

    sheets: List[NetlistSheet] = field(default_factory=list)
    """List of sheet information. Not documented in the eeschema documentation for the XML format, but is present in the example netlist and generated netlists."""

    @classmethod
    def from_sexpr(cls, exp: list):
        """Convert the given S-Expression into a Schematic object

        Args:
            - exp (list): Part of parsed S-Expression ``(design ...)``

        Raises:
            - Exception: When given parameter's type is not a list
            - Exception: When the first item of the list is not design

        Returns:
            - Schematic: Object of the class initialized with the given S-Expression
        """
        if not isinstance(exp, list):
            raise Exception("Expression does not have the correct type")

        if exp[0] != 'design':
            raise Exception(f"Expression does not have the correct type: '{exp[0]}'")

        object = cls()
        for item in exp[1:]:
            if item[0] == 'source': object.source = item[1]

            elif item[0] == 'date':
                object.date = item[1]
            elif item[0] == 'tool': object.tool = item[1]
            elif item[0] == 'sheet':
                object.sheets.append(NetlistSheet().from_sexpr(item))
        return object

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

        expression =  f'{indents}(design\n'
        expression += f'{indents}  (source "{dequote(self.source)}")\n'
        expression += f'{indents}  (date "{dequote(self.date)}")\n'
        expression += f'{indents}  (tool "{dequote(self.tool)}")\n'
        for sheet in self.sheets:
            expression += sheet.to_sexpr(indent+2)
        expression += f'{indents}){endline}'
        return expression

@dataclass
class NetlistLibsource():
    lib: str = ""
    """Logical library name"""

    part: str = ""
    """Symbol identifier"""

    description: str = ""
    """Symbol description"""

    @classmethod
    def from_sexpr(cls, exp: list):
        """Convert the given S-Expression into a Schematic object

        Args:
            - exp (list): Part of parsed S-Expression ``(libsource ...)``

        Raises:
            - Exception: When given parameter's type is not a list
            - Exception: When the first item of the list is not libsource

        Returns:
            - Schematic: Object of the class initialized with the given S-Expression
        """
        if not isinstance(exp, list):
            raise Exception("Expression does not have the correct type")

        if exp[0] != 'libsource':
            raise Exception(f"Expression does not have the correct type: '{exp[0]}'")

        object = cls()
        for item in exp[1:]:
            if item[0] == 'lib': object.lib = item[1]
            elif item[0] == 'part': object.part = item[1]
            elif item[0] == 'description': object.description = item[1]
        return object

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
        return f'{indents}(libsource (lib "{dequote(self.lib)}") (part "{dequote(self.part)}") (description "{dequote(self.description)}")){endline}'


@dataclass
class NetlistSheetpath():
    names: str = ""
    tstamps: str = ""
    @classmethod
    def from_sexpr(cls, exp: list):
        """Convert the given S-Expression into a Schematic object

        Args:
            - exp (list): Part of parsed S-Expression ``(sheetpath ...)``

        Raises:
            - Exception: When given parameter's type is not a list
            - Exception: When the first item of the list is not sheetpath

        Returns:
            - Schematic: Object of the class initialized with the given S-Expression
        """
        if not isinstance(exp, list):
            raise Exception("Expression does not have the correct type")

        if exp[0] != 'sheetpath':
            raise Exception(f"Expression does not have the correct type: '{exp[0]}'")

        object = cls()
        for item in exp[1:]:
            if item[0] == 'names': object.names = item[1]
            elif item[0] == 'tstamps': object.tstamps = item[1]
        return object

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

        expression =  f'{indents}(sheetpath'
        expression += f' (names "{dequote(self.names)}")'
        expression += f' (tstamps "{dequote(self.tstamps)}")'
        expression += f'){endline}'
        return expression

@dataclass
class NetlistField():
    name: str = ""
    value: Optional[str] = None

    @classmethod
    def from_sexpr(cls, exp: list):
        """Convert the given S-Expression into a Schematic object

        Args:
            - exp (list): Part of parsed S-Expression ``(field ...)``

        Raises:
            - Exception: When given parameter's type is not a list
            - Exception: When the first item of the list is not field

        Returns:
            - Schematic: Object of the class initialized with the given S-Expression
        """
        if not isinstance(exp, list):
            raise Exception("Expression does not have the correct type")

        if exp[0] != 'field':
            raise Exception(f"Expression does not have the correct type: '{exp[0]}'")

        object = cls()
        for item in exp[1:]:
            if item[0] == 'name': object.name = item[1]
            else: object.value = item
        return object

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
        value = f' "{dequote(self.value)}"' if self.value else ''
        return f'{indents}(field (name "{dequote(self.name)}"){value}){endline}'

@dataclass
class NetlistProperty():
    name: str = ""
    value: str = ""
    @classmethod
    def from_sexpr(cls, exp: list):
        """Convert the given S-Expression into a Schematic object

        Args:
            - exp (list): Part of parsed S-Expression ``(property ...)``

        Raises:
            - Exception: When given parameter's type is not a list
            - Exception: When the first item of the list is not property

        Returns:
            - Schematic: Object of the class initialized with the given S-Expression
        """
        if not isinstance(exp, list):
            raise Exception("Expression does not have the correct type")

        if exp[0] != 'property':
            raise Exception(f"Expression does not have the correct type: '{exp[0]}'")

        object = cls()
        for item in exp[1:]:
            if item[0] == 'name': object.name = item[1]
            elif item[0] == 'value': object.value = item[1]
        return object

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
        return f'{indents}(property (name "{dequote(self.name)}") (value "{dequote(self.value)}")){endline}'

@dataclass
class NetlistComponent():
    """A component from the schematic"""

    ref: str = ""
    """The component reference field from the schematic"""
    value: str = ""
    """The component value field from the schematic"""
    tstamps: str = ""
    """The timestamp reference is used as unique id for each component"""
    libsource: NetlistLibsource = field(default_factory=lambda: NetlistLibsource())
    """The name of the lib where this component was found."""
    sheetpath: NetlistSheetpath = field(default_factory=lambda: NetlistSheetpath())
    """The path of the sheet inside the hierarchy: identify the sheet within the full schematic hierarchy."""
    fields: List[NetlistField] = field(default_factory=list)
    """The symbol field key/value pairs."""
    properties: List[NetlistProperty] = field(default_factory=list)
    """A second set of key/value pairs. Appears to include copies of everything in the ``fields`` set plus "Sheetname" and "Sheetfile" pairs."""

    @classmethod
    def from_sexpr(cls, exp: list):
        """Convert the given S-Expression into a Component object
    https://docs.kicad.org/master/en/eeschema/eeschema.html#the-components-section
        Args:
            - exp (list): Part of parsed S-Expression ``(comp ...)``

        Raises:
            - Exception: When given parameter's type is not a list
            - Exception: When the first item of the list is not comp

        Returns:
            - Schematic: Object of the class initialized with the given S-Expression
        """
        if not isinstance(exp, list):
            raise Exception("Expression does not have the correct type")

        if exp[0] != 'comp':
            raise Exception(f"Expression does not have the correct type: '{exp[0]}'")

        object = cls()
        for item in exp[1:]:
            if item[0] == 'ref': object.ref = item[1]
            elif item[0] == 'value': object.value = item[1]
            elif item[0] == 'tstamps': object.tstamps = item[1]
            elif item[0] == 'libsource': object.libsource = NetlistLibsource.from_sexpr(item)
            elif item[0] == 'sheetpath': object.sheetpath = NetlistSheetpath.from_sexpr(item)
            elif item[0] == 'fields':
                for field in item[1:]:
                    object.fields.append(NetlistField().from_sexpr(field))
            elif item[0] == 'property':
                object.properties.append(NetlistProperty().from_sexpr(item))

        return object

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

        expression =  f'{indents}(comp'
        expression += f' (ref "{dequote(self.ref)}")\n'
        expression += f'{indents}  (value "{dequote(self.value)}")\n'
        if len(self.fields) > 0:
            expression += f'{indents}  (fields\n'
            for field in self.fields:
                expression += field.to_sexpr(indent+4)
            expression += f'{indents} )\n'
        expression += self.libsource.to_sexpr(indent+2)
        for prop in self.properties:
            expression += prop.to_sexpr(indent+2)

        expression += self.sheetpath.to_sexpr(indent+2)
        expression += f'{indents}  (tstamps "{dequote(self.tstamps)}")\n'
        expression += f'{indents}){endline}'
        return expression

@dataclass
class NetlistLibrary():
    """
    The location of the library files that parts are derived from.
    https://docs.kicad.org/master/en/eeschema/eeschema.html#the-libraries-section"""
    logical: str = ""
    """The identifier used by part listings."""
    uri: str = ""
    """The file location of the symbol file."""

    @classmethod
    def from_sexpr(cls, exp: list):
        if not isinstance(exp, list):
            raise Exception("Expression does not have the correct type")

        if exp[0] != 'library':
            raise Exception(f"Expression does not have the correct type: '{exp[0]}'")

        object = cls()
        for item in exp[1:]:
            if item[0] == 'logical': object.logical = item[1]
            elif item[0] == 'uri': object.uri = item[1]
        return object

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
        expression = f'{indents}(library (logical "{dequote(self.logical)}")\n'
        expression += f'{indents}  (uri "{dequote(self.uri)}")){endline}'
        return expression
@dataclass
class NetlistLibpartPin():
    num: str = ""
    """Numeric identifier of pin. This is used in the nets section."""

    name: str = ""
    """String identifier of pin."""

    pintype: str = ""
    """One of `input`, `output`, `inout`, `tristate`, or `passive`"""

    pinfunction: Optional[str] = None
    """Optional function id"""

    @classmethod
    def from_sexpr(cls, exp: list):
        """Convert the given S-Expression into a Schematic object

        Args:
            - exp (list): Part of parsed S-Expression ``(pin ...)``

v        Raises:
            - Exception: When given parameter's type is not a list
            - Exception: When the first item of the list is not pin

        Returns:
            - Schematic: Object of the class initialized with the given S-Expression
        """
        if not isinstance(exp, list):
            raise Exception("Expression does not have the correct type")

        if exp[0] != 'pin':
            raise Exception(f"Expression does not have the correct type: '{exp[0]}'")

        object = cls()
        for item in exp[1:]:
            if item[0] == 'name': object.name = item[1]
            elif item[0] == 'num': object.num = item[1]
            elif item[0] == 'type': object.pintype = item[1]
            elif item[0] == 'pinfunction': object.pinfunction = item[1]
        return object

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

        expression =  f'{indents}(pin'
        expression += f' (num "{dequote(self.num)}")'
        expression += f' (name "{dequote(self.name)}")'
        expression += f' (type "{dequote(self.pintype)}")'
        if self.pinfunction is not None:
            expression += f' (pinfunction "{dequote(self.pinfunction)}")'
        expression += f'){endline}'
        return expression

@dataclass
class NetlistLibpart():
    lib: str = ""
    """The logical name from the libraries section."""

    part: str = ""
    """The symbol name"""

    footprints: List[str] = field(default_factory=list)
    """The footprint filters used to define which footprints are appropriate to use with the symbol."""

    fields: List[NetlistField] = field(default_factory=list)
    """The default fields associated with the symbol."""

    pins: List[NetlistLibpartPin] = field(default_factory=list)
    """The list of pins associated with the symbol"""

    @classmethod
    def from_sexpr(cls, exp: list):
        """Convert the given S-Expression into a Schematic object
https://docs.kicad.org/master/en/eeschema/eeschema.html#the-libparts-section
        Args:
            - exp (list): Part of parsed S-Expression ``(libpart ...)``

        Raises:
            - Exception: When given parameter's type is not a list
            - Exception: When the first item of the list is not libpart

        Returns:
            - Schematic: Object of the class initialized with the given S-Expression
        """
        if not isinstance(exp, list):
            raise Exception("Expression does not have the correct type")

        if exp[0] != 'libpart':
            raise Exception(f"Expression does not have the correct type: '{exp[0]}'")

        object = cls()
        for item in exp[1:]:
            if item[0] == 'lib': object.lib = item[1]
            elif item[0] == 'part': object.part = item[1]
            elif item[0] == 'footprints':
                for fp in item[1:]:
                    assert fp[0] == 'fp'
                    object.footprints.append(fp[1])
            elif item[0] == 'fields':
                for comp in item[1:]:
                    object.fields.append(NetlistField().from_sexpr(comp))
            elif item[0] == 'pins':
                for lib in item[1:]:
                    object.pins.append(NetlistLibpartPin().from_sexpr(lib))
        return object

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

        expression =  f'{indents}(libpart'
        expression += f' (lib "{dequote(self.lib)}")'
        expression += f' (part "{dequote(self.part)}")\n'
        if len(self.footprints) > 0:
            expression += f'{indents}  (footprints\n'
            for fp in self.footprints:
                expression += f'{indents}    (fp "{dequote(fp)}")\n'
            expression += f"{indents}  )\n"

        expression += f'{indents}  (fields\n'
        for field in self.fields:
            expression += field.to_sexpr(indent+4)
        expression += f"{indents}  )\n"

        expression += f'{indents}  (pins\n'
        for pin in self.pins:
            expression += pin.to_sexpr(indent+4)
        expression += f"{indents}  )\n"

        expression += f'{indents}){endline}'
        return expression



@dataclass
class NetlistNetNode():
    """A connection to a net"""

    ref: str = ""
    """Component reference id"""

    pin: str = ""
    """Pin number on the referenced component"""

    pintype: str = ""
    """Pin type of the connection"""

    pinfunction: Optional[str] = None
    """Pin function of the connection"""

    @classmethod
    def from_sexpr(cls, exp: list):
        """Convert the given S-Expression into a Schematic object

        Args:
            - exp (list): Part of parsed S-Expression ``(node ...)``

        Raises:
            - Exception: When given parameter's type is not a list
            - Exception: When the first item of the list is not node

        Returns:
            - Schematic: Object of the class initialized with the given S-Expression
        """
        if not isinstance(exp, list):
            raise Exception("Expression does not have the correct type")

        if exp[0] != 'node':
            raise Exception(f"Expression does not have the correct type: '{exp[0]}'")

        object = cls()
        for item in exp[1:]:

            if item[0] == 'pin': object.pin = item[1]
            elif item[0] == 'ref': object.ref = item[1]
            elif item[0] == 'pintype': object.pintype = item[1]
            elif item[0] == 'pinfunction': object.pinfunction = item[1]
        return object

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

        expression =  f'{indents}(node'
        expression += f' (ref "{dequote(self.ref)}")'
        expression += f' (pin "{dequote(self.pin)}")'
        if self.pinfunction is not None:
            expression += f' (pinfunction "{dequote(self.pinfunction)}")'
        if self.pintype is not None:
            expression += f' (pintype "{dequote(self.pintype)}")'
        expression += f'){endline}'
        return expression

@dataclass
class NetlistNet():
    """A net in the design. This section describes the connectivity of the schematic by listing all nets and the pins connected to each net.
    https://docs.kicad.org/master/en/eeschema/eeschema.html#the-nets-section
"""

    code: str = ""
    """an internal identifier for this net"""

    name: str = ""
    """The net name"""

    nodes: List[NetlistNetNode] = field(default_factory=list)
    """The pin (identified by pin) of a symbol (identified by ref) which is connected to the net"""

    @classmethod
    def from_sexpr(cls, exp: list):
        """Convert the given S-Expression into a Schematic object
        Args:
            - exp (list): Part of parsed S-Expression ``(net ...)``

        Raises:
            - Exception: When given parameter's type is not a list
            - Exception: When the first item of the list is not net

b        Returns:
            - Schematic: Object of the class initialized with the given S-Expression
        """
        if not isinstance(exp, list):
            raise Exception("Expression does not have the correct type")

        if exp[0] != 'net':
            raise Exception(f"Expression does not have the correct type: '{exp[0]}'")

        object = cls()
        for item in exp[1:]:
            if item[0] == 'code': object.code = item[1]
            elif item[0] == 'name': object.name = item[1]
            elif item[0] == 'node':
                object.nodes.append(NetlistNetNode().from_sexpr(item))
        return object

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

        expression =  f'{indents}(net'
        expression += f' (code "{dequote(self.code)}")'
        expression += f' (name "{dequote(self.name)}")\n'
        for node in self.nodes:
            expression += node.to_sexpr(indent+2)
        expression += f'{indents}){endline}'
        return expression
