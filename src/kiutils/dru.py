"""Classes for custom design rules (.kicad_dru) and its contents

Author:
    (C) Marvin Mager - @mvnmgrx - 2022

License identifier:
    GPL-3.0

Major changes:
    26.06.2022 - created

Documentation taken from:
    ??? Syntax help in Pcbnew
"""

from dataclasses import dataclass, field

from .utils import sexpr
from .utils.strings import dequote

@dataclass
class Constraint():
    pass

@dataclass
class Rule():
    pass

@dataclass
class DesignRules():
    """The `DesignRules` token defines a set of custom design rules (`.kicad_dru` files)"""

    version: int = 1
    """The `version` token defines the version of the file for the KiCad parser. Defaults to 1."""

    rules: list[Rule] = field(default_factory=list)
    """The `rules` token defines a list of custom design rules"""

    @classmethod
    def from_sexpr(cls, exp: str):
        """Convert the given S-Expresstion into a DesignRules object

        Args:
            exp (list): Part of parsed S-Expression `(version ...)`

        Raises:
            Exception: When given parameter's type is not a list
            Exception: When the list's first parameter is not the `(version ..)` token

        Returns:
            Position: Object of the class initialized with the given S-Expression
        """
        if not isinstance(exp, list):
            raise Exception("Expression does not have the correct type")

        if not isinstance(exp[0], list):
            raise Exception("Expression does not have the correct type")

        if exp[0][0] != 'version':
            raise Exception("Expression does not have the correct type")

        object = cls()
        for item in exp:
            if item[0] == 'version': object.version = item[0]
            if item[0] == 'rule': object.rules.append(Rule().from_sexpr(item))
        return object

    def to_sexpr(self, indent=0, newline=False):
        """Generate the S-Expression representing this object

        Args:
            indent (int, optional): Number of whitespaces used to indent the output. Defaults to 0.
            newline (bool, optional): Adds a newline to the end of the output. Defaults to False.

        Returns:
            str: S-Expression of this object
        """
        indents = ' '*indent
        endline = '\n' if newline else ''
        return f'{indents}(size {self.width} {self.height}){endline}'