"""Defines items used in KiCad schematic files

Author:
    (C) Marvin Mager - @mvnmgrx - 2022

License identifier:
    GPL-3.0

Major changes:
    19.02.2022 - created

Documentation taken from:
    https://dev-docs.kicad.org/en/file-formats/sexpr-schematic/
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Optional, List, Dict

from kiutils.items.common import Fill, Position, ColorRGBA, ProjectInstance, Stroke, Effects, Property
from kiutils.utils.strings import dequote

@dataclass
class Junction():
    """The ``junction`` token defines a junction in the schematic

    Documentation:
        https://dev-docs.kicad.org/en/file-formats/sexpr-schematic/#_junction_section
    """

    position: Position = field(default_factory=lambda: Position())
    """The ``position`` defines the X and Y coordinates of the junction"""

    diameter: float = 0
    """The ``diameter`` token attribute defines the DIAMETER of the junction. A diameter of 0
       is the default diameter in the system settings."""

    color: ColorRGBA = field(default_factory=lambda: ColorRGBA())
    """The ``color`` token attributes define the Red, Green, Blue, and Alpha transparency of
       the junction. If all four attributes are 0, the default junction color is used."""

    uuid: Optional[str] = None
    """The optional ``uuid`` defines the universally unique identifier. Defaults to ``None.``"""

    @classmethod
    def from_sexpr(cls, exp: list) -> Junction:
        """Convert the given S-Expresstion into a Junction object

        Args:
            - exp (list): Part of parsed S-Expression ``(junction ...)``

        Raises:
            - Exception: When given parameter's type is not a list
            - Exception: When the first item of the list is not junction

        Returns:
            - Junction: Object of the class initialized with the given S-Expression
        """
        if not isinstance(exp, list):
            raise Exception("Expression does not have the correct type")

        if exp[0] != 'junction':
            raise Exception("Expression does not have the correct type")

        object = cls()
        for item in exp:
            if item[0] == 'at': object.position = Position().from_sexpr(item)
            if item[0] == 'color': object.color = ColorRGBA().from_sexpr(item)
            if item[0] == 'diameter': object.color = item[1]
            if item[0] == 'uuid': object.uuid = item[1]
        return object

    def to_sexpr(self, indent=2, newline=True) -> str:
        """Generate the S-Expression representing this object

        Args:
            - indent (int): Number of whitespaces used to indent the output. Defaults to 2.
            - newline (bool): Adds a newline to the end of the output. Defaults to True.

        Returns:
            - str: S-Expression of this object
        """
        indents = ' '*indent
        endline = '\n' if newline else ''
        uuid = f'\n{indents}  (uuid {self.uuid})\n' if self.uuid is not None else ''
        expression =  f'{indents}(junction (at {self.position.X} {self.position.Y}) (diameter {self.diameter}) {self.color.to_sexpr()}{uuid}{indents}){endline}'
        return expression

@dataclass
class NoConnect():
    """The ``no_connect`` token defines a unused pin connection in the schematic

    Documentation:
        https://dev-docs.kicad.org/en/file-formats/sexpr-schematic/#_no_connect_section
    """

    position: Position = field(default_factory=lambda: Position())
    """The ``position`` defines the X and Y coordinates of the no connect"""

    uuid: Optional[str] = None
    """The optional ``uuid`` defines the universally unique identifier. Defaults to ``None.``"""

    @classmethod
    def from_sexpr(cls, exp: list) -> NoConnect:
        """Convert the given S-Expresstion into a NoConnect object

        Args:
            - exp (list): Part of parsed S-Expression ``(no_connect ...)``

        Raises:
            - Exception: When given parameter's type is not a list
            - Exception: When the first item of the list is not no_connect

        Returns:
            - NoConnect: Object of the class initialized with the given S-Expression
        """
        if not isinstance(exp, list):
            raise Exception("Expression does not have the correct type")

        if exp[0] != 'no_connect':
            raise Exception("Expression does not have the correct type")

        object = cls()
        for item in exp:
            if item[0] == 'at': object.position = Position().from_sexpr(item)
            if item[0] == 'uuid': object.uuid = item[1]
        return object

    def to_sexpr(self, indent=2, newline=True) -> str:
        """Generate the S-Expression representing this object

        Args:
            - indent (int): Number of whitespaces used to indent the output. Defaults to 2.
            - newline (bool): Adds a newline to the end of the output. Defaults to True.

        Returns:
            - str: S-Expression of this object
        """
        indents = ' '*indent
        endline = '\n' if newline else ''
        uuid = f' (uuid {self.uuid})' if self.uuid is not None else ''

        return f'{indents}(no_connect (at {self.position.X} {self.position.Y}){uuid}){endline}'

@dataclass
class BusEntry():
    """The ``bus_entry`` token defines a bus entry in the schematic

    Documentation:
        https://dev-docs.kicad.org/en/file-formats/sexpr-schematic/#_bus_entry_section
    """

    position: Position = field(default_factory=lambda: Position())
    """The ``position`` defines the X and Y coordinates of the bus entry"""

    uuid: Optional[str] = None
    """The optional ``uuid`` defines the universally unique identifier. Defaults to ``None.``"""

    size: Position = field(default_factory=lambda: Position())         # Re-using Position class here
    """The ``size`` token attributes define the X and Y distance of the end point from
       the position of the bus entry"""

    stroke: Stroke = field(default_factory=lambda: Stroke())
    """The ``stroke`` defines how the bus entry is drawn"""

    @classmethod
    def from_sexpr(cls, exp: list) -> BusEntry:
        """Convert the given S-Expresstion into a BusEntry object

        Args:
            - exp (list): Part of parsed S-Expression ``(bus_entry ...)``

        Raises:
            - Exception: When given parameter's type is not a list
            - Exception: When the first item of the list is not bus_entry

        Returns:
            - BusEntry: Object of the class initialized with the given S-Expression
        """
        if not isinstance(exp, list):
            raise Exception("Expression does not have the correct type")

        if exp[0] != 'bus_entry':
            raise Exception("Expression does not have the correct type")

        object = cls()
        for item in exp:
            if item[0] == 'at': object.position = Position().from_sexpr(item)
            if item[0] == 'stroke': object.stroke = Stroke().from_sexpr(item)
            if item[0] == 'size': object.size = Position().from_sexpr(item)
            if item[0] == 'uuid': object.uuid = item[1]
        return object

    def to_sexpr(self, indent=2, newline=True) -> str:
        """Generate the S-Expression representing this object

        Args:
            - indent (int): Number of whitespaces used to indent the output. Defaults to 2.
            - newline (bool): Adds a newline to the end of the output. Defaults to True.

        Returns:
            - str: S-Expression of this object
        """
        indents = ' '*indent
        endline = '\n' if newline else ''

        expression =  f'{indents}(bus_entry (at {self.position.X} {self.position.Y}) (size {self.size.X} {self.size.Y})\n'
        expression += self.stroke.to_sexpr(indent+2)
        if self.uuid is not None:
            expression += f'{indents}  (uuid {self.uuid})\n'
        expression += f'{indents}){endline}'
        return expression

@dataclass
class Connection():
    """The ``wire`` and ``bus`` tokens define wires and buses in the schematic

    Documentation:
        https://dev-docs.kicad.org/en/file-formats/sexpr-schematic/#_wire_and_bus_section
    """

    type: str = "wire"
    """The ``type`` token defines wether the connection is a ``bus`` or a ``wire``"""

    points: List[Position] = field(default_factory=list)
    """The ``points`` token defines the list of X and Y coordinates of start and end points
       of the wire or bus"""

    stroke: Stroke = field(default_factory=lambda: Stroke())
    """The ``stroke`` defines how the connection is drawn"""

    uuid: Optional[str] = None
    """The optional ``uuid`` defines the universally unique identifier. Defaults to ``None.``"""

    @classmethod
    def from_sexpr(cls, exp: list) -> Connection:
        """Convert the given S-Expresstion into a Connection object

        Args:
            - exp (list): Part of parsed S-Expression ``(wire ...)`` or ``(bus ...)``

        Raises:
            - Exception: When given parameter's type is not a list
            - Exception: When the first item of the list is not wire or bus

        Returns:
            - Connection: Object of the class initialized with the given S-Expression
        """
        if not isinstance(exp, list):
            raise Exception("Expression does not have the correct type")

        if not (exp[0] == 'wire' or exp[0] == 'bus'):
            raise Exception("Expression does not have the correct type")

        object = cls()
        object.type = exp[0]
        for item in exp:
            if item[0] == 'pts':
                for point in item[1:]:
                    object.points.append(Position().from_sexpr(point))
            if item[0] == 'stroke': object.stroke = Stroke().from_sexpr(item)
            if item[0] == 'uuid': object.uuid = item[1]
        return object

    def to_sexpr(self, indent=2, newline=True) -> str:
        """Generate the S-Expression representing this object

        Args:
            - indent (int): Number of whitespaces used to indent the output. Defaults to 2.
            - newline (bool): Adds a newline to the end of the output. Defaults to True.

        Returns:
            - str: S-Expression of this object
        """
        indents = ' '*indent
        endline = '\n' if newline else ''

        points = ''
        for point in self.points:
            points += f' (xy {point.X} {point.Y})'

        expression =  f'{indents}({self.type} (pts{points})\n'
        expression += self.stroke.to_sexpr(indent+2)
        if self.uuid is not None:
            expression += f'{indents}  (uuid {self.uuid})\n'
        expression += f'{indents}){endline}'
        return expression

@dataclass
class PolyLine():
    """The ``polyline`` token defines one or more lines that may or may not represent a polygon

    Documentation:
        https://dev-docs.kicad.org/en/file-formats/sexpr-schematic/#_graphical_line_section
    """

    points: List[Position] = field(default_factory=list)
    """The ``points`` token defines the list of X/Y coordinates of to draw line(s)
       between. A minimum of two points is required."""

    stroke: Stroke = field(default_factory=lambda: Stroke())
    """The ``stroke`` defines how the graphical line is drawn"""

    uuid: Optional[str] = None
    """The optional ``uuid`` defines the universally unique identifier. Defaults to ``None.``"""

    @classmethod
    def from_sexpr(cls, exp: list) -> PolyLine:
        """Convert the given S-Expresstion into a PolyLine object

        Args:
            - exp (list): Part of parsed S-Expression ``(polyline ...)``

        Raises:
            - Exception: When given parameter's type is not a list
            - Exception: When the first item of the list is not polyline

        Returns:
            - PolyLine: Object of the class initialized with the given S-Expression
        """
        if not isinstance(exp, list):
            raise Exception("Expression does not have the correct type")

        if exp[0] != 'polyline':
            raise Exception("Expression does not have the correct type")

        object = cls()
        for item in exp:
            if item[0] == 'pts':
                for point in item[1:]:
                    object.points.append(Position().from_sexpr(point))
            if item[0] == 'stroke': object.stroke = Stroke().from_sexpr(item)
            if item[0] == 'uuid': object.uuid = item[1]
        return object

    def to_sexpr(self, indent=2, newline=True) -> str:
        """Generate the S-Expression representing this object

        Args:
            - indent (int): Number of whitespaces used to indent the output. Defaults to 2.
            - newline (bool): Adds a newline to the end of the output. Defaults to True.

        Returns:
            - str: S-Expression of this object
        """
        indents = ' '*indent
        endline = '\n' if newline else ''

        points = ''
        for point in self.points:
            points += f' (xy {point.X} {point.Y})'

        expression =  f'{indents}(polyline (pts{points})\n'
        expression += self.stroke.to_sexpr(indent+2)
        if self.uuid is not None:
            expression += f'{indents}  (uuid {self.uuid})\n'
        expression += f'{indents}){endline}'
        return expression

@dataclass
class Text():
    """The ``text`` token defines graphical text in a schematic

    Documentation:
        https://dev-docs.kicad.org/en/file-formats/sexpr-schematic/#_graphical_text_section
    """

    text: str = ""
    """The ``text`` token defines the text string"""

    position: Position = field(default_factory=lambda: Position())
    """The ``position`` token defines the X and Y coordinates and rotation angle of the text"""

    effects: Effects = field(default_factory=lambda: Effects())
    """The ``effects`` token defines how the text is drawn"""

    uuid: Optional[str] = None
    """The optional ``uuid`` defines the universally unique identifier. Defaults to ``None.``"""

    @classmethod
    def from_sexpr(cls, exp: list) -> Text:
        """Convert the given S-Expresstion into a Text object

        Args:
            - exp (list): Part of parsed S-Expression ``(text ...)``

        Raises:
            - Exception: When given parameter's type is not a list
            - Exception: When the first item of the list is not text

        Returns:
            - Text: Object of the class initialized with the given S-Expression
        """
        if not isinstance(exp, list):
            raise Exception("Expression does not have the correct type")

        if exp[0] != 'text':
            raise Exception("Expression does not have the correct type")

        object = cls()
        object.text = exp[1]
        for item in exp[2:]:
            if item[0] == 'at': object.position = Position().from_sexpr(item)
            if item[0] == 'effects': object.effects = Effects().from_sexpr(item)
            if item[0] == 'uuid': object.uuid = item[1]
        return object

    def to_sexpr(self, indent=2, newline=True) -> str:
        """Generate the S-Expression representing this object

        Args:
            - indent (int): Number of whitespaces used to indent the output. Defaults to 2.
            - newline (bool): Adds a newline to the end of the output. Defaults to True.

        Returns:
            - str: S-Expression of this object
        """
        indents = ' '*indent
        endline = '\n' if newline else ''

        posA = f' {self.position.angle}' if self.position.angle is not None else ''

        expression =  f'{indents}(text "{dequote(self.text)}"'

        # Strings longer or equal than 50 chars have the position in the next line
        if len(self.text) >= 50:
            expression += f'\n{indents}  '
        else:
            expression += ' '
        expression += f'(at {self.position.X} {self.position.Y}{posA})\n'
        expression += self.effects.to_sexpr(indent+2)
        if self.uuid is not None:
            expression += f'{indents}  (uuid {self.uuid})\n'
        expression += f'{indents}){endline}'
        return expression

@dataclass
class TextBox():
    """The ``text_box`` token defines a text box inside a schematic

    Available since KiCad v7

    Documentation:
        ????
    """
    text: str = ""
    """The ``text`` token defines the text string"""

    position: Position = field(default_factory=lambda: Position())
    """The ``position`` token defines the X and Y coordinates and rotation angle of the text"""

    size: Position = field(default_factory=lambda: Position())
    """The ``size`` token defines the size in X and Y direction. Angle is not used."""

    stroke: Stroke = field(default_factory=lambda: Stroke())
    """The ``stroke`` token defines the look of the outline of the text box"""

    fill: Fill = field(default_factory=lambda: Fill())
    """The ``fill`` token defines how the text box should be filled"""

    effects: Effects = field(default_factory=lambda: Effects())
    """The ``effects`` token defines how the text is drawn"""

    uuid: Optional[str] = None
    """The optional ``uuid`` defines the universally unique identifier. Defaults to ``None.``"""

    @classmethod
    def from_sexpr(cls, exp: list) -> TextBox:
        """Convert the given S-Expresstion into a TextBox object

        Args:
            - exp (list): Part of parsed S-Expression ``(text_box ...)``

        Raises:
            - Exception: When given parameter's type is not a list
            - Exception: When the first item of the list is not text_box

        Returns:
            - TextBox: Object of the class initialized with the given S-Expression
        """
        if not isinstance(exp, list):
            raise Exception("Expression does not have the correct type")

        if exp[0] != 'text_box':
            raise Exception("Expression does not have the correct type")

        object = cls()
        object.text = exp[1]
        for item in exp[2:]:
            if item[0] == 'at': object.position = Position().from_sexpr(item)
            if item[0] == 'size': object.size = Position().from_sexpr(item)
            if item[0] == 'effects': object.effects = Effects().from_sexpr(item)
            if item[0] == 'stroke': object.stroke = Stroke().from_sexpr(item)
            if item[0] == 'fill': object.fill = Fill().from_sexpr(item)
            if item[0] == 'uuid': object.uuid = item[1]
        return object

    def to_sexpr(self, indent=2, newline=True) -> str:
        """Generate the S-Expression representing this object

        Args:
            - indent (int): Number of whitespaces used to indent the output. Defaults to 2.
            - newline (bool): Adds a newline to the end of the output. Defaults to True.

        Returns:
            - str: S-Expression of this object
        """
        indents = ' '*indent
        endline = '\n' if newline else ''

        posA = f' {self.position.angle}' if self.position.angle is not None else ''

        expression =  f'{indents}(text_box "{dequote(self.text)}"\n'
        expression += f'{indents}  (at {self.position.X} {self.position.Y}{posA}) (size {self.size.X} {self.size.Y})\n'
        expression += self.stroke.to_sexpr(indent+2)
        expression += self.fill.to_sexpr(indent+2)
        expression += self.effects.to_sexpr(indent+2)
        if self.uuid is not None:
            expression += f'{indents}  (uuid {self.uuid})\n'
        expression += f'{indents}){endline}'
        return expression

@dataclass
class LocalLabel():
    """The ``label`` token defines an wire or bus label name in a schematic

    Documentation:
        https://dev-docs.kicad.org/en/file-formats/sexpr-schematic/#local_label_section
    """

    text: str = ""
    """The ``text`` token defines the text in the label"""

    position: Position = field(default_factory=lambda: Position())
    """The ``position`` token defines the X and Y coordinates and rotation angle of the label"""

    effects: Effects = field(default_factory=lambda: Effects())
    """The ``effects`` token defines how the label is drawn"""

    uuid: Optional[str] = None
    """The optional ``uuid`` defines the universally unique identifier. Defaults to ``None.``"""

    fieldsAutoplaced: bool = False
    """The ``fields_autoplaced`` is a flag that indicates that any PROPERTIES associated
    with the global label have been place automatically"""

    @classmethod
    def from_sexpr(cls, exp: list) -> LocalLabel:
        """Convert the given S-Expresstion into a LocalLabel object

        Args:
            - exp (list): Part of parsed S-Expression ``(label ...)``

        Raises:
            - Exception: When given parameter's type is not a list
            - Exception: When the first item of the list is not label

        Returns:
            - LocalLabel: Object of the class initialized with the given S-Expression
        """
        if not isinstance(exp, list):
            raise Exception("Expression does not have the correct type")

        if exp[0] != 'label':
            raise Exception("Expression does not have the correct type")

        object = cls()
        object.text = exp[1]
        for item in exp[2:]:
            if item[0] == 'at': object.position = Position().from_sexpr(item)
            if item[0] == 'effects': object.effects = Effects().from_sexpr(item)
            if item[0] == 'uuid': object.uuid = item[1]
            if item[0] == 'fields_autoplaced': object.fieldsAutoplaced = True
        return object

    def to_sexpr(self, indent=2, newline=True) -> str:
        """Generate the S-Expression representing this object

        Args:
            - indent (int): Number of whitespaces used to indent the output. Defaults to 2.
            - newline (bool): Adds a newline to the end of the output. Defaults to True.

        Returns:
            - str: S-Expression of this object
        """
        indents = ' '*indent
        endline = '\n' if newline else ''

        posA = f' {self.position.angle}' if self.position.angle is not None else ''
        fieldsAutoplaced = ' (fields_autoplaced)' if self.fieldsAutoplaced else ''

        expression =  f'{indents}(label "{dequote(self.text)}" (at {self.position.X} {self.position.Y}{posA}){fieldsAutoplaced}\n'
        expression += self.effects.to_sexpr(indent+2)
        if self.uuid is not None:
            expression += f'{indents}  (uuid {self.uuid})\n'
        expression += f'{indents}){endline}'
        return expression

@dataclass
class GlobalLabel():
    """The ``global_label`` token defines a label name that is visible across all schematics in a design

    Documentation:
        https://dev-docs.kicad.org/en/file-formats/sexpr-schematic/#_global_label_section
    """

    text: str = ""
    """The ``text`` token defines the text in the label"""

    shape: str = "input"
    """The ``shape`` token defines the way the global label is drawn. Possible values are:
       ``input``, ``output``, ``bidirectional``, ``tri_state``, ``passive``."""

    fieldsAutoplaced: bool = False
    """The ``fields_autoplaced`` is a flag that indicates that any PROPERTIES associated
       with the global label have been place automatically"""

    position: Position = field(default_factory=lambda: Position())
    """The ``position`` token defines the X and Y coordinates and rotation angle of the label"""

    effects: Effects = field(default_factory=lambda: Effects())
    """The ``effects`` token defines how the label is drawn"""

    uuid: Optional[str] = None
    """The optional ``uuid`` defines the universally unique identifier. Defaults to ``None.``"""

    properties: List[Property] = field(default_factory=list)
    """	The ``properties`` token defines a list of properties of the global label. Currently, the
    only supported property is the inter-sheet reference"""

    @classmethod
    def from_sexpr(cls, exp: list) -> GlobalLabel:
        """Convert the given S-Expresstion into a GlobalLabel object

        Args:
            - exp (list): Part of parsed S-Expression ``(global_label ...)``

        Raises:
            - Exception: When given parameter's type is not a list
            - Exception: When the first item of the list is not global_label

        Returns:
            - GlobalLabel: Object of the class initialized with the given S-Expression
        """
        if not isinstance(exp, list):
            raise Exception("Expression does not have the correct type")

        if exp[0] != 'global_label':
            raise Exception("Expression does not have the correct type")

        object = cls()
        object.text = exp[1]
        for item in exp[2:]:
            if item[0] == 'fields_autoplaced': object.fieldsAutoplaced = True
            if item[0] == 'at': object.position = Position().from_sexpr(item)
            if item[0] == 'effects': object.effects = Effects().from_sexpr(item)
            if item[0] == 'property': object.properties.append(Property().from_sexpr(item))
            if item[0] == 'shape': object.shape = item[1]
            if item[0] == 'uuid': object.uuid = item[1]
        return object

    def to_sexpr(self, indent=2, newline=True) -> str:
        """Generate the S-Expression representing this object

        Args:
            - indent (int): Number of whitespaces used to indent the output. Defaults to 2.
            - newline (bool): Adds a newline to the end of the output. Defaults to True.

        Returns:
            - str: S-Expression of this object
        """
        indents = ' '*indent
        endline = '\n' if newline else ''

        posA = f' {self.position.angle}' if self.position.angle is not None else ''
        fa = ' (fields_autoplaced)' if self.fieldsAutoplaced else ''

        expression =  f'{indents}(global_label "{dequote(self.text)}" (shape {self.shape}) (at {self.position.X} {self.position.Y}{posA}){fa}\n'
        expression += self.effects.to_sexpr(indent+2)
        if self.uuid is not None:
            expression += f'{indents}  (uuid {self.uuid})\n'
        for property in self.properties:
            expression += property.to_sexpr(indent+2)
        expression += f'{indents}){endline}'
        return expression

@dataclass
class HierarchicalLabel():
    """The ``hierarchical_label`` token defines a label that are used by hierarchical sheets to
    define connections between sheet in hierarchical designs

    Documentation:
        https://dev-docs.kicad.org/en/file-formats/sexpr-schematic/#_hierarchical_label_section
    """

    text: str = ""
    """The ``text`` token defines the text in the label"""

    shape: str = "input"
    """The ``shape`` token defines the way the global label is drawn. Possible values are:
    ``input``, ``output``, ``bidirectional``, ``tri_state``, ``passive``."""

    position: Position = field(default_factory=lambda: Position())
    """The ``position`` token defines the X and Y coordinates and rotation angle of the label"""

    effects: Effects = field(default_factory=lambda: Effects())
    """The ``effects`` token defines how the label is drawn"""

    uuid: Optional[str] = None
    """The optional ``uuid`` defines the universally unique identifier. Defaults to ``None.``"""
    
    fieldsAutoplaced: bool = False
    """The ``fields_autoplaced`` is a flag that indicates that any PROPERTIES associated
    with the global label have been place automatically"""

    @classmethod
    def from_sexpr(cls, exp: list) -> HierarchicalLabel:
        """Convert the given S-Expresstion into a HierarchicalLabel object

        Args:
            - exp (list): Part of parsed S-Expression ``(hierarchical_label ...)``

        Raises:
            - Exception: When given parameter's type is not a list
            - Exception: When the first item of the list is not hierarchical_label

        Returns:
            - HierarchicalLabel: Object of the class initialized with the given S-Expression
        """
        if not isinstance(exp, list):
            raise Exception("Expression does not have the correct type")

        if exp[0] != 'hierarchical_label':
            raise Exception("Expression does not have the correct type")

        object = cls()
        object.text = exp[1]
        for item in exp[2:]:
            if item[0] == 'at': object.position = Position().from_sexpr(item)
            if item[0] == 'effects': object.effects = Effects().from_sexpr(item)
            if item[0] == 'shape': object.shape = item[1]
            if item[0] == 'uuid': object.uuid = item[1]
            if item[0] == 'fields_autoplaced': object.fieldsAutoplaced = True
        return object

    def to_sexpr(self, indent=2, newline=True) -> str:
        """Generate the S-Expression representing this object

        Args:
            - indent (int): Number of whitespaces used to indent the output. Defaults to 2.
            - newline (bool): Adds a newline to the end of the output. Defaults to True.

        Returns:
            - str: S-Expression of this object
        """
        indents = ' '*indent
        endline = '\n' if newline else ''

        posA = f' {self.position.angle}' if self.position.angle is not None else ''
        fieldsAutoplaced = ' (fields_autoplaced)' if self.fieldsAutoplaced else ''

        expression =  f'{indents}(hierarchical_label "{dequote(self.text)}" (shape {self.shape}) (at {self.position.X} {self.position.Y}{posA}){fieldsAutoplaced}\n'
        expression += self.effects.to_sexpr(indent+2)
        if self.uuid is not None:
            expression += f'{indents}  (uuid {self.uuid})\n'
        expression += f'{indents}){endline}'
        return expression

@dataclass
class SymbolProjectPath():
    """The symbol project path defines the ``path`` token to the sheet instance of the instance data
    of a symbol.

    Available since KiCad v7.

    Documentation:
        https://dev-docs.kicad.org/en/file-formats/sexpr-schematic/#_symbol_section
    """
    
    sheetInstancePath: str = ""
    """The ``PATH_INSTANCE`` token defines the path to the symbol instance"""

    reference: str = ""
    """The ``reference`` token is a string that defines the reference designator for the symbol
    instance"""

    unit: int = 1
    """The ``unit`` token is a integer that defines the symbol unit for the symbol instance. For 
    symbols that do not define multiple units, this will always be 1."""

    @classmethod
    def from_sexpr(cls, exp: list) -> SymbolProjectPath:        
        """Convert the given S-Expression into a SymbolProjectPath object

        Args:
            - exp (list): Part of parsed S-Expression ``(path ...)``

        Raises:
            - Exception: When given parameter's type is not a list
            - Exception: When the first item of the list is not path

        Returns:
            - SymbolProjectPath: Object of the class initialized with the given S-Expression
        """
        if not isinstance(exp, list) or len(exp) < 2:
            raise Exception("Expression does not have the correct type")

        if exp[0] != 'path':
            raise Exception("Expression does not have the correct type")

        object = cls()
        object.sheetInstancePath = exp[1]
        for item in exp[2:]:
            if item[0] == 'reference': object.reference = item[1]
            if item[0] == 'unit': object.unit = item[1]
        return object

    def to_sexpr(self, indent=4, newline=True) -> str:
        """Generate the S-Expression representing this object

        Args:
            - indent (int): Number of whitespaces used to indent the output. Defaults to 4.
            - newline (bool): Adds a newline to the end of the output. Defaults to True.

        Returns:
            - str: S-Expression of this object
        """
        indents = ' '*indent
        endline = '\n' if newline else ''
        expression =  f'{indents}(path "{dequote(self.sheetInstancePath)}"\n'
        expression += f'{indents}  (reference "{dequote(self.reference)}") (unit {self.unit})\n'
        expression += f'{indents}){endline}'
        return expression

@dataclass
class SymbolProjectInstance(ProjectInstance):
    """The ``project`` token attribute defines the name of the project as well as a list of symbol
    project paths (instance data). There can be instance data from other project when schematics 
    are shared across multiple projects. The projects will have to be sorted by the ``name`` token
    in alphabetical order.

    Available since KiCad v7.

    Documentation:
        https://dev-docs.kicad.org/en/file-formats/sexpr-schematic/#_symbol_section
    """

    paths: List[SymbolProjectPath] = field(default_factory=list)
    """The ``paths`` token defines a list of symbol project paths for this project instance"""
    
    @classmethod
    def from_sexpr(cls, exp: list) -> SymbolProjectInstance:        
        """Convert the given S-Expression into a SymbolProjectInstance object

        Args:
            - exp (list): Part of parsed S-Expression ``(project ...)``

        Raises:
            - Exception: When given parameter's type is not a list
            - Exception: When the first item of the list is not project

        Returns:
            - SymbolProjectInstance: Object of the class initialized with the given S-Expression
        """
        if not isinstance(exp, list) or len(exp) < 2:
            raise Exception("Expression does not have the correct type")

        if exp[0] != 'project':
            raise Exception("Expression does not have the correct type")

        object = cls()
        object.name = exp[1]
        for item in exp[2:]:
            if item[0] == 'path': object.paths.append(SymbolProjectPath.from_sexpr(item))
        return object

    def to_sexpr(self, indent=2, newline=True) -> str:
        """Generate the S-Expression representing this object

        Args:
            - indent (int): Number of whitespaces used to indent the output. Defaults to 2.
            - newline (bool): Adds a newline to the end of the output. Defaults to True.

        Returns:
            - str: S-Expression of this object
        """
        indents = ' '*indent
        endline = '\n' if newline else ''
        expression = f'{indents}(project "{dequote(self.name)}"\n'
        for path in self.paths:
            expression += path.to_sexpr(indent+2)
        expression += f'{indents}){endline}'
        return expression

@dataclass
class SchematicSymbol():
    """The ``symbol`` token in the symbol section of the schematic defines an instance of a symbol
    from the library symbol section of the schematic

    Documentation:
        https://dev-docs.kicad.org/en/file-formats/sexpr-schematic/#_symbol_section
    """

    @property
    def libId(self) -> str:
        """The ``lib_id`` token defines which symbol in the library symbol section of the schematic
        this schematic symbol references. In ``kiutils``, the ``lib_id`` token is a combination of
        both the ``libraryNickname`` and ``entryName`` token. Setting the ``lib_id`` token will
        update those tokens accordingly.

        Returns:
            - Symbol id in the following format: ``<libraryNickname>:<entryName>`` or ``<entryName>``,
              if ``libraryNickname`` token is not set.
        """
        if self.libraryNickname:
            return f'{self.libraryNickname}:{self.entryName}'
        else:
            return f'{self.entryName}'

    @libId.setter
    def libId(self, symbol_id: str):
        """Sets the ``lib_id`` token and parses its contents into the ``libraryNickname`` and
        ``entryName`` token.

        Args:
            - symbol_id (str): The symbol id in the following format: ``<libraryNickname>:<entryName>``
              or only ``<entryName>``
        """
        parse_symbol_id = re.match(r"^(.+?):(.+?)$", symbol_id)
        if parse_symbol_id:
            self.libraryNickname = parse_symbol_id.group(1)
            self.entryName = parse_symbol_id.group(2)
        else:
            self.libraryNickname = None
            self.entryName = symbol_id

    libraryNickname: Optional[str] = None
    """The optional ``libraryNickname`` token defines which symbol library this symbol belongs to
    and is a part of the ``id`` token"""

    entryName: str = None
    """The ``entryName`` token defines the actual name of the symbol and is a part of the ``id``
    token"""

    libName: Optional[str] = None
    """The optional ``lib_name`` token is only set when the symbol was edited in the schematic.
    It may be set to ``<entryName>_X`` where X is a unique number that specifies which variation
    this symbol is of its original."""

    position: Position = field(default_factory=lambda: Position())
    """The ``position`` defines the X and Y coordinates and angle of rotation of the symbol"""

    unit: Optional[int] = None
    """The optional ``unit`` token attribute defines which unit in the symbol library definition
    that the schematic symbol represents"""

    inBom: bool = False
    """The ``in_bom`` token attribute determines whether the schematic symbol appears in any bill
    of materials output"""

    onBoard: bool = False
    """The ``on_board`` token attribute determines if the footprint associated with the symbol is
    exported to the board via the netlist"""

    dnp: Optional[bool] = None
    """The optional ``dnp`` token defines if a symbol is marked as do-not-populate in the schematic. 
    
    Available since KiCad v7"""

    fieldsAutoplaced: bool = False
    """The ``fields_autoplaced`` is a flag that indicates that any PROPERTIES associated
    with the global label have been place automatically"""

    uuid: Optional[str] = ""
    """The optional `uuid` defines the universally unique identifier"""

    properties: List[Property] = field(default_factory=list)
    """The ``properties`` section defines a list of symbol properties of the schematic symbol"""

    pins: Dict[str, str] = field(default_factory=dict)
    """The ``pins`` token defines a dictionary with pin numbers in form of strings as keys and
    uuid's as values"""

    mirror: Optional[str] = None
    """The ``mirror`` token defines if the symbol is mirrored in the schematic. Accepted values:
    ``x`` or ``y``. When mirroring around the x and y axis at the same time use some additional
    rotation to get the correct orientation of the symbol."""

    instances: List[SymbolProjectInstance] = field(default_factory=list)
    """The ``instances`` token defines a list of symbol instances grouped by project. Every symbol 
    will have a least one instance.
    
    Available since KiCad v7."""

    @classmethod
    def from_sexpr(cls, exp: list) -> SchematicSymbol:
        """Convert the given S-Expresstion into a SchematicSymbol object

        Args:
            - exp (list): Part of parsed S-Expression ``(symbol ...)``

        Raises:
            - Exception: When given parameter's type is not a list
            - Exception: When the first item of the list is not symbol

        Returns:
            - SchematicSymbol: Object of the class initialized with the given S-Expression
        """
        if not isinstance(exp, list):
            raise Exception("Expression does not have the correct type")

        if exp[0] != 'symbol':
            raise Exception("Expression does not have the correct type")

        object = cls()
        for item in exp[1:]:
            if item[0] == 'fields_autoplaced': object.fieldsAutoplaced = True
            if item[0] == 'lib_id': object.libId = item[1]
            if item[0] == 'lib_name': object.libName = item[1]
            if item[0] == 'uuid': object.uuid = item[1]
            if item[0] == 'unit': object.unit = item[1]
            if item[0] == 'in_bom': object.inBom = True if item[1] == 'yes' else False
            if item[0] == 'on_board': object.onBoard = True if item[1] == 'yes' else False
            if item[0] == 'dnp': object.dnp = True if item[1] == 'yes' else False
            if item[0] == 'at': object.position = Position().from_sexpr(item)
            if item[0] == 'property': object.properties.append(Property().from_sexpr(item))
            if item[0] == 'pin': object.pins.update({item[1]: item[2][1]})
            if item[0] == 'mirror': object.mirror = item[1]
            if item[0] == 'instances':
                for instance in item[1:]:
                    object.instances.append(SymbolProjectInstance.from_sexpr(instance))
        
        return object

    def to_sexpr(self, indent=2, newline=True) -> str:
        """Generate the S-Expression representing this object

        Args:
            - indent (int): Number of whitespaces used to indent the output. Defaults to 2.
            - newline (bool): Adds a newline to the end of the output. Defaults to True.

        Returns:
            - str: S-Expression of this object
        """
        indents = ' '*indent
        endline = '\n' if newline else ''

        posA = f' {self.position.angle}' if self.position.angle is not None else ''
        fa = f' (fields_autoplaced)' if self.fieldsAutoplaced else ''
        inBom = 'yes' if self.inBom else 'no'
        onBoard = 'yes' if self.onBoard else 'no'
        mirror = f' (mirror {self.mirror})' if self.mirror is not None else ''
        unit = f' (unit {self.unit})' if self.unit is not None else ''
        lib_name = f' (lib_name "{dequote(self.libName)}")' if self.libName is not None else ''
        if self.dnp is not None:
            dnp = ' (dnp yes)' if self.dnp else ' (dnp no)'
        else:
            dnp = ''

        expression =  f'{indents}(symbol{lib_name} (lib_id "{dequote(self.libId)}") (at {self.position.X} {self.position.Y}{posA}){mirror}{unit}\n'
        expression += f'{indents}  (in_bom {inBom}) (on_board {onBoard}){dnp}{fa}\n'
        if self.uuid:
            expression += f'{indents}  (uuid {self.uuid})\n'
        for property in self.properties:
            expression += property.to_sexpr(indent+2)
        for number, uuid in self.pins.items():
            expression += f'{indents}  (pin "{dequote(number)}" (uuid {uuid}))\n'
        if len(self.instances) != 0:
            expression += f'{indents}  (instances\n'
            for instance in self.instances:
                expression += instance.to_sexpr(indent+4)
            expression += f'{indents}  )\n'
        expression += f'{indents}){endline}'
        return expression

