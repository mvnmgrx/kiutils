"""Footprint graphical items define all of the drawing items that are used in the footprint
definition. This includes text, text boxes, lines, rectangles, circles, arcs, polygons, curves
and dimensions.

Author:
    (C) Marvin Mager - @mvnmgrx - 2022

License identifier:
    GPL-3.0

Major changes:
    08.02.2022 - created

Documentation taken from:
    https://dev-docs.kicad.org/en/file-formats/sexpr-intro/index.html#_footprint_graphics_items
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, List
from copy import deepcopy

from kiutils.items.common import Stroke, Position, Effects
from kiutils.utils.strings import dequote

# FIXME: Several classes have a ``stroke`` member. This feature will be introduced in KiCad 7 and 
#        has yet to be tested here.

@dataclass
class FpText():
    """The ``fp_text`` token defines a graphic line in a footprint definition.

    Documentation:
        https://dev-docs.kicad.org/en/file-formats/sexpr-intro/index.html#_footprint_text
    """

    type: str = "reference"
    """The ``type`` attribute defines the type of text. Valid types are ``reference``, ``value``, and
    ``user``"""

    text: str = "%REF"
    """The ``text`` attribute is a string that defines the text"""

    position: Position = field(default_factory=lambda: Position())
    """The ``position`` defines the X and Y position coordinates and optional orientation angle of
    the text"""

    layer: str = "F.Cu"
    """The ``layer`` token defines the canonical layer the text resides on"""

    hide: bool = False
    """The optional ``hide`` token, defines if the text is hidden"""

    effects: Effects = field(default_factory=lambda: Effects())
    """The ``effects`` token defines how the text is displayed"""

    tstamp: Optional[str] = None      # Used since KiCad 6
    """The ``tstamp`` token defines the unique identifier of the text object"""

    @classmethod
    def from_sexpr(cls, exp: list) -> FpText:
        """Convert the given S-Expresstion into a FpText object

        Args:
            - exp (list): Part of parsed S-Expression ``(fp_text ...)``

        Raises:
            - Exception: When given parameter's type is not a list
            - Exception: When the first item of the list is not fp_text

        Returns:
            - FpText: Object of the class initialized with the given S-Expression
        """
        if not isinstance(exp, list):
            raise Exception("Expression does not have the correct type")

        if exp[0] != 'fp_text':
            raise Exception("Expression does not have the correct type")

        object = cls()
        object.type = exp[1]
        object.text = exp[2]
        for item in exp[3:]:
            if type(item) != type([]):
                if item == 'hide': object.hide = True
                continue
            if item[0] == 'at': object.position = Position().from_sexpr(item)
            if item[0] == 'layer': object.layer = item[1]
            if item[0] == 'effects': object.effects = Effects().from_sexpr(item)
            if item[0] == 'tstamp': object.tstamp = item[1]
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

        hide = ' hide' if self.hide else ''
        unlocked = ' unlocked' if self.position.unlocked else ''
        posA = f' {self.position.angle}' if self.position.angle is not None else ''

        expression =  f'{indents}(fp_text {self.type} "{dequote(self.text)}" (at {self.position.X} {self.position.Y}{posA}{unlocked}) (layer "{dequote(self.layer)}"){hide}\n'
        expression += f'{indents}  {self.effects.to_sexpr()}'
        if self.tstamp is not None:
            expression += f'{indents}  (tstamp {self.tstamp})\n'
        expression += f'{indents}){endline}'
        return expression

@dataclass
class FpLine():
    """The ``fp_line`` token defines a graphic line in a footprint definition.

    Documentation:
        https://dev-docs.kicad.org/en/file-formats/sexpr-intro/index.html#_footprint_line
    """

    start: Position = field(default_factory=lambda: Position())
    """The ``start`` token defines the coordinates of the upper left corner of the line"""

    end: Position = field(default_factory=lambda: Position())
    """The ``end`` token defines the coordinates of the low right corner of the line"""

    layer: str = "F.Cu"
    """The ``layer`` token defines the canonical layer the line resides on"""

    width: Optional[float] = 0.12     # Used for KiCad < 7
    """The ``width`` token defines the line width of the line. (prior to version 7)"""

    stroke: Optional[Stroke] = None   # Used for KiCad >= 7
    """The ``stroke`` describes the line width and style of the line. (version 7)"""

    # FIXME: This is not implemented in to_sexpr() because it does not seem to be used on lines
    #        in footprints. Further testing required ..
    locked: bool = False
    """The optional ``locked`` token defines if the line cannot be edited"""

    tstamp: Optional[str] = None      # Used since KiCad 6
    """The ``tstamp`` token defines the unique identifier of the line object"""

    @classmethod
    def from_sexpr(cls, exp: list) -> FpLine:
        """Convert the given S-Expresstion into a FpLine object

        Args:
            - exp (list): Part of parsed S-Expression ``(fp_line ...)``

        Raises:
            - Exception: When given parameter's type is not a list
            - Exception: When the first item of the list is not fp_line

        Returns:
            - FpLine: Object of the class initialized with the given S-Expression
        """
        if not isinstance(exp, list):
            raise Exception("Expression does not have the correct type")

        if exp[0] != 'fp_line':
            raise Exception("Expression does not have the correct type")

        object = cls()
        for item in exp:
            if type(item) != type([]):
                if item == 'locked': object.locked = True
                else: continue

            if item[0] == 'start': object.start = Position.from_sexpr(item)
            if item[0] == 'end': object.end = Position.from_sexpr(item)
            if item[0] == 'layer': object.layer = item[1]
            if item[0] == 'tstamp': object.tstamp = item[1]
            if item[0] == 'width':
                object.width = item[1]
                object.stroke = None
            if item[0] == 'stroke':
                object.stroke = Stroke.from_sexpr(item)
                object.width = None

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
        tstamp = f' (tstamp {self.tstamp})' if self.tstamp is not None else ''
        if self.width is not None:
            width = f' (width {self.width})'
        elif self.stroke is not None:
            width = f' {self.stroke.to_sexpr(indent=0, newline=False)}'
        else:
            width = ''

        return f'{indents}(fp_line (start {self.start.X} {self.start.Y}) (end {self.end.X} {self.end.Y}) (layer "{dequote(self.layer)}"){width}{tstamp}){endline}'

@dataclass
class FpRect():
    """The ``fp_rect`` token defines a graphic rectangle in a footprint definition.

    Documentation:
        https://dev-docs.kicad.org/en/file-formats/sexpr-intro/index.html#_footprint_rectangle
    """

    start: Position = field(default_factory=lambda: Position())
    """The ``start`` token defines the coordinates of the upper left corner of the rectangle"""

    end: Position = field(default_factory=lambda: Position())
    """The ``end`` token defines the coordinates of the low right corner of the rectangle"""

    layer: str = "F.Cu"
    """The ``layer`` token defines the canonical layer the rectangle resides on"""

    width: Optional[float] = 0.12     # Used for KiCad < 7
    """The ``width`` token defines the line width of the rectangle. (prior to version 7)"""

    stroke: Optional[Stroke] = None   # Used for KiCad >= 7
    """The ``stroke`` describes the line width and style of the rectangle. (version 7)"""

    fill: Optional[str] = None
    """The optional ``fill`` toke defines how the rectangle is filled. Valid fill types are solid
    and none. If not defined, the rectangle is not filled."""

    locked: bool = False
    """The optional ``locked`` token defines if the rectangle cannot be edited"""

    tstamp: Optional[str] = None      # Used since KiCad 6
    """The ``tstamp`` token defines the unique identifier of the rectangle object"""

    @classmethod
    def from_sexpr(cls, exp: list) -> FpRect:
        """Convert the given S-Expresstion into a FpRect object

        Args:
            - exp (list): Part of parsed S-Expression ``(fp_rect ...)``

        Raises:
            - Exception: When given parameter's type is not a list
            - Exception: When the first item of the list is not fp_rect

        Returns:
            - FpRect: Object of the class initialized with the given S-Expression
        """
        if not isinstance(exp, list):
            raise Exception("Expression does not have the correct type")

        if exp[0] != 'fp_rect':
            raise Exception("Expression does not have the correct type")

        object = cls()
        for item in exp:
            if type(item) != type([]):
                if item == 'locked': object.locked = True
                else: continue

            if item[0] == 'start': object.start = Position.from_sexpr(item)
            if item[0] == 'end': object.end = Position.from_sexpr(item)
            if item[0] == 'layer': object.layer = item[1]
            if item[0] == 'tstamp': object.tstamp = item[1]
            if item[0] == 'fill': object.fill = item[1]
            if item[0] == 'width':
                object.width = item[1]
                object.stroke = None
            if item[0] == 'stroke':
                object.stroke = Stroke.from_sexpr(item)
                object.width = None

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

        tstamp = f' (tstamp {self.tstamp})' if self.tstamp is not None else ''
        locked = ' locked' if self.locked else ''
        fill = f' (fill {self.fill})' if self.fill is not None else ''

        if self.width is not None:
            width = f' (width {self.width})'
        elif self.stroke is not None:
            width = f' {self.stroke.to_sexpr(indent=0, newline=False)}'
        else:
            width = ''

        return f'{indents}(fp_rect (start {self.start.X} {self.start.Y}) (end {self.end.X} {self.end.Y}) (layer "{dequote(self.layer)}"){width}{fill}{locked}{tstamp}){endline}'

@dataclass
class FpTextBox():
    """TBD when KiCad 7 is released

    Documentation:
        https://dev-docs.kicad.org/en/file-formats/sexpr-intro/index.html#_footprint_text_box
    """

    locked: bool = False
    text: str = "text"
    start: Optional[Position] = None
    end: Optional[Position] = None
    pts: List[Position] = field(default_factory=list)
    angle: Optional[float] = None
    layer: str = "F.Cu"
    tstamp: Optional[str] = None
    effects: Effects = field(default_factory=lambda: Effects())
    stroke: Stroke = field(default_factory=lambda: Stroke())
    renderCache: Optional[str] = None

    @classmethod
    def from_sexpr(cls, exp: list) -> FpTextBox:
        """Not implemented yet"""
        raise NotImplementedError("FpTextBoxes are not yet handled! Please report this bug along with the file being parsed.")

    def to_sexpr(self, indent: int = 2, newline: bool = True) -> str:
        """Not implemented yet"""
        raise NotImplementedError("FpTextBoxes are not yet handled! Please report this bug along with the file being parsed.")

@dataclass
class FpCircle():
    """The ``fp_circle `` token defines a graphic circle in a footprint definition.

    Documentation:
        https://dev-docs.kicad.org/en/file-formats/sexpr-intro/index.html#_footprint_circle
    """

    center: Position = field(default_factory=lambda: Position())
    """The ``center`` token defines the coordinates of the center of the circle"""

    end: Position = field(default_factory=lambda: Position())
    """The ``end`` token defines the coordinates of the low right corner of the circle"""

    layer: str = "F.Cu"
    """The ``layer`` token defines the canonical layer the circle resides on"""

    width: Optional[float] = 0.12     # Used for KiCad < 7
    """The ``width`` token defines the line width of the circle. (prior to version 7)"""

    stroke: Optional[Stroke] = None   # Used for KiCad >= 7
    """The ``stroke`` describes the line width and style of the circle. (version 7)"""

    fill: Optional[str] = None
    """The optional ``fill`` toke defines how the circle is filled. Valid fill types are solid and none. If not defined, the circle is not filled."""

    locked: bool = False
    """The optional ``locked`` token defines if the circle cannot be edited"""

    tstamp: Optional[str] = None      # Used since KiCad 6
    """The ``tstamp`` token defines the unique identifier of the circle object"""

    @classmethod
    def from_sexpr(cls, exp: list) -> FpCircle:
        """Convert the given S-Expresstion into a FpCircle object

        Args:
            - exp (list): Part of parsed S-Expression ``(fp_circle ...)``

        Raises:
            - Exception: When given parameter's type is not a list
            - Exception: When the first item of the list is not fp_circle

        Returns:
            - FpCircle: Object of the class initialized with the given S-Expression
        """
        if not isinstance(exp, list):
            raise Exception("Expression does not have the correct type")

        if exp[0] != 'fp_circle':
            raise Exception("Expression does not have the correct type")

        object = cls()
        for item in exp:
            if type(item) != type([]):
                if item == 'locked': object.locked = True
                else: continue

            if item[0] == 'center': object.center = Position.from_sexpr(item)
            if item[0] == 'end': object.end = Position.from_sexpr(item)
            if item[0] == 'layer': object.layer = item[1]
            if item[0] == 'tstamp': object.tstamp = item[1]
            if item[0] == 'fill': object.fill = item[1]
            if item[0] == 'width':
                object.width = item[1]
                object.stroke = None
            if item[0] == 'stroke':
                object.stroke = Stroke.from_sexpr(item)
                object.width = None

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

        tstamp = f' (tstamp {self.tstamp})' if self.tstamp is not None else ''
        locked = ' locked' if self.locked else ''
        fill = f' (fill {self.fill})' if self.fill is not None else ''

        if self.width is not None:
            width = f' (width {self.width})'
        elif self.stroke is not None:
            width = f' {self.stroke.to_sexpr(indent=0, newline=False)}'
        else:
            width = ''

        return f'{indents}(fp_circle (center {self.center.X} {self.center.Y}) (end {self.end.X} {self.end.Y}) (layer "{dequote(self.layer)}"){width}{fill}{locked}{tstamp}){endline}'

@dataclass
class FpArc():
    """The ``fp_arc`` token defines a graphic arc in a footprint definition.

    Documentation:
        https://dev-docs.kicad.org/en/file-formats/sexpr-intro/index.html#_footprint_arc
    """

    start: Position = field(default_factory=lambda: Position())
    """The ``start`` token defines the coordinates of the start position of the arc radius"""

    mid: Position = field(default_factory=lambda: Position())
    """The ``mid`` token defines the coordinates of the midpoint along the arc"""

    end: Position = field(default_factory=lambda: Position())
    """The ``end`` token defines the coordinates of the end position of the arc radius"""

    layer: str = "F.Cu"
    """The ``layer`` token defines the canonical layer the arc resides on"""

    width: Optional[float] = 0.12     # Used for KiCad < 7
    """The ``width`` token defines the line width of the arc. (prior to version 7)"""

    stroke: Optional[Stroke] = None   # Used for KiCad >= 7
    """The ``stroke`` describes the line width and style of the arc. (version 7)"""

    locked: bool = False
    """The optional ``locked`` token defines if the arc cannot be edited"""

    tstamp: Optional[str] = None      # Used since KiCad 6
    """The ``tstamp`` token defines the unique identifier of the arc object"""

    @classmethod
    def from_sexpr(cls, exp: list) -> FpArc:
        """Convert the given S-Expresstion into a FpArc object

        Args:
            - exp (list): Part of parsed S-Expression ``(fp_arc ...)``

        Raises:
            - Exception: When given parameter's type is not a list
            - Exception: When the first item of the list is not fp_arc
            - Exception: When a legacy `angle` token and a modern `mid` token are both provided

        Returns:
            - FpArc: Object of the class initialized with the given S-Expression
        """
        if not isinstance(exp, list):
            raise Exception("Expression does not have the correct type")

        if exp[0] != 'fp_arc':
            raise Exception("Expression does not have the correct type")

        object = cls()

        # HACK: Assumes both legacy and modern `fp_arc`s are possible in the same file.
        #   Parsing method should be determined by footprint version number.
        #   KiCad source has version <= "20210925" activate legacy fp_arc parsing.
        #   Source: https://gitlab.com/kicad/code/kicad/-/blob/master/pcbnew/plugins/kicad/pcb_plugin.h#L136
        start = None
        mid = None
        end = None
        angle = None

        for item in exp:
            if type(item) != type([]):
                if item == 'locked': object.locked = True
                else: continue

            if item[0] == 'start': start = Position.from_sexpr(item)
            if item[0] == 'mid': mid = Position.from_sexpr(item)
            if item[0] == 'end': end = Position.from_sexpr(item)
            if item[0] == 'angle': angle = item[1]
            if item[0] == 'layer': object.layer = item[1]
            if item[0] == 'tstamp': object.tstamp = item[1]
            if item[0] == 'width':
                object.width = item[1]
                object.stroke = None
            if item[0] == 'stroke':
                object.stroke = Stroke.from_sexpr(item)
                object.width = None
        
        # FIXME: Legacy upgrade code has not been tested
        if angle is not None and mid is not None:
            raise Exception('Legacy `angle` token and modern `mid` token both provided for fp_arc')

        if angle is not None:
            # Legacy fp_arc is as follows:
            #   (start x y): The position of the centre of the circle that is the basis
            #       of the arc.
            #   (end x y): The starting point of the arc. Both the radius of the arc
            #       and the start angle are calculated from this point.
            #   (angle a): The angular span that the arc covers, from the start angle, in
            #       clock-wise direction. It is added to the start angle to find the end angle.
            # Source: https://www.compuphase.com/electronics/LibraryFileFormats.pdf

            centerOfCircle = start
            startingPointOfArc = end

            # Following code based off of KiCad source code:
            #   https://gitlab.com/kicad/code/kicad/-/blob/master/pcbnew/fp_shape.cpp#L193
            endOfArc = startingPointOfArc

            # Get midpoint by rotating halfway
            endOfArc.rotate_around_center(centerOfCircle, -1 * (angle / 2))
            mid = deepcopy(endOfArc)
            endOfArc.rotate_around_center(centerOfCircle, -1 * (angle / 2))

            # Swap points on negative angle as that is what the KiCad source does
            if angle < 0.0:
                startingPointOfArc, endOfArc = endOfArc, startingPointOfArc

            start = startingPointOfArc
            end = endOfArc

        object.start = start
        object.mid = mid
        object.end = end

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

        tstamp = f' (tstamp {self.tstamp})' if self.tstamp is not None else ''
        locked = ' locked' if self.locked else ''

        if self.width is not None:
            width = f' (width {self.width})'
        elif self.stroke is not None:
            width = f' {self.stroke.to_sexpr(indent=0, newline=False)}'
        else:
            width = ''

        return f'{indents}(fp_arc (start {self.start.X} {self.start.Y}) (mid {self.mid.X} {self.mid.Y}) (end {self.end.X} {self.end.Y}) (layer "{dequote(self.layer)}"){width}{locked}{tstamp}){endline}'

@dataclass
class FpPoly():
    """The ``fp_poly`` token defines a graphic polygon in a footprint definition.

    Documentation:
        https://dev-docs.kicad.org/en/file-formats/sexpr-intro/index.html#_footprint_polygon
    """

    layer: str = "F.Cu"
    """The ``layer`` token defines the canonical layer the polygon resides on"""

    coordinates: List[Position] = field(default_factory=list)
    """The ``coordinates`` define the list of X/Y coordinates of the polygon outline"""

    width: Optional[float] = 0.12     # Used for KiCad < 7
    """The ``width`` token defines the line width of the polygon. (prior to version 7)"""

    stroke: Optional[Stroke] = None   # Used for KiCad >= 7
    """The ``stroke`` describes the line width and style of the polygon. (version 7)"""

    fill: Optional[str] = None
    """The optional ``fill`` toke defines how the polygon is filled. Valid fill types are solid
    and none. If not defined, the rectangle is not filled."""

    locked: bool = False
    """The optional ``locked`` token defines if the polygon cannot be edited"""

    tstamp: Optional[str] = None      # Used since KiCad 6
    """The ``tstamp`` token defines the unique identifier of the polygon object"""

    @classmethod
    def from_sexpr(cls, exp: list) -> FpPoly:
        """Convert the given S-Expresstion into a FpPoly object

        Args:
            - exp (list): Part of parsed S-Expression ``(fp_poly ...)``

        Raises:
            - Exception: When given parameter's type is not a list
            - Exception: When the first item of the list is not fp_poly

        Returns:
            - FpPoly: Object of the class initialized with the given S-Expression
        """
        if not isinstance(exp, list):
            raise Exception("Expression does not have the correct type")

        if exp[0] != 'fp_poly':
            raise Exception("Expression does not have the correct type")

        object = cls()

        for item in exp:
            if type(item) != type([]):
                if item == 'locked': object.locked = True
                else: continue

            if item[0] == 'pts':
                for point in item[1:]:
                    object.coordinates.append(Position().from_sexpr(point))
            if item[0] == 'layer': object.layer = item[1]
            if item[0] == 'tstamp': object.tstamp = item[1]
            if item[0] == 'fill': object.fill = item[1]
            if item[0] == 'width':
                object.width = item[1]
                object.stroke = None
            if item[0] == 'stroke':
                object.stroke = Stroke.from_sexpr(item)
                object.width = None

        return object

    def to_sexpr(self, indent: int = 2, newline: bool = True) -> str:
        """Generate the S-Expression representing this object. When no coordinates are set
        in the polygon, the resulting S-Expression will be left empty.

        Args:
            - indent (int): Number of whitespaces used to indent the output. Defaults to 2.
            - newline (bool): Adds a newline to the end of the output. Defaults to True.

        Returns:
            - str: S-Expression of this object
        """
        indents = ' '*indent
        endline = '\n' if newline else ''
        if len(self.coordinates) == 0:
            return f'{indents}{endline}'

        tstamp = f' (tstamp {self.tstamp})' if self.tstamp is not None else ''
        locked = ' locked' if self.locked else ''
        fill = f' (fill {self.fill})' if self.fill is not None else ''

        if self.width is not None:
            width = f' (width {self.width})'
        elif self.stroke is not None:
            width = f' {self.stroke.to_sexpr(indent=0, newline=False)}'
        else:
            width = ''

        expression = f'{indents}(fp_poly (pts\n'
        for point in self.coordinates:
            expression += f'{indents}    (xy {point.X} {point.Y})\n'
        expression += f'{indents}  ) (layer "{dequote(self.layer)}"){width}{fill}{locked}{tstamp}){endline}'
        return expression

@dataclass
class FpCurve():
    """The ``fp_curve`` token defines a graphic Cubic Bezier curve in a footprint definition.

    Documentation:
        https://dev-docs.kicad.org/en/file-formats/sexpr-intro/index.html#_footprint_curve
    """

    coordinates: List[Position] = field(default_factory=list)
    """The ``coordinates`` define the list of X/Y coordinates of the curve outline"""

    layer: str = "F.Cu"
    """The ``layer`` token defines the canonical layer the curve resides on"""

    width: Optional[float] = 0.12     # Used for KiCad < 7
    """The ``width`` token defines the line width of the curve. (prior to version 7)"""

    stroke: Optional[Stroke] = None   # Used for KiCad >= 7
    """The ``stroke`` describes the line width and style of the curve. (version 7)"""

    locked: bool = False
    """The optional ``locked`` token defines if the curve cannot be edited"""

    tstamp: Optional[str] = None      # Used since KiCad 6
    """The ``tstamp`` token defines the unique identifier of the curve object"""

    @classmethod
    def from_sexpr(cls, exp: list) -> FpCurve:
        """Convert the given S-Expresstion into a FpCurve object

        Args:
            - exp (list): Part of parsed S-Expression ``(fp_curve ...)``

        Raises:
            - Exception: When given parameter's type is not a list
            - Exception: When the first item of the list is not fp_curve

        Returns:
            - FpCurve: Object of the class initialized with the given S-Expression
        """
        if not isinstance(exp, list):
            raise Exception("Expression does not have the correct type")

        if exp[0] != 'fp_curve':
            raise Exception("Expression does not have the correct type")

        object = cls()
        for item in exp:
            if type(item) != type([]):
                if item == 'locked': object.locked = True
                else: continue

            if item[0] == 'pts':
                for point in item[1:]:
                    object.coordinates.append(Position().from_sexpr(point))
            if item[0] == 'layer': object.layer = item[1]
            if item[0] == 'tstamp': object.tstamp = item[1]
            if item[0] == 'width':
                object.width = item[1]
                object.stroke = None
            if item[0] == 'stroke':
                object.stroke = Stroke.from_sexpr(item)
                object.width = None

        return object

    def to_sexpr(self, indent: int = 2, newline: bool = True) -> str:
        """Generate the S-Expression representing this object. When no coordinates are set
        in the curve, the resulting S-Expression will be left empty.

        Args:
            - indent (int): Number of whitespaces used to indent the output. Defaults to 2.
            - newline (bool): Adds a newline to the end of the output. Defaults to True.

        Returns:
            - str: S-Expression of this object
        """
        indents = ' '*indent
        endline = '\n' if newline else ''
        if len(self.coordinates) == 0:
            return f'{indents}{endline}'

        tstamp = f' (tstamp {self.tstamp})' if self.tstamp is not None else ''
        locked = ' locked' if self.locked else ''

        if self.width is not None:
            width = f' (width {self.width})'
        elif self.stroke is not None:
            width = f' {self.stroke.to_sexpr(indent=0, newline=False)}'
        else:
            width = ''

        expression = f'{indents}(fp_curve (pts\n'
        for point in self.coordinates:
            expression += f'{indents}  (xy {point.X} {point.Y})\n'
        expression += f'{indents}) (layer "{dequote(self.layer)}"){width}{locked}{tstamp}){endline}'
        return expression
