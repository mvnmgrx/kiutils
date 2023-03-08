"""Symbol graphical items define all of the drawing items that are used in the symbol
definition. This includes text, text boxes, lines, rectangles, circles, arcs, polygons
and curves.

Author:
    (C) Marvin Mager - @mvnmgrx - 2022

License identifier:
    GPL-3.0

Major changes:
    16.02.2022 - created

Documentation taken from:
    https://dev-docs.kicad.org/en/file-formats/sexpr-intro/index.html#_symbol_graphic_items
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from kiutils.items.common import Fill, Position, Stroke, Effects, Fill
from kiutils.utils.strings import dequote

@dataclass
class SyArc():
    """The ``arc`` token defines a graphical arc in a symbol definition.

    Documentation:
        https://dev-docs.kicad.org/en/file-formats/sexpr-intro/index.html#_symbol_arc
    """

    private: bool = False
    """The ``private`` token defines if the arc is only visible in the symbol editor. Defaults
    to ``False``.

    Available since KiCad v7"""

    start: Position = field(default_factory=lambda: Position())
    """The ``start`` token defines the coordinates of start point of the arc"""

    mid: Position = field(default_factory=lambda: Position())
    """The ``mid`` token defines the coordinates of mid point of the arc"""

    end: Position = field(default_factory=lambda: Position())
    """The ``end`` token defines the coordinates of end point of the arc"""

    stroke: Stroke = field(default_factory=lambda: Stroke())
    """The ``stroke`` defines how the arc outline is drawn"""

    fill: Fill = field(default_factory=lambda: Fill())
    """The ``fill`` token attributes define how the arc is filled"""

    @classmethod
    def from_sexpr(cls, exp: list) -> SyArc:
        """Convert the given S-Expresstion into a SyArc object

        Args:
            - exp (list): Part of parsed S-Expression ``(arc ...)``

        Raises:
            - Exception: When given parameter's type is not a list
            - Exception: When the first item of the list is not arc

        Returns:
            - SyArc: Object of the class initialized with the given S-Expression
        """
        if not isinstance(exp, list):
            raise Exception("Expression does not have the correct type")

        if exp[0] != 'arc':
            raise Exception("Expression does not have the correct type")

        object = cls()

        for item in exp:
            if isinstance(item, str):
                if item == 'private': object.private = True
                continue
            if item[0] == 'start': object.start = Position().from_sexpr(item)
            if item[0] == 'mid': object.mid = Position().from_sexpr(item)
            if item[0] == 'end': object.end = Position().from_sexpr(item)
            if item[0] == 'stroke': object.stroke = Stroke().from_sexpr(item)
            if item[0] == 'fill': object.fill = Fill().from_sexpr(item)
        return object

    def to_sexpr(self, indent: int = 6, newline: bool = True) -> str:
        """Generate the S-Expression representing this object

        Args:
            - indent (int): Number of whitespaces used to indent the output. Defaults to 6.
            - newline (bool): Adds a newline to the end of the output. Defaults to True.

        Returns:
            - str: S-Expression of this object
        """
        indents = ' '*indent
        endline = '\n' if newline else ''

        startA = f' {self.start.angle}' if self.start.angle is not None else ''
        midA = f' {self.mid.angle}' if self.mid.angle is not None else ''
        endA = f' {self.end.angle}' if self.end.angle is not None else ''
        private = ' private' if self.private else ''

        expression =  f'{indents}(arc{private} (start {self.start.X} {self.start.Y}{startA}) (mid {self.mid.X} {self.mid.Y}{midA}) (end {self.end.X} {self.end.Y}{endA})\n'
        expression += self.stroke.to_sexpr(indent+2)
        expression += self.fill.to_sexpr(indent+2)
        expression += f'{indents}){endline}'
        return expression

@dataclass
class SyCircle():
    """The ``circle`` token defines a graphical circle in a symbol definition.

    Documentation:
        https://dev-docs.kicad.org/en/file-formats/sexpr-intro/index.html#_symbol_circle
    """

    private: bool = False
    """The ``private`` token defines if the circle is only visible in the symbol editor. Defaults
    to ``False``.

    Available since KiCad v7"""

    center: Position = field(default_factory=lambda: Position())
    """The ``center`` token defines the coordinates of center point of the circle"""

    radius: float = 0.0
    """The ``radius`` token defines the length of the radius of the circle"""

    stroke: Stroke = field(default_factory=lambda: Stroke())
    """The ``stroke`` defines how the circle outline is drawn"""

    fill: Fill = field(default_factory=lambda: Fill())
    """The ``fill`` token attributes define how the circle is filled"""

    @classmethod
    def from_sexpr(cls, exp: list) -> SyCircle:
        """Convert the given S-Expresstion into a SyCircle object

        Args:
            - exp (list): Part of parsed S-Expression ``(circle ...)``

        Raises:
            - Exception: When given parameter's type is not a list
            - Exception: When the first item of the list is not circle

        Returns:
            - SyCircle: Object of the class initialized with the given S-Expression
        """
        if not isinstance(exp, list):
            raise Exception("Expression does not have the correct type")

        if exp[0] != 'circle':
            raise Exception("Expression does not have the correct type")

        object = cls()

        for item in exp:
            if isinstance(item, str):
                if item == 'private': object.private = True
                continue
            if item[0] == 'center': object.center = Position().from_sexpr(item)
            if item[0] == 'radius': object.radius = item[1]
            if item[0] == 'stroke': object.stroke = Stroke().from_sexpr(item)
            if item[0] == 'fill': object.fill = Fill().from_sexpr(item)
        return object

    def to_sexpr(self, indent: int = 6, newline: bool = True) -> str:
        """Generate the S-Expression representing this object

        Args:
            - indent (int): Number of whitespaces used to indent the output. Defaults to 6.
            - newline (bool): Adds a newline to the end of the output. Defaults to True.

        Returns:
            - str: S-Expression of this object
        """
        indents = ' '*indent
        endline = '\n' if newline else ''
        private = ' private' if self.private else ''

        expression =  f'{indents}(circle{private} (center {self.center.X} {self.center.Y}) (radius {self.radius})\n'
        expression += self.stroke.to_sexpr(indent+2)
        expression += self.fill.to_sexpr(indent+2)
        expression += f'{indents}){endline}'
        return expression

@dataclass
class SyCurve():
    """The ``curve`` token defines a graphical Qubic Bezier curve.

    Documentation:
        https://dev-docs.kicad.org/en/file-formats/sexpr-intro/index.html#_symbol_curve
    """

    points: List[Position] = field(default_factory=list)
    """The ``points`` token defines the four X/Y coordinates of each point of the curve"""

    stroke: Stroke = field(default_factory=lambda: Stroke())
    """The ``stroke`` defines how the curve outline is drawn"""

    fill: Fill = field(default_factory=lambda: Fill())
    """The ``fill`` token attributes define how curve arc is filled"""

    @classmethod
    def from_sexpr(cls, exp: list) -> SyCurve:
        """Convert the given S-Expresstion into a SyCurve object

        Args:
            - exp (list): Part of parsed S-Expression ``(curve ...)``

        Raises:
            - Exception: When given parameter's type is not a list
            - Exception: When the first item of the list is not curve

        Returns:
            - SyCurve: Object of the class initialized with the given S-Expression
        """
        if not isinstance(exp, list):
            raise Exception("Expression does not have the correct type")

        if exp[0] != 'curve':
            raise Exception("Expression does not have the correct type")

        object = cls()
        for item in exp:
            if item[0] == 'stroke': object.stroke = Stroke().from_sexpr(item)
            if item[0] == 'fill': object.fill = Fill().from_sexpr(item)
            if item[0] == 'pts':
                for point in item[1:]:
                    object.points.append(Position().from_sexpr(point))
        return object

    def to_sexpr(self, indent: int = 6, newline: bool = True) -> str:
        """Generate the S-Expression representing this object

        Args:
            - indent (int): Number of whitespaces used to indent the output. Defaults to 6.
            - newline (bool): Adds a newline to the end of the output. Defaults to True.

        Returns:
            - str: S-Expression of this object
        """
        indents = ' '*indent
        endline = '\n' if newline else ''

        expression =  f'{indents}(curve\n'
        expression =  f'{indents}  (pts\n'
        for point in self.points:
            expression =  f'{indents}    (xy {point.X} {point.Y})\n'
        expression =  f'{indents}  )\n'
        expression += self.stroke.to_sexpr(indent+2)
        expression += self.fill.to_sexpr(indent+2)
        expression += f'{indents}){endline}'
        return expression

@dataclass
class SyPolyLine():
    """The ``polyline`` token defines one or more graphical lines that may or may not define a polygon.

    Documentation:
        https://dev-docs.kicad.org/en/file-formats/sexpr-intro/index.html#_symbol_line
    """

    points: List[Position] = field(default_factory=list)
    """The ``points`` token defines the four X/Y coordinates of each point of the polyline"""

    stroke: Stroke = field(default_factory=lambda: Stroke())
    """The ``stroke`` defines how the polyline outline is drawn"""

    fill: Fill = field(default_factory=lambda: Fill())
    """The ``fill`` token attributes define how polyline arc is filled"""

    @classmethod
    def from_sexpr(cls, exp: list) -> SyPolyLine:
        """Convert the given S-Expresstion into a SyPolyLine object

        Args:
            - exp (list): Part of parsed S-Expression ``(polyline ...)``

        Raises:
            - Exception: When given parameter's type is not a list
            - Exception: When the first item of the list is not polyline

        Returns:
            - SyPolyLine: Object of the class initialized with the given S-Expression
        """
        if not isinstance(exp, list):
            raise Exception("Expression does not have the correct type")

        if exp[0] != 'polyline':
            raise Exception("Expression does not have the correct type")

        object = cls()
        for item in exp:
            if item[0] == 'stroke': object.stroke = Stroke().from_sexpr(item)
            if item[0] == 'fill': object.fill = Fill().from_sexpr(item)
            if item[0] == 'pts':
                for point in item[1:]:
                    object.points.append(Position().from_sexpr(point))
        return object

    def to_sexpr(self, indent: int = 6, newline: bool = True) -> str:
        """Generate the S-Expression representing this object

        Args:
            - indent (int): Number of whitespaces used to indent the output. Defaults to 6.
            - newline (bool): Adds a newline to the end of the output. Defaults to True.

        Returns:
            - str: S-Expression of this object
        """
        indents = ' '*indent
        endline = '\n' if newline else ''

        expression =  f'{indents}(polyline\n'
        expression +=  f'{indents}  (pts\n'
        for point in self.points:
            expression +=  f'{indents}    (xy {point.X} {point.Y})\n'
        expression += f'{indents}  )\n'
        expression += self.stroke.to_sexpr(indent+2)
        expression += self.fill.to_sexpr(indent+2)
        expression += f'{indents}){endline}'
        return expression

@dataclass
class SyRect():
    """The ``rectangle`` token defines a graphical rectangle in a symbol definition.

    Documentation:
        https://dev-docs.kicad.org/en/file-formats/sexpr-intro/index.html#_symbol_rectangle
    """

    private: bool = False
    """The ``private`` token defines if the rectangle is only visible in the symbol editor. Defaults
    to ``False``.
    
    Available since KiCad v7"""

    start: Position = field(default_factory=lambda: Position())
    """The ``start`` token attributes define the coordinates of the start point of the rectangle"""

    end: Position = field(default_factory=lambda: Position())
    """The ``end`` token attributes define the coordinates of the end point of the rectangle"""

    stroke: Stroke = field(default_factory=lambda: Stroke())
    """The ``stroke`` defines how the rectangle outline is drawn"""

    fill: Fill = field(default_factory=lambda: Fill())
    """The ``fill`` token attributes define how rectangle arc is filled"""

    @classmethod
    def from_sexpr(cls, exp: list) -> SyRect:
        """Convert the given S-Expresstion into a SyRect object

        Args:
            - exp (list): Part of parsed S-Expression ``(rectangle ...)``

        Raises:
            - Exception: When given parameter's type is not a list
            - Exception: When the first item of the list is not rectangle

        Returns:
            - SyRect: Object of the class initialized with the given S-Expression
        """
        if not isinstance(exp, list):
            raise Exception("Expression does not have the correct type")

        if exp[0] != 'rectangle':
            raise Exception("Expression does not have the correct type")

        object = cls()

        for item in exp:
            if isinstance(item, str):
                if item == 'private': object.private = True
                continue
            if item[0] == 'start': object.start = Position().from_sexpr(item)
            if item[0] == 'end': object.end = Position().from_sexpr(item)
            if item[0] == 'stroke': object.stroke = Stroke().from_sexpr(item)
            if item[0] == 'fill': object.fill = Fill().from_sexpr(item)
        return object

    def to_sexpr(self, indent: int = 6, newline: bool = True) -> str:
        """Generate the S-Expression representing this object

        Args:
            - indent (int): Number of whitespaces used to indent the output. Defaults to 6.
            - newline (bool): Adds a newline to the end of the output. Defaults to True.

        Returns:
            - str: S-Expression of this object
        """
        indents = ' '*indent
        endline = '\n' if newline else ''
        private = ' private' if self.private else ''

        expression =  f'{indents}(rectangle{private} (start {self.start.X} {self.start.Y}) (end {self.end.X} {self.end.Y})\n'
        expression += self.stroke.to_sexpr(indent+2)
        expression += self.fill.to_sexpr(indent+2)
        expression += f'{indents}){endline}'
        return expression

@dataclass
class SyText():
    """The ``text`` token defines a graphical text in a symbol definition.

    Documentation:
        https://dev-docs.kicad.org/en/file-formats/sexpr-intro/index.html#_symbol_text
    """

    text: str = ""
    """The ``text`` attribute is a quoted string that defines the text"""

    position: Position = field(default_factory=lambda: Position())
    """The ``position`` defines the X and Y coordinates and rotation angle of the text"""

    effects: Effects = field(default_factory=lambda: Effects())
    """The ``effects`` token defines how the text is displayed"""

    @classmethod
    def from_sexpr(cls, exp: list) -> SyText:
        """Convert the given S-Expresstion into a SyText object

        Args:
            - exp (list): Part of parsed S-Expression ``(text ...)``

        Raises:
            - Exception: When given parameter's type is not a list
            - Exception: When the first item of the list is not text

        Returns:
            - SyText: Object of the class initialized with the given S-Expression
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
        return object

    def to_sexpr(self, indent: int = 6, newline: bool = True) -> str:
        """Generate the S-Expression representing this object

        Args:
            - indent (int): Number of whitespaces used to indent the output. Defaults to 6.
            - newline (bool): Adds a newline to the end of the output. Defaults to True.

        Returns:
            - str: S-Expression of this object
        """
        indents = ' '*indent
        endline = '\n' if newline else ''

        posA = f' {self.position.angle}' if self.position.angle is not None else ''

        expression =  f'{indents}(text "{dequote(self.text)}" (at {self.position.X} {self.position.Y}{posA})\n'
        expression += f'{indents}  {self.effects.to_sexpr()}'
        expression += f'{indents}){endline}'
        return expression