@dataclass
class HierarchicalPin():
    """The ``pin`` token in a sheet object defines an electrical connection between the sheet in a
       schematic with the hierarchical label defined in the associated schematic file

    Documentation:
        https://dev-docs.kicad.org/en/file-formats/sexpr-schematic/#_hierarchical_sheet_pin_definition
    """

    name: str = ""
    """	The ``name`` attribute defines the name of the sheet pin. It must have an identically named
        hierarchical label in the associated schematic file."""

    connectionType: str = "input"
    """The electrical connect type token defines the type of electrical connect made by the
       sheet pin"""

    position: Position = field(default_factory=lambda: Position())
    """The ``position`` defines the X and Y coordinates and angle of rotation of the pin"""

    effects: Effects = field(default_factory=lambda: Effects())
    """The ``effects`` section defines how the pin name text is drawn"""

    uuid: Optional[str] = None
    """The optional ``uuid`` defines the universally unique identifier. Defaults to ``None.``"""

    @classmethod
    def from_sexpr(cls, exp: list) -> HierarchicalPin:
        """Convert the given S-Expresstion into a HierarchicalPin object

        Args:
            - exp (list): Part of parsed S-Expression ``(pin ...)``

        Raises:
            - Exception: When given parameter's type is not a list
            - Exception: When the first item of the list is not pin

        Returns:
            - HierarchicalPin: Object of the class initialized with the given S-Expression
        """
        if not isinstance(exp, list):
            raise Exception("Expression does not have the correct type")

        if exp[0] != 'pin':
            raise Exception("Expression does not have the correct type")

        object = cls()
        object.name = exp[1]
        object.connectionType = exp[2]
        for item in exp[3:]:
            if item[0] == 'at': object.position = Position().from_sexpr(item)
            if item[0] == 'effects': object.effects = Effects().from_sexpr(item)
            if item[0] == 'uuid': object.uuid = item[1]
        return object

    def to_sexpr(self, indent=4, newline=True) -> str:
        """Generate the S-Expression representing this object

        Args:
            - indent (int): Number of whitespaces used to indent the output. Defaults to 4.
            - newline (bool): Adds a newline to the end of the output. Defaults to True.

        Returns:
            - str: S-Expression of this object
        """
        indents = ' '*indent
        endline = '\n' if newline else ''

        posA = f' {self.position.angle}' if self.position.angle is not None else ''

        expression =  f'{indents}(pin "{dequote(self.name)}" {self.connectionType} (at {self.position.X} {self.position.Y}{posA})\n'
        expression += self.effects.to_sexpr(indent+2)
        if self.uuid is not None:
            expression += f'{indents}  (uuid {self.uuid})\n'
        expression += f'{indents}){endline}'
        return expression


