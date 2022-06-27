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
    """The `Constraint` token defines a design rule's constraint"""

    type: str = "clearance"
    """The `type` token defines the type of constraint. Defaults to `clearance`. Allowed types:
    - `annular_width` - Width of an annular ring
    - `clearance` - Clearance between two items
    - `courtyard_clearance` - Clearance between two courtyards
    - `diff_pair_gap` - Gap between differential pairs
    - `diff_pair_uncoupled` - ???
    - `disallow` - ??? Do not allow this rule
    - `edge_clearance` - Clearance between the item and board edges
    - `length` - Length of the item
    - `hole_clearance` - Clearance between the item and holes
    - `hole_size` - Size of the holes associated with this item
    - `silk_clearance` - Clearance to silk screen
    - `skew` - Difference in length between the items associated with this constraint
    - `track_width` - Width of the tracks associated with this constraint
    - `via_count` - Number of vias
    - `via_diameter` - Diameter of vias associated with this constraint
    """

    min: str | None = None
    """The `min` token defines the minimum allowed in this constraint"""

    opt: str | None = None
    """The `opt` token defines the optimum allowed in this constraint"""

    max: str | None = None
    """The `max` token defines the maximum allowed in this constraint"""

@dataclass
class Rule():
    """The `Rule` token defines a custom design rule"""

    name: str = ""
    """The `name` token defines the name of the custom design rule"""

    constraints: list[Constraint] = field(default_factory=list)
    """The `constraints` token defines a list of constraints for this custom design rule"""

    condition: str = ""
    """The `condition` token defines the conditions that apply for this rule. Check KiCad syntax
    reference for more information. Example rule:
    - `A.inDiffPair('*') && !AB.isCoupledDiffPair()`"""

    layer: str | None = None
    """The optional `layer` token defines the canonical layer the rule applys to"""

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