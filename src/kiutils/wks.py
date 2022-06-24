"""Classes for worksheets (.kicad_wks) and its contents

Author:
    (C) Marvin Mager - @mvnmgrx - 2022

License identifier:
    GPL-3.0

Major changes:
    24.06.2022 - created

Documentation taken from:
    https://dev-docs.kicad.org/en/file-formats/sexpr-worksheet/
"""

from dataclasses import dataclass, field


@dataclass
class WksFontSize():
    """The `WksFontSize` token defines the size of a font in a worksheet"""

    width: float = 1.0
    """The `width` token defines the width of the font"""

    height: float = 1.0
    """The `height` token defines the height of the font"""

    @classmethod
    def from_sexpr(cls, exp: str):
        """Convert the given S-Expresstion into a WksFontSize object

        Args:
            exp (list): Part of parsed S-Expression `(size ...)`

        Raises:
            Exception: When given parameter's type is not a list
            Exception: When the first item of the list is not `size`

        Returns:
            Position: Object of the class initialized with the given S-Expression
        """
        raise NotImplementedError()

    def to_sexpr(self, indent=0, newline=False):
        """Generate the S-Expression representing this object

        Args:
            indent (int, optional): Number of whitespaces used to indent the output. Defaults to 0.
            newline (bool, optional): Adds a newline to the end of the output. Defaults to False.

        Returns:
            str: S-Expression of this object
        """
        raise NotImplementedError()

@dataclass
class WksFont():
    """The `WksFont` token defines how a text is drawn"""

    size: WksFontSize | None = None
    """The optional `size` token defines the size of the font"""

    bold: bool = False
    """The `bold` token defines if the font is drawn bold"""

    italic: bool = False
    """The `italic` token defines if the font is drawn italic"""

    @classmethod
    def from_sexpr(cls, exp: str):
        """Convert the given S-Expresstion into a WksFont object

        Args:
            exp (list): Part of parsed S-Expression `(font ...)`

        Raises:
            Exception: When given parameter's type is not a list
            Exception: When the first item of the list is not `font`

        Returns:
            Position: Object of the class initialized with the given S-Expression
        """
        raise NotImplementedError()

    def to_sexpr(self, indent=0, newline=False):
        """Generate the S-Expression representing this object

        Args:
            indent (int, optional): Number of whitespaces used to indent the output. Defaults to 0.
            newline (bool, optional): Adds a newline to the end of the output. Defaults to False.

        Returns:
            str: S-Expression of this object
        """
        raise NotImplementedError()

@dataclass
class WksPosition():
    """The `WksPosition` token defines the positional coordinates and rotation of an worksheet
    object.
    """

    X: float = 0.0
    """The `X` attribute defines the horizontal position of the object"""

    Y: float = 0.0
    """The `Y` attribute defines the vertical position of the object"""

    corner: str | None = None
    """The optional `corner` token is used to define the initial corner for repeating"""

    @classmethod
    def from_sexpr(cls, exp: str):
        """Convert the given S-Expresstion into a WksPosition object

        Args:
            exp (list): Part of parsed S-Expression `(xxx ...)`

        Raises:
            Exception: When the given expression is not of type `list` or the list is less than
            3 items long

        Returns:
            Position: Object of the class initialized with the given S-Expression
        """
        if not isinstance(exp, list) or len(exp) < 3:
            raise Exception("Expression does not have the correct type")

        object = cls()
        object.X = exp[1]
        object.Y = exp[2]

        if len(exp) >= 3:
            object.corner = exp[3]

        return object

    def to_sexpr():
        """This object does not have a direct S-Expression representation.
        """
        raise NotImplementedError()