@dataclass
class HierarchicalSheetProjectPath():
    """The symbol project path defines the ``path`` token to the sheet instance of the instance data
    of a symbol.

    Available since KiCad v7.

    Documentation:
        https://dev-docs.kicad.org/en/file-formats/sexpr-schematic/#_hierarchical_sheet_section
    """
    
    sheetInstancePath: str = ""
    """The ``PATH_INSTANCE`` token defines the path to the symbol instance"""

    page: str = ""
    """The ``page`` token is a string that defines the page number of the sheet instance"""

    @classmethod
    def from_sexpr(cls, exp: list) -> HierarchicalSheetProjectPath:        
        """Convert the given S-Expression into a HierarchicalSheetProjectPath object

        Args:
            - exp (list): Part of parsed S-Expression ``(path ...)``

        Raises:
            - Exception: When given parameter's type is not a list
            - Exception: When the first item of the list is not path

        Returns:
            - HierarchicalSheetProjectPath: Object of the class initialized with the given S-Expression
        """
        if not isinstance(exp, list) or len(exp) < 2:
            raise Exception("Expression does not have the correct type")

        if exp[0] != 'path':
            raise Exception("Expression does not have the correct type")

        object = cls()
        object.sheetInstancePath = exp[1]
        for item in exp[2:]:
            if item[0] == 'page': object.page = item[1]
        return object

    def to_sexpr(self, indent=4, newline=True) -> str:
        """Generate the S-Expression representing this object

        Args:
            - indent (int): Number of whitespaces used to indent the output. Defaults to 4.
            - newline (bool): Adds a newline to the end of the output. Defaults to True.

        Returns:
            - str: S-Expression of this object
        """
        indents = ' '*indent
        endline = '\n' if newline else ''
        return f'{indents}(path "{dequote(self.sheetInstancePath)}" (page "{dequote(self.page)}")){endline}'