@dataclass
class SyTextBox():
    """The ``text_box`` token defines a text box inside a symbol

    Available since KiCad v7

    Documentation:
        ????
    """

    # NOTE: This is almost the same implementation as in ``kiutils.items.schitems.TextBox`` but
    #       used in a different context.

    text: str = ""
    """The ``text`` token defines the text string"""

    private: bool = False
    """The ``private`` token defines if the text box is only visible in the symbol editor. Defaults
    to ``False``."""

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
    def from_sexpr(cls, exp: list) -> SyTextBox:
        """Convert the given S-Expresstion into a SyTextBox object

        Args:
            - exp (list): Part of parsed S-Expression ``(text_box ...)``

        Raises:
            - Exception: When given parameter's type is not a list
            - Exception: When the first item of the list is not text_box

        Returns:
            - SyTextBox: Object of the class initialized with the given S-Expression
        """
        if not isinstance(exp, list):
            raise Exception("Expression does not have the correct type")

        if exp[0] != 'text_box':
            raise Exception("Expression does not have the correct type")

        object = cls()

        # Extract "private" token, if any is present
        if exp[1] == "private" and not isinstance(exp[2], list):
            object.private = True
            object.text = exp[2]
            start_at = 3
        else:
            object.text = exp[1]
            start_at = 2

        for item in exp[start_at:]:
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
        private = ' private' if self.private else ''

        expression =  f'{indents}(text_box{private} "{dequote(self.text)}"\n'
        expression += f'{indents}  (at {self.position.X} {self.position.Y}{posA}) (size {self.size.X} {self.size.Y})\n'
        expression += self.stroke.to_sexpr(indent+2)
        expression += self.fill.to_sexpr(indent+2)
        expression += self.effects.to_sexpr(indent+2)
        if self.uuid is not None:
            expression += f'{indents}  (uuid {self.uuid})\n'
        expression += f'{indents}){endline}'
        return expression