@dataclass
class Line():
    """The `Line` token defines how a line is drawn in a work sheet
    
    Documentation:
        https://dev-docs.kicad.org/en/file-formats/sexpr-worksheet/#_graphical_line"""

    name: str = ""
    """The `name` token defines the name of the line object"""

    start: WksPosition = WksPosition()
    """The `start` token defines the start position of the line"""

    end: WksPosition = WksPosition()
    """The `end` token defines the end position of the line"""

    repeat: int | None = None
    """The optional `repeat` token defines the count for repeated incremental lines"""

    incrx: float | None = None
    """The optional `incrx` token defines the repeat distance on the X axis"""

    incry: float | None = None
    """The optional `incry` token defines the repeat distance on the Y axis"""

    comment: str | None = None
    """The optional `comment` token is a comment for the line object"""

    @classmethod
    def from_sexpr(cls, exp: str):
        """Convert the given S-Expresstion into a TbText object

        Args:
            exp (list): Part of parsed S-Expression `(tbtext ...)`

        Raises:
            Exception: When given parameter's type is not a list
            Exception: When the first item of the list is not `tbtext`

        Returns:
            Position: Object of the class initialized with the given S-Expression
        """
        raise NotImplementedError()

    def to_sexpr(self, indent=0, newline=False):
        """Generate the S-Expression representing this object

        Args:
            indent (int, optional): Number of whitespaces used to indent the output. Defaults to 0.
            newline (bool, optional): Adds a newline to the end of the output. Defaults to False.

        Returns:
            str: S-Expression of this object
        """
        raise NotImplementedError()

@dataclass
class Rect():
    """The `Rect` token defines how a rectangle is drawn in a work sheet
    
    Documentation:
        https://dev-docs.kicad.org/en/file-formats/sexpr-worksheet/#_graphical_rectangle"""

    name: str = ""
    """The `name` token defines the name of the rectangle object"""

    start: WksPosition = WksPosition()
    """The `start` token defines the start position of the rectangle"""

    end: WksPosition = WksPosition()
    """The `end` token defines the end position of the rectangle"""

    repeat: int | None = None
    """The optional `repeat` token defines the count for repeated incremental rectangles"""

    incrx: float | None = None
    """The optional `incrx` token defines the repeat distance on the X axis"""

    incry: float | None = None
    """The optional `incry` token defines the repeat distance on the Y axis"""

    comment: str | None = None
    """The optional `comment` token is a comment for the rectangle object"""

    @classmethod
    def from_sexpr(cls, exp: str):
        """Convert the given S-Expresstion into a TbText object

        Args:
            exp (list): Part of parsed S-Expression `(tbtext ...)`

        Raises:
            Exception: When given parameter's type is not a list
            Exception: When the first item of the list is not `tbtext`

        Returns:
            Position: Object of the class initialized with the given S-Expression
        """
        raise NotImplementedError()

    def to_sexpr(self, indent=0, newline=False):
        """Generate the S-Expression representing this object

        Args:
            indent (int, optional): Number of whitespaces used to indent the output. Defaults to 0.
            newline (bool, optional): Adds a newline to the end of the output. Defaults to False.

        Returns:
            str: S-Expression of this object
        """
        raise NotImplementedError()

@dataclass
class Polygon():
    """The `Polygon` token defines a graphical polygon in a worksheet
    
    Documentation:
        https://dev-docs.kicad.org/en/file-formats/sexpr-worksheet/#_graphical_polygon
    """

    name: str = ""
    """The `name` token defines the name of the polygon"""

    position: WksPosition = WksPosition()
    """The `position` token defines the coordinates of the polygon"""

    rotate: float | None = None
    """The optional `rotate` token defines the rotation angle of the polygon object"""

    coordinates: list[WksPosition] = field(default_factory=list)
    """The `coordinates` token defines a list of X/Y coordinates that forms the polygon"""

    repeat: int | None = None
    """The optional `repeat` token defines the count for repeated incremental polygons"""

    incrx: float | None = None
    """The optional `incrx` token defines the repeat distance on the X axis"""

    incry: float | None = None
    """The optional `incry` token defines the repeat distance on the Y axis"""

    comment: str | None = None
    """The optional `comment` token is a comment for the polygon object"""

    @classmethod
    def from_sexpr(cls, exp: str):
        """Convert the given S-Expresstion into a Polygon object

        Args:
            exp (list): Part of parsed S-Expression `(polygon ...)`

        Raises:
            Exception: When given parameter's type is not a list
            Exception: When the first item of the list is not `polygon`

        Returns:
            Position: Object of the class initialized with the given S-Expression
        """
        raise NotImplementedError()

    def to_sexpr(self, indent=0, newline=False):
        """Generate the S-Expression representing this object

        Args:
            indent (int, optional): Number of whitespaces used to indent the output. Defaults to 0.
            newline (bool, optional): Adds a newline to the end of the output. Defaults to False.

        Returns:
            str: S-Expression of this object
        """
        raise NotImplementedError()