@dataclass
class HierarchicalSheetProjectInstance(ProjectInstance):
    """The ``project`` token attribute defines the name of the project as well as a list of 
    hierarchical sheet project paths (instance data). There can be instance data from other project 
    when schematics are shared across multiple projects. The projects will have to be sorted by the 
    ``name`` token in alphabetical order.

    Available since KiCad v7.

    Documentation:
        https://dev-docs.kicad.org/en/file-formats/sexpr-schematic/#_hierarchical_sheet_section
    """

    paths: List[HierarchicalSheetProjectPath] = field(default_factory=list)
    """The ``paths`` token defines a list of hierarchical sheet project paths for this project instance"""
    
    @classmethod
    def from_sexpr(cls, exp: list) -> HierarchicalSheetProjectInstance:        
        """Convert the given S-Expression into a HierarchicalSheetProjectInstance object

        Args:
            - exp (list): Part of parsed S-Expression ``(project ...)``

        Raises:
            - Exception: When given parameter's type is not a list
            - Exception: When the first item of the list is not project

        Returns:
            - HierarchicalSheetProjectInstance: Object of the class initialized with the given S-Expression
        """
        if not isinstance(exp, list) or len(exp) < 2:
            raise Exception("Expression does not have the correct type")

        if exp[0] != 'project':
            raise Exception("Expression does not have the correct type")

        object = cls()
        object.name = exp[1]
        for item in exp[2:]:
            if item[0] == 'path': object.paths.append(HierarchicalSheetProjectPath.from_sexpr(item))
        return object

    def to_sexpr(self, indent=2, newline=True) -> str:
        """Generate the S-Expression representing this object

        Args:
            - indent (int): Number of whitespaces used to indent the output. Defaults to 2.
            - newline (bool): Adds a newline to the end of the output. Defaults to True.

        Returns:
            - str: S-Expression of this object
        """
        indents = ' '*indent
        endline = '\n' if newline else ''
        expression = f'{indents}(project "{dequote(self.name)}"\n'
        for path in self.paths:
            expression += path.to_sexpr(indent+2)
        expression += f'{indents}){endline}'
        return expression

