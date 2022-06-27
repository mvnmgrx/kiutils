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
from os import path

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

    elements: list[str] = field(default_factory=list)
    """The `items` token defines a list of zero or more element types to include in this constraint.
    The following element types are available:
    - `buried_via`
    - `micro_via`
    - `via`
    - `graphic`
    - `hole`
    - `pad`
    - `text`
    - `track`
    - `zone`
    """

    @classmethod
    def from_sexpr(cls, exp: str):
        """Convert the given S-Expresstion into a Constraint object

        Args:
            exp (list): Part of parsed S-Expression `(constraint ...)`

        Raises:
            Exception: When given parameter's type is not a list
            Exception: When the list's first parameter is not the `(constraint ..)` token

        Returns:
            Position: Object of the class initialized with the given S-Expression
        """
        if not isinstance(exp, list):
            raise Exception("Expression does not have the correct type")

        if exp[0] != 'constraint':
            raise Exception("Expression does not have the correct type")

        object = cls()
        object.type = exp[1]
        for item in exp[2:]:
            if type(item) != type([]):
                object.elements.append(item)
            if item[0] == 'min': object.min = item[1]
            if item[0] == 'opt': object.opt = item[1]
            if item[0] == 'max': object.max = item[1]
        return object

    def to_sexpr(self, indent=2, newline=True):
        """Generate the S-Expression representing this object

        Args:
            indent (int, optional): Number of whitespaces used to indent the output. Defaults to 2.
            newline (bool, optional): Adds a newline to the end of the output. Defaults to True.

        Returns:
            str: S-Expression of this object
        """
        indents = ' '*indent
        endline = '\n' if newline else ''

        min = f' (min "{dequote(self.min)}")' if self.min is not None else ''
        opt = f' (opt "{dequote(self.opt)}")' if self.opt is not None else ''
        max = f' (max "{dequote(self.max)}")' if self.max is not None else ''

        elements = ' '+' '.join(self.elements) if (len(self.elements) > 0) else ''

        return f'{indents}(constraint {self.type}{min}{opt}{max}{elements}){endline}'

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

    @classmethod
    def from_sexpr(cls, exp: str):
        """Convert the given S-Expresstion into a Rule object

        Args:
            exp (list): Part of parsed S-Expression `(rule ...)`

        Raises:
            Exception: When given parameter's type is not a list
            Exception: When the list's first parameter is not the `(rule ..)` token

        Returns:
            Position: Object of the class initialized with the given S-Expression
        """
        if not isinstance(exp, list):
            raise Exception("Expression does not have the correct type")

        if exp[0] != 'rule':
            raise Exception("Expression does not have the correct type")

        object = cls()
        object.name = exp[1]
        for item in exp[2:]:
            if item[0] == 'constraint': object.constraints.append(Constraint().from_sexpr(item))
            if item[0] == 'condition': object.condition = item[1]
            if item[0] == 'layer': object.layer = item[1]
        return object

    def to_sexpr(self, indent=0):
        """Generate the S-Expression representing this object

        Args:
            indent (int, optional): Number of whitespaces used to indent the output. Defaults to 0.

        Returns:
            str: S-Expression of this object
        """
        indents = ' '*indent

        expression = f'{indents}(rule "{dequote(self.name)}"\n'
        if self.layer is not None:
            expression += f'{indents}  (layer "{dequote(self.layer)}")\n'
        for item in self.constraints:
            expression += f'{indents}{item.to_sexpr(indent+2)}'
        expression += f'{indents}  (condition "{dequote(self.condition)}"))\n'
        return expression

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

    @classmethod
    def from_file(cls, filepath: str):
        """Load a custom design rules set directly from a KiCad design rules file (`.kicad_dru`) and
        sets the `self.filePath` attribute to the given file path.

        Args:
            filepath (str): Path or path-like object that points to the file

        Raises:
            Exception: If the given path is not a file

        Returns:
            Footprint: Object of the DesignRules class initialized with the given KiCad file
        """
        if not path.isfile(filepath):
            raise Exception("Given path is not a file!")

        with open(filepath, 'r') as infile:
            # This dirty fix adds opening and closing brackets `(..)` to the read input to enable
            # the S-Expression parser to work for the DRU-format as well.
            data = f'({infile.read()})'
            item = cls.from_sexpr(sexpr.parse_sexp(data))
            item.filePath = filepath
            return item

    def to_file(self, filepath = None):
        """Save the object to a file in S-Expression format

        Args:
            filepath (str, optional): Path-like string to the file. Defaults to None. If not set, the
            attribute `self.filePath` will be used instead

        Raises:
            Exception: If no file path is given via the argument or via `self.filePath`
        """
        if filepath is None:
            if self.filePath is None:
                raise Exception("File path not set")
            filepath = self.filePath

        with open(filepath, 'w') as outfile:
            outfile.write(self.to_sexpr())

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

        expression = f'(version {self.version})\n\n'

        for rule in self.rules:
            expression += rule.to_sexpr()

        return expression