@dataclass
class Bitmap():
    """The `Polygon` token defines on or more embedded images
    
    Documentation:
        https://dev-docs.kicad.org/en/file-formats/sexpr-worksheet/#_image
    """

    name: str = ""
    """The `name` token defines the name of the bitmap"""

    position: WksPosition = WksPosition()
    """The `position` token defines the coordinates of the bitmap"""

    scale: float = 1.0
    """The `scale` token defines the scale of the bitmap object"""

    repeat: int | None = None
    """The optional `repeat` token defines the count for repeated incremental bitmaps"""

    incrx: float | None = None
    """The optional `incrx` token defines the repeat distance on the X axis"""

    incry: float | None = None
    """The optional `incry` token defines the repeat distance on the Y axis"""

    comment: str | None = None
    """The optional `comment` token is a comment for the bitmap object"""

    # TODO: Parse this nonesense as a binary struct to make it more useful
    pngdata: list[str] = field(default_factory=list)
    """The `pngdata` token defines a list of strings representing up to 32 bytes per entry of 
    the image being saved. 
    
    Format: 
    - "xx xx xx xx xx (..) xx "

    The list must be 32byte aligned, leaving a space after the last byte as shown in the format
    example.
    """

    @classmethod
    def from_sexpr(cls, exp: str):
        """Convert the given S-Expresstion into a Bitmap object

        Args:
            exp (list): Part of parsed S-Expression `(bitmap ...)`

        Raises:
            Exception: When given parameter's type is not a list
            Exception: When the first item of the list is not `bitmap`

        Returns:
            Position: Object of the class initialized with the given S-Expression
        """
        raise NotImplementedError()

    def to_sexpr(self, indent=0, newline=False):
        """Generate the S-Expression representing this object

        Args:
            indent (int, optional): Number of whitespaces used to indent the output. Defaults to 0.
            newline (bool, optional): Adds a newline to the end of the output. Defaults to False.

        Returns:
            str: S-Expression of this object
        """
        raise NotImplementedError()


@dataclass
class TbText():
    """The `TbText` token define text used in the title block of a work sheet
    
    Documentation:
        https://dev-docs.kicad.org/en/file-formats/sexpr-worksheet/#_title_block_text"""

    text: str = ""
    """The `text` token defines the text itself"""

    name: str = ""
    """The `name` token defines the name of the text object"""

    position: WksPosition = WksPosition()
    """The `position` token defines the position of the text"""

    font: WksFont = WksFont()
    """The `font` token define how the text is drawn"""

    repeat: int | None = None
    """The optional `repeat` token defines the count for repeated incremental text"""

    incrx: float | None = None
    """The optional `incrx` token defines the repeat distance on the X axis"""

    incry: float | None = None
    """The optional `incry` token defines the repeat distance on the Y axis"""

    comment: str | None = None
    """The optional `comment` token is a comment for the text object"""

    @classmethod
    def from_sexpr(cls, exp: str):
        """Convert the given S-Expresstion into a TbText object

        Args:
            exp (list): Part of parsed S-Expression `(tbtext ...)`

        Raises:
            Exception: When given parameter's type is not a list
            Exception: When the first item of the list is not `tbtext`

        Returns:
            Position: Object of the class initialized with the given S-Expression
        """
        raise NotImplementedError()

    def to_sexpr(self, indent=0, newline=False):
        """Generate the S-Expression representing this object

        Args:
            indent (int, optional): Number of whitespaces used to indent the output. Defaults to 0.
            newline (bool, optional): Adds a newline to the end of the output. Defaults to False.

        Returns:
            str: S-Expression of this object
        """
        raise NotImplementedError()