@dataclass
class HierarchicalSheet():
    """The ``sheet`` token defines a hierarchical sheet of the schematic

    Documentation:
        https://dev-docs.kicad.org/en/file-formats/sexpr-schematic/#_hierarchical_sheet_section
    """

    position: Position = field(default_factory=lambda: Position())
    """The ``position`` defines the X and Y coordinates and angle of rotation of the sheet in the schematic"""

    width: float = 0
    """The ``width`` token defines the width of the sheet"""

    height: float = 0
    """The ``height`` token defines the height of the sheet"""

    fieldsAutoplaced: bool = False
    """The ``fields_autoplaced`` is a flag that indicates that any PROPERTIES associated
       with the global label have been place automatically"""

    stroke: Stroke = field(default_factory=lambda: Stroke())
    """The ``stroke`` defines how the sheet outline is drawn"""

    fill: ColorRGBA = field(default_factory=lambda: ColorRGBA())
    """The fill defines the color how the sheet is filled"""

    uuid: Optional[str] = None
    """The optional ``uuid`` defines the universally unique identifier. Defaults to ``None.``"""

    sheetName: Property = field(default_factory=lambda: Property(key="Sheet name"))
    """The ``sheetName`` is a property that defines the name of the sheet. The property's
       key should therefore be set to `Sheet name`"""

    fileName: Property = field(default_factory=lambda: Property(key="Sheet file"))
    """The ``fileName`` is a property that defines the file name of the sheet. The property's
       key should therefore be set to `Sheet file`"""

    pins: List[HierarchicalPin] = field(default_factory=list)
    """The ``pins`` section is a list of hierarchical pins that map a hierarchical label defined in
       the associated schematic file"""
    
    instances: List[HierarchicalSheetProjectInstance] = field(default_factory=list)
    """The ``instances`` token defines a list of hierachical sheet instances grouped by project. 
    Every hierarchical sheet will have a least one instance.
    
    Available since KiCad v7."""

    @classmethod
    def from_sexpr(cls, exp: list) -> HierarchicalSheet:
        """Convert the given S-Expresstion into a HierarchicalSheet object

        Args:
            - exp (list): Part of parsed S-Expression ``(sheet ...)``

        Raises:
            - Exception: When given parameter's type is not a list
            - Exception: When the first item of the list is not sheet

        Returns:
            - HierarchicalSheet: Object of the class initialized with the given S-Expression
        """
        if not isinstance(exp, list):
            raise Exception("Expression does not have the correct type")

        if exp[0] != 'sheet':
            raise Exception("Expression does not have the correct type")

        object = cls()
        for item in exp[1:]:
            if item[0] == 'fields_autoplaced': object.fieldsAutoplaced = True
            if item[0] == 'at': object.position = Position().from_sexpr(item)
            if item[0] == 'stroke': object.stroke = Stroke().from_sexpr(item)
            if item[0] == 'size':
                object.width = item[1]
                object.height = item[2]
            if item[0] == 'fill':
                object.fill = ColorRGBA().from_sexpr(item[1])
                object.fill.precision = 4
            if item[0] == 'uuid': object.uuid = item[1]
            if item[0] == 'property':
                if item[1] == 'Sheet name' or item[1] == 'Sheetname': object.sheetName = Property().from_sexpr(item)
                if item[1] == 'Sheet file' or item[1] == 'Sheetfile': object.fileName = Property().from_sexpr(item)
            if item[0] == 'pin': object.pins.append(HierarchicalPin().from_sexpr(item))
            if item[0] == 'instances':
                for instance in item[1:]:
                    object.instances.append(HierarchicalSheetProjectInstance.from_sexpr(instance))
        return object

    def to_sexpr(self, indent=2, newline=True) -> str:
        """Generate the S-Expression representing this object

        Args:
            - indent (int): Number of whitespaces used to indent the output. Defaults to 2.
            - newline (bool): Adds a newline to the end of the output. Defaults to True.

        Returns:
            - str: S-Expression of this object
        """
        indents = ' '*indent
        endline = '\n' if newline else ''

        fa = ' (fields_autoplaced)' if self.fieldsAutoplaced else ''

        expression =  f'{indents}(sheet (at {self.position.X} {self.position.Y}) (size {self.width} {self.height}){fa}\n'
        expression += self.stroke.to_sexpr(indent+2)
        expression += f'{indents}  (fill {self.fill.to_sexpr()})\n'
        if self.uuid is not None:
            expression += f'{indents}  (uuid {self.uuid})\n'
        expression += self.sheetName.to_sexpr(indent+2)
        expression += self.fileName.to_sexpr(indent+2)
        for pin in self.pins:
            expression += pin.to_sexpr(indent+2)
        if len(self.instances) != 0:
            expression += f'{indents}  (instances\n'
            for instance in self.instances:
                expression += instance.to_sexpr(indent+4)
            expression += f'{indents}  )\n'
        expression += f'{indents}){endline}'
        return expression

@dataclass
class HierarchicalSheetInstance():
    """The sheet_instance token defines the per sheet information for the entire schematic. This
       section will only exist in schematic files that are the root sheet of a project

    Documentation:
           https://dev-docs.kicad.org/en/file-formats/sexpr-schematic/#_hierarchical_sheet_instance_section
    """

    instancePath: str = "/"
    """The ``instancePath`` attribute is the path to the sheet instance"""

    page: str = "1"
    """The ``page`` token defines the page number of the schematic represented by the sheet
       instance information. Page numbers can be any valid string."""

    @classmethod
    def from_sexpr(cls, exp: list) -> HierarchicalSheetInstance:
        """Convert the given S-Expresstion into a HierarchicalSheetInstance object

        Args:
            - exp (list): Part of parsed S-Expression ``(path ...)``

        Raises:
            - Exception: When given parameter's type is not a list
            - Exception: When the first item of the list is not path

        Returns:
            - HierarchicalSheetInstance: Object of the class initialized with the given S-Expression
        """
        if not isinstance(exp, list):
            raise Exception("Expression does not have the correct type")

        if exp[0] != 'path':
            raise Exception("Expression does not have the correct type")

        object = cls()
        object.instancePath = exp[1]
        for item in exp[2:]:
            if item[0] == 'page': object.page = item[1]
        return object

    def to_sexpr(self, indent=4, newline=True) -> str:
        """Generate the S-Expression representing this object

        Args:
            - indent (int): Number of whitespaces used to indent the output. Defaults to 4.
            - newline (bool): Adds a newline to the end of the output. Defaults to True.

        Returns:
            - str: S-Expression of this object
        """
        indents = ' '*indent
        endline = '\n' if newline else ''

        return f'{indents}(path "{dequote(self.instancePath)}" (page "{dequote(self.page)}")){endline}'