@dataclass
class TextSize():
    """The `TextSize` define the default width and height of text"""

    width: float = 1.5
    """The `width` token defines the default width of a text element"""

    height: float = 1.5
    """The `height` token defines the default height of a text element"""

    @classmethod
    def from_sexpr(cls, exp: str):
        """Convert the given S-Expresstion into a TextSize object

        Args:
            exp (list): Part of parsed S-Expression `(textsize ...)`

        Raises:
            Exception: When given parameter's type is not a list
            Exception: When the first item of the list is not `textsize`

        Returns:
            Position: Object of the class initialized with the given S-Expression
        """
        raise NotImplementedError()

    def to_sexpr(self, indent=0, newline=False):
        """Generate the S-Expression representing this object

        Args:
            indent (int, optional): Number of whitespaces used to indent the output. Defaults to 0.
            newline (bool, optional): Adds a newline to the end of the output. Defaults to False.

        Returns:
            str: S-Expression of this object
        """
        raise NotImplementedError()

@dataclass
class Setup():
    """The `setup` token defines the configuration information for the work sheet
    
    Documentation:
        https://dev-docs.kicad.org/en/file-formats/sexpr-worksheet/#_set_up_section"""

    textSize: TextSize = TextSize()
    """The `textSize` token defines the default width and height of text"""

    lineWidth: float = 0.15
    """The `lineWidth` token attribute defines the default width of lines"""

    textLineWidth: float = 10.0
    """The `textLineWidth` token attribute define the default width of the lines used to draw text"""

    leftMargin: float = 10.0
    """The `leftMargin` token defines the distance from the left edge of the page"""

    rightMargin: float = 10.0
    """The `rightMargin` token defines the distance from the right edge of the page"""

    topMargin: float = 10.0
    """The `topMargin` token defines the distance from the top edge of the page"""

    bottomMargin: float = 10.0
    """The `bottomMargin` token defines the distance from the bottom edge of the page"""

    @classmethod
    def from_sexpr(cls, exp: str):
        """Convert the given S-Expresstion into a Setup object

        Args:
            exp (list): Part of parsed S-Expression `(setup ...)`

        Raises:
            Exception: When given parameter's type is not a list
            Exception: When the first item of the list is not `setup`

        Returns:
            Position: Object of the class initialized with the given S-Expression
        """
        raise NotImplementedError()

    def to_sexpr(self, indent=0, newline=False):
        """Generate the S-Expression representing this object

        Args:
            indent (int, optional): Number of whitespaces used to indent the output. Defaults to 0.
            newline (bool, optional): Adds a newline to the end of the output. Defaults to False.

        Returns:
            str: S-Expression of this object
        """
        raise NotImplementedError()

@dataclass
class Worksheet():
    """The `Worksheet` token defines a KiCad worksheet (.kicad_wks file)
    
    Documentation:
        https://dev-docs.kicad.org/en/file-formats/sexpr-worksheet/#_header_section"""
    
    version: str = "20210606"
    """The `version` token defines the work sheet version using the YYYYMMDD date format"""

    generator: str = "kiutils"
    """The `generator` token defines the program used to write the file"""

    setup: Setup = Setup()
    """The `setup` token defines the configuration information for the work sheet"""

    drawingObjects: list = field(default_factory=list)
    """The `drawingObjects` token can contain zero or more texts, lines, rectangles, polys or images"""

    @classmethod
    def from_sexpr(cls, exp: str):
        """Convert the given S-Expresstion into a Worksheet object

        Args:
            exp (list): Part of parsed S-Expression `(kicad_wks ...)`

        Raises:
            Exception: When given parameter's type is not a list
            Exception: When the first item of the list is not `kicad_wks`

        Returns:
            Position: Object of the class initialized with the given S-Expression
        """
        raise NotImplementedError()

    def to_sexpr(self, indent=0, newline=False):
        """Generate the S-Expression representing this object

        Args:
            indent (int, optional): Number of whitespaces used to indent the output. Defaults to 0.
            newline (bool, optional): Adds a newline to the end of the output. Defaults to False.

        Returns:
            str: S-Expression of this object
        """
        raise NotImplementedError()