@dataclass
class SymbolInstance():
    """The ``symbol_instance`` token defines the per symbol information for the entire schematic

    Documentation:
        https://dev-docs.kicad.org/en/file-formats/sexpr-schematic/#_symbol_instance_section
    """

    path: str = "/"
    """The ``path`` attribute is the path to the sheet instance"""

    reference: str = ""
    """The ``reference`` token attribute is a string that defines the reference designator for
       the symbol instance"""

    unit: int = 0
    """The unit token attribute is a integer ordinal that defines the symbol unit for the
       symbol instance. For symbols that do not define multiple units, this will always be 1."""

    value: str = ""
    """The value token attribute is a string that defines the value field for the symbol instance"""

    footprint: str = ""
    """The ``footprint`` token attribute is a string that defines the LIBRARY_IDENTIFIER for footprint associated with the symbol instance"""

    @classmethod
    def from_sexpr(cls, exp: list) -> SymbolInstance:
        """Convert the given S-Expresstion into a SymbolInstance object

        Args:
            - exp (list): Part of parsed S-Expression ``(path ...)``

        Raises:
            - Exception: When given parameter's type is not a list
            - Exception: When the first item of the list is not path

        Returns:
            - SymbolInstance: Object of the class initialized with the given S-Expression
        """
        if not isinstance(exp, list):
            raise Exception("Expression does not have the correct type")

        if exp[0] != 'path':
            raise Exception("Expression does not have the correct type")

        object = cls()
        object.path = exp[1]
        for item in exp[2:]:
            if item[0] == 'reference': object.reference = item[1]
            if item[0] == 'unit': object.unit = item[1]
            if item[0] == 'value': object.value = item[1]
            if item[0] == 'footprint': object.footprint = item[1]
        return object

    def to_sexpr(self, indent=4, newline=True) -> str:
        """Generate the S-Expression representing this object

        Args:
            - indent (int): Number of whitespaces used to indent the output. Defaults to 4.
            - newline (bool): Adds a newline to the end of the output. Defaults to True.

        Returns:
            - str: S-Expression of this object
        """
        indents = ' '*indent
        endline = '\n' if newline else ''

        expression =  f'{indents}(path "{dequote(self.path)}"\n'
        expression += f'{indents}  (reference "{dequote(self.reference)}") (unit {self.unit}) (value "{dequote(self.value)}") (footprint "{dequote(self.footprint)}")\n'
        expression += f'{indents}){endline}'
        return expression

@dataclass
class Rectangle():
    """The ``rectangle`` token defines a graphical rectangle in a schematic.

    Available since KiCad v7

    Documentation:
        https://dev-docs.kicad.org/en/file-formats/sexpr-intro/index.html#_symbol_rectangle
    """

    start: Position = field(default_factory=lambda: Position())
    """The ``start`` token attributes define the coordinates of the start point of the rectangle"""

    end: Position = field(default_factory=lambda: Position())
    """The ``end`` token attributes define the coordinates of the end point of the rectangle"""

    stroke: Stroke = field(default_factory=lambda: Stroke())
    """The ``stroke`` defines how the rectangle outline is drawn"""

    fill: Fill = field(default_factory=lambda: Fill())
    """The ``fill`` token attributes define how rectangle arc is filled"""

    uuid: Optional[str] = None
    """The optional ``uuid`` defines the universally unique identifier. Defaults to ``None.``"""

    @classmethod
    def from_sexpr(cls, exp: list) -> Rectangle:
        """Convert the given S-Expresstion into a Rectangle object

        Args:
            - exp (list): Part of parsed S-Expression ``(rectangle ...)``

        Raises:
            - Exception: When given parameter's type is not a list
            - Exception: When the first item of the list is not rectangle

        Returns:
            - Rectangle: Object of the class initialized with the given S-Expression
        """
        if not isinstance(exp, list):
            raise Exception("Expression does not have the correct type")

        if exp[0] != 'rectangle':
            raise Exception("Expression does not have the correct type")

        object = cls()

        for item in exp:
            if item[0] == 'start': object.start = Position().from_sexpr(item)
            if item[0] == 'end': object.end = Position().from_sexpr(item)
            if item[0] == 'stroke': object.stroke = Stroke().from_sexpr(item)
            if item[0] == 'fill': object.fill = Fill().from_sexpr(item)
            if item[0] == 'uuid': object.uuid = item[1]
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

        expression =  f'{indents}(rectangle (start {self.start.X} {self.start.Y}) (end {self.end.X} {self.end.Y})\n'
        expression += self.stroke.to_sexpr(indent+2)
        expression += self.fill.to_sexpr(indent+2)
        if self.uuid is not None:
            expression += f'{indents}  (uuid {self.uuid})\n'
        expression += f'{indents}){endline}'
        return expression

@dataclass
class Arc():
    """The ``Arc`` token defines a graphical arc in a schematic.

    Available since KiCad v7

    Documentation:
        - ???
    """

    start: Position = field(default_factory=lambda: Position())
    """The ``start`` token attributes define the coordinates of the start point of the arc"""

    mid: Position = field(default_factory=lambda: Position())
    """The ``end`` token attributes define the coordinates of the mid point of the arc"""

    end: Position = field(default_factory=lambda: Position())
    """The ``end`` token attributes define the coordinates of the end point of the arc"""

    stroke: Stroke = field(default_factory=lambda: Stroke())
    """The ``stroke`` defines how the arc outline is drawn"""

    fill: Fill = field(default_factory=lambda: Fill())
    """The ``fill`` token attributes define how the arc is filled"""

    uuid: Optional[str] = None
    """The optional ``uuid`` defines the universally unique identifier. Defaults to ``None.``"""

    @classmethod
    def from_sexpr(cls, exp: list) -> Arc:
        """Convert the given S-Expresstion into a Arc object

        Args:
            - exp (list): Part of parsed S-Expression ``(arc ...)``

        Raises:
            - Exception: When given parameter's type is not a list
            - Exception: When the first item of the list is not arc

        Returns:
            - Arc: Object of the class initialized with the given S-Expression
        """
        if not isinstance(exp, list):
            raise Exception("Expression does not have the correct type")

        if exp[0] != 'arc':
            raise Exception("Expression does not have the correct type")

        object = cls()

        for item in exp:
            if item[0] == 'start': object.start = Position().from_sexpr(item)
            if item[0] == 'mid': object.mid = Position().from_sexpr(item)
            if item[0] == 'end': object.end = Position().from_sexpr(item)
            if item[0] == 'stroke': object.stroke = Stroke().from_sexpr(item)
            if item[0] == 'fill': object.fill = Fill().from_sexpr(item)
            if item[0] == 'uuid': object.uuid = item[1]
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

        expression =  f'{indents}(arc (start {self.start.X} {self.start.Y}) (mid {self.mid.X} {self.mid.Y}) (end {self.end.X} {self.end.Y})\n'
        expression += self.stroke.to_sexpr(indent+2)
        expression += self.fill.to_sexpr(indent+2)
        if self.uuid is not None:
            expression += f'{indents}  (uuid {self.uuid})\n'
        expression += f'{indents}){endline}'
        return expression

@dataclass
class Circle():
    """The ``Circle`` token defines a graphical circle in a schematic.

    Available since KiCad v7

    Documentation:
        - ???
    """

    center: Position = field(default_factory=lambda: Position())
    """The ``center`` token attributes define the coordinates of the center point of the circle"""

    radius: float = 0.0
    """The ``radius`` token attributes define the radius of the circle"""

    stroke: Stroke = field(default_factory=lambda: Stroke())
    """The ``stroke`` defines how the circle outline is drawn"""

    fill: Fill = field(default_factory=lambda: Fill())
    """The ``fill`` token attributes define how the circle is filled"""

    uuid: Optional[str] = None
    """The optional ``uuid`` defines the universally unique identifier. Defaults to ``None.``"""

    @classmethod
    def from_sexpr(cls, exp: list) -> Circle:
        """Convert the given S-Expresstion into a Circle object

        Args:
            - exp (list): Part of parsed S-Expression ``(circle ...)``

        Raises:
            - Exception: When given parameter's type is not a list
            - Exception: When the first item of the list is not circle

        Returns:
            - Circle: Object of the class initialized with the given S-Expression
        """
        if not isinstance(exp, list):
            raise Exception("Expression does not have the correct type")

        if exp[0] != 'circle':
            raise Exception("Expression does not have the correct type")

        object = cls()

        for item in exp:
            if item[0] == 'center': object.center = Position().from_sexpr(item)
            if item[0] == 'radius': object.radius = item[1]
            if item[0] == 'stroke': object.stroke = Stroke().from_sexpr(item)
            if item[0] == 'fill': object.fill = Fill().from_sexpr(item)
            if item[0] == 'uuid': object.uuid = item[1]
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

        expression =  f'{indents}(circle (center {self.center.X} {self.center.Y}) (radius {self.radius})\n'
        expression += self.stroke.to_sexpr(indent+2)
        expression += self.fill.to_sexpr(indent+2)
        if self.uuid is not None:
            expression += f'{indents}  (uuid {self.uuid})\n'
        expression += f'{indents}){endline}'
        return expression
    
@dataclass
class NetclassFlag():
    """The ``netclass_flag`` token defines a netclass flag in a schematic.

    Available since KiCad v7

    Documentation:
        - ???
    """

    text: str = ""
    """The ``text`` token defines the text the netclass flag"""

    length: float = 2.54
    """The ``length`` token defines the length of the netclass flag"""

    shape: str = "round"
    """The ``shape`` token defines the shape of the netclass flag. Valid values are ``round``,
    ``rectangle``, ``dot`` or``diamond``."""

    position: Position = field(default_factory=lambda: Position)
    """The ``position`` token defines the position and rotation of the netclass flag"""

    effects: Effects = field(default_factory=lambda: Effects)
    """The ``effects`` token defines how the text is drawn"""

    properties: List[Property] = field(default_factory=list)
    """The ``properties`` token defines a list of properties the netclass is assigned to"""

    uuid: Optional[str] = None
    """The optional ``uuid`` defines the universally unique identifier"""

    fieldsAutoplaced: bool = False
    """The ``fields_autoplaced`` is a flag that indicates that any PROPERTIES associated
    with the netclas flag have been place automatically"""

    @classmethod
    def from_sexpr(cls, exp: list) -> NetclassFlag:
        """Convert the given S-Expresstion into a Circle object

        Args:
            - exp (list): Part of parsed S-Expression ``(netclass_flag ...)``

        Raises:
            - Exception: When given parameter's type is not a list
            - Exception: When the first item of the list is not netclass_flag

        Returns:
            - NetclassFlag: Object of the class initialized with the given S-Expression
        """
        if not isinstance(exp, list):
            raise Exception("Expression does not have the correct type")

        if exp[0] != 'netclass_flag':
            raise Exception("Expression does not have the correct type")

        object = cls()
        object.text = exp[1]
        for item in exp[2:]:
            if item[0] == 'length': object.length = item[1]
            if item[0] == 'shape': object.shape = item[1]
            if item[0] == 'at': object.position = Position.from_sexpr(item)
            if item[0] == 'fields_autoplaced': object.fieldsAutoplaced = True
            if item[0] == 'effects': object.effects = Effects.from_sexpr(item)
            if item[0] == 'uuid': object.uuid = item[1]
            if item[0] == 'property': object.properties.append(Property.from_sexpr(item))
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

        posA = f' {self.position.angle}' if self.position.angle is not None else ''
        fa = f' (fields_autoplaced)' if self.fieldsAutoplaced else ''

        expression =  f'{indents}(netclass_flag "{dequote(self.text)}" (length {self.length}) (shape {self.shape}) (at {self.position.X} {self.position.Y}{posA}){fa}\n'
        expression += self.effects.to_sexpr(indent+2)
        if self.uuid is not None:
            expression += f'{indents}  (uuid {self.uuid})\n'
        for property in self.properties:
            expression += property.to_sexpr(indent+2)
        expression += f'{indents}){endline}'
        return expression