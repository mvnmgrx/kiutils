"""Classes to manage KiCad board items

Author:
    (C) Marvin Mager - @mvnmgrx - 2022

License identifier:
    GPL-3.0

Major changes:
    20.02.2022 - created

Documentation taken from:
    https://dev-docs.kicad.org/en/file-formats/sexpr-pcb/
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, List

from kiutils.items.common import Position
from kiutils.utils.strings import dequote

@dataclass
class GeneralSettings():
    """The ``general`` token define general information about the board

    Documentation:
        https://dev-docs.kicad.org/en/file-formats/sexpr-pcb/#_general_section
    """

    thickness: float = 1.6
    """The ``thickness`` token attribute defines the overall board thickness"""

    @classmethod
    def from_sexpr(cls, exp: list) -> GeneralSettings:
        """Convert the given S-Expresstion into a GeneralSettings object

        Args:
            - exp (list): Part of parsed S-Expression ``(general ...)``

        Raises:
            - Exception: When given parameter's type is not a list
            - Exception: When the first item of the list is not general

        Returns:
            - GeneralSettings: Object of the class initialized with the given S-Expression
        """
        if not isinstance(exp, list):
            raise Exception("Expression does not have the correct type")

        if exp[0] != 'general':
            raise Exception("Expression does not have the correct type")

        object = cls()
        for item in exp:
            if item[0] == 'thickness': object.thickness = item[1]
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

        expression =  f'{indents}(general\n'
        expression += f'{indents}  (thickness {self.thickness})\n'
        expression += f'{indents}){endline}'
        return expression


@dataclass
class LayerToken():
    """Intermediate type used for the ``layers`` token in a board

    Documentation:
        https://dev-docs.kicad.org/en/file-formats/sexpr-pcb/#_layers_section
    """

    ordinal: int = 0
    """The layer ``ordinal`` is an integer used to associate the layer stack ordering. This is mostly
    to ensure correct mapping when the number of layers is increased in the future"""

    name: str = "F.Cu"
    """The ``name`` is the layer name defined for internal board use"""

    type: str = "signal"
    """The layer ``type`` defines the type of layer and can be defined as ``jumper``, ``mixed``, ``power``,
    ``signal``, or ``user``."""

    userName: Optional[str] = None
    """The optional ``userName`` attribute defines the custom user name"""

    @classmethod
    def from_sexpr(cls, exp: list) -> LayerToken:
        """Convert the given S-Expresstion into a LayerToken object

        Args:
            - exp (list): Part of parsed S-Expression ``(<nr> "<name>" <type>)``

        Raises:
            - Exception: When given parameter's type is not a list or the length of the list is not 3 - 4
            - Exception: When the first item of the list is not kicad_pcb

        Returns:
            - LayerToken: Object of the class initialized with the given S-Expression
        """
        if not isinstance(exp, list) or len(exp) < 3 or len(exp) > 4:
            raise Exception("Expression does not have the correct type")

        object = cls()
        object.ordinal = exp[0]
        object.name = exp[1]
        object.type = exp[2]
        if len(exp) == 4:
            object.userName = exp[3]
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

        username = f' "{dequote(self.userName)}"' if self.userName is not None else ''

        return f'{indents}({self.ordinal} "{dequote(self.name)}" {self.type}{username}){endline}'


@dataclass
class StackupSubLayer():
    """The ``StackupSubLayer`` token defines a sublayer used when stacking dielectrics in a PCB"""

    thickness: float = 0.1
    """The ``thickness`` token defines the thickness of the sublayer. Defaults to 0.1"""

    material: Optional[str] = None
    """The optional ``material`` token defines a string that describes the sublayer material"""

    epsilonR: Optional[float] = None
    """The optional ``epsilonR`` token defines the dielectric constant of the sublayer material"""

    lossTangent: Optional[float] = None
    """The optional layer ``lossTangent`` token defines the dielectric loss tangent of the sublayer"""

    @classmethod
    def from_sexpr(cls, exp: list) -> StackupSubLayer:
        """This class cannot be derived from an S-Expression as the format currently used in KiCad
        board files does not match the usual convention. Assign member values manually when using
        this object.

        Raises:
            - NotImplementedError"""
        raise NotImplementedError("This class cannot be derived from an S-Expression!")

    def to_sexpr(self, indent=0, newline=False) -> str:
        """Generate the S-Expression representing this object. The representation differs from the
        normal form of an S-Expression as this uses no opening and closing parenthesis.

        Args:
            - indent (int): Number of whitespaces used to indent the output. Defaults to 0.
            - newline (bool): Adds a newline to the end of the output. Defaults to False.

        Returns:
            - str: S-Expression of this object
        """
        indents = ' '*indent
        endline = '\n' if newline else ''

        mat = f' (material "{dequote(self.material)}")' if self.material is not None else ''
        er = f' (epsilon_r {self.epsilonR})' if self.epsilonR is not None else ''
        lt = f' (loss_tangent {self.lossTangent})' if self.lossTangent is not None else ''

        return f'{indents}addsublayer (thickness {self.thickness}){mat}{er}{lt}{endline}'


@dataclass
class StackupLayer():
    """The ``layer`` token defines the stack up setting of a single layer in the board stack up
    settings.

    Documentation:
        https://dev-docs.kicad.org/en/file-formats/sexpr-pcb/#_stack_up_settings
    """

    name: str = ""
    """The ``name`` attribute is either one of the canonical copper or technical layer names
    or ``dielectric ID`` if it is dielectric layer"""

    # Not found in example project ...
    #number: int = 0
    """The ``number`` attribute defines the stack order of the layer"""

    type: str = ""
    """The ``type`` token defines a string that describes the layer"""

    color: Optional[str] = None
    """The optional ``color`` token defines a string that describes the layer color. This is
    only used on solder mask and silkscreen layers"""

    thickness: Optional[float] = None
    """The optional ``thickness`` token defines the thickness of the layer where appropriate"""

    material: Optional[str] = None
    """The optional ``material`` token defines a string that describes the layer material
    where appropriate"""

    epsilonR: Optional[float] = None
    """The optional ``epsilonR`` token defines the dielectric constant of the layer material"""

    lossTangent: Optional[float] = None
    """The optional layer ``lossTangent`` token defines the dielectric loss tangent of the layer"""

    subLayers: List[StackupSubLayer] = field(default_factory=list)
    """The ``sublayers`` token defines a list of zero or more sublayers that are used to create
    stacks of dielectric layers. Does not apply to copper-type layers."""

    @classmethod
    def from_sexpr(cls, exp: list) -> StackupLayer:
        """Convert the given S-Expresstion into a StackupLayer object

        Args:
            - exp (list): Part of parsed S-Expression ``(layer ...)``

        Raises:
            - Exception: When given parameter's type is not a list
            - Exception: When the first item of the list is not layer

        Returns:
            - StackupLayer: Object of the class initialized with the given S-Expression
        """
        if not isinstance(exp, list):
            raise Exception("Expression does not have the correct type")

        if exp[0] != 'layer':
            raise Exception("Expression does not have the correct type")

        parsingSublayer = False
        tempSublayer = StackupSubLayer()
        object = cls()
        object.name = exp[1]
        for item in exp[2:]:
            if type(item) != type([]):
                # Start parsing the layer's sublayer if the first sublayer token was found
                if item == 'addsublayer':
                    if parsingSublayer:
                        # When the ``addsublayer`` token was found a second time, the previously
                        # parsed sublayer will be appended to the list of sublayers
                        object.subLayers.append(tempSublayer)
                        tempSublayer = StackupSubLayer()
                    else:
                        # Change state of the parser to look for StackupSubLayer tokens
                        parsingSublayer = True
                continue

            # Parse the tokens of StackupSubLayer for the current sublayer
            if parsingSublayer:
                if item[0] == 'thickness': tempSublayer.thickness = item[1]
                if item[0] == 'material': tempSublayer.material = item[1]
                if item[0] == 'epsilon_r': tempSublayer.epsilonR = item[1]
                if item[0] == 'loss_tangent': tempSublayer.lossTangent = item[1]
                continue

            # Parse the normal tokens of StackupLayer token
            if item[0] == 'type': object.type = item[1]
            if item[0] == 'thickness': object.thickness = item[1]
            if item[0] == 'material': object.material = item[1]
            if item[0] == 'epsilon_r': object.epsilonR = item[1]
            if item[0] == 'loss_tangent': object.lossTangent = item[1]
            if item[0] == 'color': object.color = item[1]

        # Add the last parsed sublayer to the list, if any
        if parsingSublayer:
            object.subLayers.append(tempSublayer)

        return object

    def to_sexpr(self, indent=6, newline=True) -> str:
        """Generate the S-Expression representing this object

        Args:
            - indent (int): Number of whitespaces used to indent the output. Defaults to 6.
            - newline (bool): Adds a newline to the end of the output. Defaults to True.

        Returns:
            - str: S-Expression of this object
        """
        indents = ' '*indent
        endline = '\n' if newline else ''

        color = f' (color "{dequote(self.color)}")' if self.color is not None else ''
        material = f' (material "{dequote(self.material)}")' if self.material is not None else ''
        thickness = f' (thickness {self.thickness})' if self.thickness is not None else ''
        epsilon_r = f' (epsilon_r {self.epsilonR})' if self.epsilonR is not None else ''
        loss_tangent = f' (loss_tangent {self.lossTangent})' if self.lossTangent is not None else ''

        expression = f'{indents}(layer "{dequote(self.name)}" (type "{self.type}"){color}{thickness}'
        expression +=f'{material}{epsilon_r}{loss_tangent}'
        for layer in self.subLayers:
            expression += f'\n{layer.to_sexpr(indent+2)}'
        expression += f'){endline}'
        return expression

@dataclass
class Stackup():
    """The ``stackup`` token defines the board stack up settings and is defined in the setup
    section.

    Documentation:
        https://dev-docs.kicad.org/en/file-formats/sexpr-pcb/#_stack_up_settings
    """

    layers: List[StackupLayer] = field(default_factory=list)
    """The ``layers``token is a list of layer settings for each layer required to manufacture
    a board including the dielectric material between the actual layers defined in the board
    editor."""

    copperFinish: Optional[str] = None
    """The optional ``copperFinish`` token is a string that defines the copper finish used to
    manufacture the board"""

    dielectricContraints: Optional[str] = None
    """The optional ``dielectricContraints`` token define if the board should meet all
    dielectric requirements. Valid values are ``yes`` and ``no``."""

    edgeConnector: Optional[str] = None
    """The optional ``edgeConnector`` token defines if the board has an edge connector
    (value: ``yes``) and if the edge connector is bevelled (value: ``bevelled``)"""

    castellatedPads: bool = False
    """The ``castellatedPads`` token defines if the board edges contain castellated pads"""

    edgePlating: bool = False
    """The ``edgePlating`` token defines if the board edges should be plated."""

    @classmethod
    def from_sexpr(cls, exp: list) -> Stackup:
        """Convert the given S-Expresstion into a Stackup object

        Args:
            - exp (list): Part of parsed S-Expression ``(stackup ...)``

        Raises:
            - Exception: When given parameter's type is not a list
            - Exception: When the first item of the list is not stackup

        Returns:
            - Stackup: Object of the class initialized with the given S-Expression
        """
        if not isinstance(exp, list):
            raise Exception("Expression does not have the correct type")

        if exp[0] != 'stackup':
            raise Exception("Expression does not have the correct type")

        object = cls()
        for item in exp:
            if item[0] == 'layer': object.layers.append(StackupLayer().from_sexpr(item))
            if item[0] == 'copper_finish': object.copperFinish = item[1]
            if item[0] == 'dielectric_constraints': object.dielectricContraints = item[1]
            if item[0] == 'edge_connector': object.edgeConnector = item[1]
            if item[0] == 'castellated_pads': object.castellatedPads = True
            if item[0] == 'edge_plating': object.edgePlating = True
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

        expression =  f'{indents}(stackup\n'
        for layer in self.layers:
            expression += layer.to_sexpr(indent+2)
        if self.copperFinish is not None:         expression += f'{indents}  (copper_finish "{dequote(self.copperFinish)}")\n'
        if self.dielectricContraints is not None: expression += f'{indents}  (dielectric_constraints {self.dielectricContraints})\n'
        if self.edgeConnector is not None:        expression += f'{indents}  (edge_connector {self.edgeConnector})\n'
        if self.castellatedPads:                  expression += f'{indents}  (castellated_pads yes)\n'
        if self.edgePlating:                      expression += f'{indents}  (edge_plating yes)\n'
        expression += f'{indents}){endline}'
        return expression

@dataclass
class PlotSettings():
    """The ``pcbplotparams`` token defines the plotting and printing settings used for the last
    plot and is defined in the set up section.

    Documentation:
        https://dev-docs.kicad.org/en/file-formats/sexpr-pcb/#_plot_settings
    """

    layerSelection: str = ""
    """The ``layerSelection`` token defines a hexadecimal bit set of the layers to plot"""

    plotOnAllLayersSelection: Optional[str] = None
    """The ``plotOnAllLayersSelection`` token defines a hexadecimal bit set of layers where all 
    selected layers shall be plotted.
    
    Available and required since KiCad v7"""

    disableApertMacros: bool = False
    """The ``disableApertMacros`` token defines if aperture macros are to be used in gerber plots"""

    useGerberExtensions: bool = False
    """The ``useGerberExtensions`` token  defines if the Protel layer file name extensions are to
    be used in gerber plots"""

    useGerberAttributes: bool = False
    """The ``useGerberAttributes`` token defines if the X2 extensions are used in gerber plots"""

    useGerberAdvancedAttributes: bool = False
    """The ``useGerberAdvancedAttributes`` token defines if the netlist information should be
    included in gerber plots"""

    createGerberJobFile: bool = False
    """The ``createGerberJobFile`` token defines if a job file should be created when plotting 
    gerber files"""

    # FIXME: Where is the docu of this token?
    dashedLineDashRatio: Optional[float] = None
    """The ``dashedLineDashRatio`` token's documentation is still missing ..
    
    Available and required since KiCad v7"""

    # FIXME: Where is the docu of this token?
    dashedLineGapRatio: Optional[float] = None
    """The ``dashedLineGapRatio`` token's documentation is still missing ..
    
    Available and required since KiCad v7"""

    svgUseInch: Optional[bool] = None
    """The ``svgUseInch`` token defines if inch units should be use when plotting SVG files.
    
    Required until KiCad v6, removed since KiCad v7"""

    svgPrecision: float = 0.0
    """The ``svgPrecision`` token defines the units precision used when plotting SVG files"""

    excludeEdgeLayer: Optional[bool] = None
    """The ``excludeEdgeLayer`` token defines if the board edge layer is plotted on all layers.
    
    Required until KiCad v6, removed since KiCad v7"""

    plotFameRef: bool = False
    """The ``plotFameRef`` token defines if the border and title block should be plotted"""

    viasOnMask: bool = False
    """The ``viasOnMask`` token defines if the vias are to be tented"""

    mode: int = 1
    """The ``mode`` token defines the plot mode. An attribute of 1 plots in the normal
    mode and an attribute of 2 plots in the outline (sketch) mode."""

    useAuxOrigin: bool = False
    """The ``useAuxOrigin`` token determines if all coordinates are offset by the defined user origin"""

    hpglPenNumber: int = 0
    """The ``hpglPenNumber`` token defines the integer pen number used for HPGL plots"""

    hpglPenSpeed: int = 0
    """The ``hpglPenSpeed`` token defines the integer pen speed used for HPGL plots"""

    hpglPenDiameter: float = 0.0
    """The ``hpglPenDiameter`` token defines the floating point pen size for HPGL plots"""

    dxfPolygonMode: bool = False
    """The ``dxfPolygonMode`` token defines if the polygon mode should be used for DXF plots"""

    dxfImperialUnits: bool = False
    """The ``dxfImperialUnits`` token defines if imperial units should be used for DXF plots"""

    dxfUsePcbnewFont: bool = False
    """The ``dxfUsePcbnewFont`` token defines if the Pcbnew font (vector font) or the default
    font should be used for DXF plots"""

    psNegative: bool = False
    """The ``psNegative`` token defines if the output should be the negative for PostScript plots"""

    psA4Output: bool = False
    """The ``psA4Output`` token defines if the A4 page size should be used for PostScript plots"""

    plotReference: bool = False
    """The ``plotReference`` token defines if hidden reference field text should be plotted"""

    plotValue: bool = False
    """The ``plotValue`` token defines if hidden value field text should be plotted"""

    plotInvisibleText: bool = False
    """The ``plotInvisibleText`` token defines if hidden text other than the reference and
    value fields should be plotted"""

    sketchPadsOnFab: bool = False
    """The ``sketchPadsOnFab`` token defines if pads should be plotted in the outline (sketch) mode"""

    subtractMaskFromSilk: bool = False
    """The ``subtractMaskFromSilk`` token defines if the solder mask layers should be subtracted from
    the silk screen layers for gerber plots"""

    outputFormat: int = 0
    """The ``outputFormat`` token defines the last plot type. The following values are defined:
    - 0: gerber
    - 1: PostScript
    - 2: SVG
    - 3: DXF
    - 4: HPGL
    - 5: PDF"""

    mirror: bool = False
    """The ``mirror`` token defines if the plot should be mirrored"""

    drillShape: int = 0
    """The ``drillShape`` token defines the type of drill marks used for drill files"""

    scaleSelection: int = 1
    """The ``scaleSelection`` is not documented yet (as of 20.02.2022)"""

    outputDirectory: str = ""
    """The ``drillShape`` token defines the path relative to the current project path
    where the plot files will be saved"""

    pdfFrontFpPropertyPopups: Optional[bool] = None
    """The ``pdf_front_fp_property_popups`` token defines if front footprint property popups
    are shown in PDF plots. Available since KiCad v8"""

    pdfBackFpPropertyPopups: Optional[bool] = None
    """The ``pdf_back_fp_property_popups`` token defines if back footprint property popups
    are shown in PDF plots. Available since KiCad v8"""

    pdfMetadata: Optional[bool] = None
    """The ``pdf_metadata`` token defines if metadata is included in PDF plots.
    Available since KiCad v8"""

    pdfSingleDocument: Optional[bool] = None
    """The ``pdf_single_document`` token defines if PDF plots are in a single document.
    Available since KiCad v8"""

    plotBlackAndWhite: Optional[bool] = None
    """The ``plot_black_and_white`` token defines if plots are in black and white.
    Available since KiCad v8"""

    plotPadNumbers: Optional[bool] = None
    """The ``plotpadnumbers`` token defines if pad numbers are plotted.
    Available since KiCad v8"""

    hideDnpOnFab: Optional[bool] = None
    """The ``hidednponfab`` token defines if DNP markers are hidden on fab layers.
    Available since KiCad v8"""

    sketchDnpOnFab: Optional[bool] = None
    """The ``sketchdnponfab`` token defines if DNP markers are sketched on fab layers.
    Available since KiCad v8"""

    crossoutDnpOnFab: Optional[bool] = None
    """The ``crossoutdnponfab`` token defines if DNP markers are crossed out on fab layers.
    Available since KiCad v8"""

    @classmethod
    def from_sexpr(cls, exp: list) -> PlotSettings:
        """Convert the given S-Expresstion into a PlotSettings object

        Args:
            - exp (list): Part of parsed S-Expression ``(pcbplotparams ...)``

        Raises:
            - Exception: When given parameter's type is not a list
            - Exception: When the first item of the list is not pcbplotparams

        Returns:
            - PlotSettings: Object of the class initialized with the given S-Expression
        """
        if not isinstance(exp, list):
            raise Exception("Expression does not have the correct type")

        if exp[0] != 'pcbplotparams':
            raise Exception("Expression does not have the correct type")

        object = cls()
        _b = lambda v: v in ('true', 'yes')
        for item in exp:
            if item[0] == 'layerselection': object.layerSelection = item[1]
            if item[0] == 'plot_on_all_layers_selection': object.plotOnAllLayersSelection = item[1]
            if item[0] == 'disableapertmacros': object.disableApertMacros = _b(item[1])
            if item[0] == 'usegerberextensions' : object.useGerberExtensions = _b(item[1])
            if item[0] == 'usegerberattributes' : object.useGerberAttributes = _b(item[1])
            if item[0] == 'usegerberadvancedattributes' : object.useGerberAdvancedAttributes = _b(item[1])
            if item[0] == 'creategerberjobfile' : object.createGerberJobFile = _b(item[1])
            if item[0] == 'dashed_line_dash_ratio': object.dashedLineDashRatio = item[1]
            if item[0] == 'dashed_line_gap_ratio': object.dashedLineGapRatio = item[1]
            if item[0] == 'svguseinch' : object.svgUseInch = _b(item[1])
            if item[0] == 'svgprecision' : object.svgPrecision = item[1]
            if item[0] == 'excludeedgelayer' : object.excludeEdgeLayer = _b(item[1])
            if item[0] == 'plotframeref' : object.plotFameRef = _b(item[1])
            if item[0] == 'viasonmask' : object.viasOnMask = _b(item[1])
            if item[0] == 'mode' : object.mode = item[1]
            if item[0] == 'useauxorigin' : object.useAuxOrigin = _b(item[1])
            if item[0] == 'hpglpennumber' : object.hpglPenNumber = item[1]
            if item[0] == 'hpglpenspeed' : object.hpglPenSpeed = item[1]
            if item[0] == 'hpglpendiameter' : object.hpglPenDiameter = item[1]
            if item[0] == 'dxfpolygonmode' : object.dxfPolygonMode = _b(item[1])
            if item[0] == 'dxfimperialunits' : object.dxfImperialUnits = _b(item[1])
            if item[0] == 'dxfusepcbnewfont' : object.dxfUsePcbnewFont = _b(item[1])
            if item[0] == 'psnegative' : object.psNegative = _b(item[1])
            if item[0] == 'psa4output' : object.psA4Output = _b(item[1])
            if item[0] == 'plotreference' : object.plotReference = _b(item[1])
            if item[0] == 'plotvalue' : object.plotValue = _b(item[1])
            if item[0] == 'plotinvisibletext' : object.plotInvisibleText = _b(item[1])
            if item[0] == 'sketchpadsonfab' : object.sketchPadsOnFab = _b(item[1])
            if item[0] == 'subtractmaskfromsilk' : object.subtractMaskFromSilk = _b(item[1])
            if item[0] == 'outputformat' : object.outputFormat = item[1]
            if item[0] == 'mirror' : object.mirror = _b(item[1])
            if item[0] == 'drillshape' : object.drillShape = item[1]
            if item[0] == 'scaleselection' : object.scaleSelection = item[1]
            if item[0] == 'outputdirectory' : object.outputDirectory = item[1]
            if item[0] == 'pdf_front_fp_property_popups' : object.pdfFrontFpPropertyPopups = _b(item[1])
            if item[0] == 'pdf_back_fp_property_popups' : object.pdfBackFpPropertyPopups = _b(item[1])
            if item[0] == 'pdf_metadata' : object.pdfMetadata = _b(item[1])
            if item[0] == 'pdf_single_document' : object.pdfSingleDocument = _b(item[1])
            if item[0] == 'plot_black_and_white' : object.plotBlackAndWhite = _b(item[1])
            if item[0] == 'plotpadnumbers' : object.plotPadNumbers = _b(item[1])
            if item[0] == 'hidednponfab' : object.hideDnpOnFab = _b(item[1])
            if item[0] == 'sketchdnponfab' : object.sketchDnpOnFab = _b(item[1])
            if item[0] == 'crossoutdnponfab' : object.crossoutDnpOnFab = _b(item[1])
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

        _yn = lambda v: 'yes' if v else 'no'

        expression =  f'{indents}(pcbplotparams\n'
        expression += f'{indents}  (layerselection {self.layerSelection})\n'
        if self.plotOnAllLayersSelection is not None:
            expression += f'{indents}  (plot_on_all_layers_selection {self.plotOnAllLayersSelection})\n'
        expression += f'{indents}  (disableapertmacros {_yn(self.disableApertMacros)})\n'
        expression += f'{indents}  (usegerberextensions {_yn(self.useGerberExtensions)})\n'
        expression += f'{indents}  (usegerberattributes {_yn(self.useGerberAttributes)})\n'
        expression += f'{indents}  (usegerberadvancedattributes {_yn(self.useGerberAdvancedAttributes)})\n'
        expression += f'{indents}  (creategerberjobfile {_yn(self.createGerberJobFile)})\n'
        if self.dashedLineDashRatio is not None:
            expression += f'{indents}  (dashed_line_dash_ratio {float(self.dashedLineDashRatio):.6f})\n'
        if self.dashedLineGapRatio is not None:
            expression += f'{indents}  (dashed_line_gap_ratio {float(self.dashedLineGapRatio):.6f})\n'
        if self.svgUseInch is not None:
            expression += f'{indents}  (svguseinch {_yn(self.svgUseInch)})\n'
        expression += f'{indents}  (svgprecision {self.svgPrecision})\n'
        if self.excludeEdgeLayer is not None:
            expression += f'{indents}  (excludeedgelayer {_yn(self.excludeEdgeLayer)})\n'
        expression += f'{indents}  (plotframeref {_yn(self.plotFameRef)})\n'
        expression += f'{indents}  (viasonmask {_yn(self.viasOnMask)})\n'
        expression += f'{indents}  (mode {self.mode})\n'
        expression += f'{indents}  (useauxorigin {_yn(self.useAuxOrigin)})\n'
        if self.pdfFrontFpPropertyPopups is not None:
            expression += f'{indents}  (pdf_front_fp_property_popups {_yn(self.pdfFrontFpPropertyPopups)})\n'
        if self.pdfBackFpPropertyPopups is not None:
            expression += f'{indents}  (pdf_back_fp_property_popups {_yn(self.pdfBackFpPropertyPopups)})\n'
        if self.pdfMetadata is not None:
            expression += f'{indents}  (pdf_metadata {_yn(self.pdfMetadata)})\n'
        if self.pdfSingleDocument is not None:
            expression += f'{indents}  (pdf_single_document {_yn(self.pdfSingleDocument)})\n'
        expression += f'{indents}  (hpglpennumber {self.hpglPenNumber})\n'
        expression += f'{indents}  (hpglpenspeed {self.hpglPenSpeed})\n'
        expression += f'{indents}  (hpglpendiameter {float(self.hpglPenDiameter):.6f})\n'
        expression += f'{indents}  (dxfpolygonmode {_yn(self.dxfPolygonMode)})\n'
        expression += f'{indents}  (dxfimperialunits {_yn(self.dxfImperialUnits)})\n'
        expression += f'{indents}  (dxfusepcbnewfont {_yn(self.dxfUsePcbnewFont)})\n'
        expression += f'{indents}  (psnegative {_yn(self.psNegative)})\n'
        expression += f'{indents}  (psa4output {_yn(self.psA4Output)})\n'
        if self.plotBlackAndWhite is not None:
            expression += f'{indents}  (plot_black_and_white {_yn(self.plotBlackAndWhite)})\n'
        expression += f'{indents}  (plotreference {_yn(self.plotReference)})\n'
        expression += f'{indents}  (plotvalue {_yn(self.plotValue)})\n'
        expression += f'{indents}  (plotinvisibletext {_yn(self.plotInvisibleText)})\n'
        expression += f'{indents}  (sketchpadsonfab {_yn(self.sketchPadsOnFab)})\n'
        if self.plotPadNumbers is not None:
            expression += f'{indents}  (plotpadnumbers {_yn(self.plotPadNumbers)})\n'
        if self.hideDnpOnFab is not None:
            expression += f'{indents}  (hidednponfab {_yn(self.hideDnpOnFab)})\n'
        if self.sketchDnpOnFab is not None:
            expression += f'{indents}  (sketchdnponfab {_yn(self.sketchDnpOnFab)})\n'
        if self.crossoutDnpOnFab is not None:
            expression += f'{indents}  (crossoutdnponfab {_yn(self.crossoutDnpOnFab)})\n'
        expression += f'{indents}  (subtractmaskfromsilk {_yn(self.subtractMaskFromSilk)})\n'
        expression += f'{indents}  (outputformat {self.outputFormat})\n'
        expression += f'{indents}  (mirror {_yn(self.mirror)})\n'
        expression += f'{indents}  (drillshape {self.drillShape})\n'
        expression += f'{indents}  (scaleselection {self.scaleSelection})\n'
        expression += f'{indents}  (outputdirectory "{dequote(self.outputDirectory)}")\n'
        expression += f'{indents}){endline}'
        return expression


@dataclass
class SetupData():
    """The setup token is used to store the current settings such as default item sizes and
    other options used by the board

    Documentation:
        https://dev-docs.kicad.org/en/file-formats/sexpr-pcb/#_setup_section
    """

    stackup: Optional[Stackup] = None
    """The optional ``stackup`` define the parameters required to manufacture the board"""

    packToMaskClearance: float = 0.0
    """The ``packToMaskClearance`` token defines the clearance between footprint pads and
    the solder mask"""

    solderMaskMinWidth: Optional[float] = None
    """The optional ``solderMaskMinWidth`` defines the minimum solder mask width. If not
    defined, the minimum width is zero."""

    padToPasteClearance: Optional[float] = None
    """The optional ``padToPasteClearance`` defines the clearance between footprint pads
    and the solder paste layer. If not defined, the clearance is zero"""

    padToPasteClearanceRatio: Optional[float] = None
    """The optional ``padToPasteClearanceRatio`` is the percentage (from 0 to 100) of the
    footprint pad to make the solder paste. If not defined, the ratio is 100% (the same
    size as the pad)."""

    auxAxisOrigin: Optional[Position] = None
    """The optional ``auxAxisOrigin`` defines the auxiliary origin if it is set to anything
    other than (0,0)."""

    gridOrigin: Optional[Position] = None
    """The optional ``gridOrigin`` defines the grid original if it is set to anything other
    than (0,0)."""

    allowSoldermaskBridgesInFootprints: Optional[bool] = None
    """The optional ``allow_soldermask_bridges_in_footprints`` token. Available since KiCad v8"""

    tentingFront: Optional[bool] = None
    """The ``tenting front`` option. Available since KiCad v8"""

    tentingBack: Optional[bool] = None
    """The ``tenting back`` option. Available since KiCad v8"""

    coveringFront: Optional[bool] = None
    """The ``covering front`` option. Available since KiCad v8"""

    coveringBack: Optional[bool] = None
    """The ``covering back`` option. Available since KiCad v8"""

    pluggingFront: Optional[bool] = None
    """The ``plugging front`` option. Available since KiCad v8"""

    pluggingBack: Optional[bool] = None
    """The ``plugging back`` option. Available since KiCad v8"""

    capping: Optional[bool] = None
    """The ``capping`` option. Available since KiCad v8"""

    filling: Optional[bool] = None
    """The ``filling`` option. Available since KiCad v8"""

    plotSettings: Optional[PlotSettings] = None
    """The optional ``plotSettings`` define how the board was last plotted."""

    @classmethod
    def from_sexpr(cls, exp: list) -> SetupData:
        """Convert the given S-Expresstion into a SetupData object

        Args:
            - exp (list): Part of parsed S-Expression ``(setup ...)``

        Raises:
            - Exception: When given parameter's type is not a list
            - Exception: When the first item of the list is not setup

        Returns:
            - SetupData: Object of the class initialized with the given S-Expression
        """
        if not isinstance(exp, list):
            raise Exception("Expression does not have the correct type")

        if exp[0] != 'setup':
            raise Exception("Expression does not have the correct type")

        object = cls()
        for item in exp:
            if item[0] == 'stackup': object.stackup = Stackup().from_sexpr(item)
            if item[0] == 'pcbplotparams': object.plotSettings = PlotSettings().from_sexpr(item)
            if item[0] == 'pad_to_mask_clearance': object.packToMaskClearance = item[1]
            if item[0] == 'solder_mask_min_width': object.solderMaskMinWidth = item[1]
            if item[0] == 'pad_to_paste_clearance': object.padToPasteClearance = item[1]
            if item[0] == 'pad_to_paste_clearance_ratio': object.padToPasteClearanceRatio = item[1]
            if item[0] == 'aux_axis_origin': object.auxAxisOrigin = Position().from_sexpr(item)
            if item[0] == 'grid_origin': object.gridOrigin = Position().from_sexpr(item)
            if item[0] == 'pcbplotparams': object.plotSettings = PlotSettings().from_sexpr(item)
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

        expression =  f'{indents}(setup\n'
        if self.stackup is not None:                  expression += self.stackup.to_sexpr(indent+2)
        expression += f'{indents}  (pad_to_mask_clearance {self.packToMaskClearance})\n'
        if self.solderMaskMinWidth is not None:       expression += f'{indents}  (solder_mask_min_width {self.solderMaskMinWidth})\n'
        if self.padToPasteClearance is not None:      expression += f'{indents}  (pad_to_paste_clearance {self.padToPasteClearance})\n'
        if self.padToPasteClearanceRatio is not None: expression += f'{indents}  (pad_to_paste_clearance_ratio {self.padToPasteClearanceRatio})\n'
        if self.auxAxisOrigin is not None:            expression += f'{indents}  (aux_axis_origin {self.auxAxisOrigin.X} {self.auxAxisOrigin.Y})\n'
        if self.gridOrigin is not None:               expression += f'{indents}  (grid_origin {self.gridOrigin.X} {self.gridOrigin.Y})\n'
        if self.plotSettings is not None:             expression += self.plotSettings.to_sexpr(indent+2)
        expression += f'{indents}){endline}'
        return expression


@dataclass
class Segment():
    """The ``segment`` token defines a track segment in a KiCad board

    Documentation:
        https://dev-docs.kicad.org/en/file-formats/sexpr-pcb/#_track_segment
    """

    start: Position = field(default_factory=lambda: Position())
    """The ``start`` token defines the coordinates of the beginning of the line"""

    end: Position = field(default_factory=lambda: Position())
    """The ``end`` token defines the coordinates of the end of the line"""

    width: float = 0.1
    """The ``width`` token defines the line width"""

    layer: str = "F.Cu"
    """The ``layer`` token defines the canonical layer the track segment resides on"""

    locked: bool = False
    """The ``locked`` token defines if the line cannot be edited"""

    net: int = 0
    """The ``net`` token defines by the net ordinal number which net in the net
    section that the segment is part of"""

    tstamp: str = ""
    """The ``tstamp`` token defines the unique identifier of the line object"""

    @classmethod
    def from_sexpr(cls, exp: list) -> Segment:
        """Convert the given S-Expresstion into a Segment object

        Args:
            - exp (list): Part of parsed S-Expression ``(segment ...)``

        Raises:
            - Exception: When given parameter's type is not a list
            - Exception: When the first item of the list is not segment

        Returns:
            - Segment: Object of the class initialized with the given S-Expression
        """
        if not isinstance(exp, list):
            raise Exception("Expression does not have the correct type")

        if exp[0] != 'segment':
            raise Exception("Expression does not have the correct type")

        object = cls()
        for item in exp:
            if type(item) != type([]):
                if item == 'locked': object.locked = True
                continue
            if item[0] == 'start': object.start = Position().from_sexpr(item)
            if item[0] == 'end': object.end = Position().from_sexpr(item)
            if item[0] == 'width': object.width = item[1]
            if item[0] == 'layer': object.layer = item[1]
            if item[0] == 'net': object.net = item[1]
            if item[0] == 'tstamp': object.tstamp = item[1]
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
        locked = ' locked' if self.locked else ''

        return f'{indents}(segment{locked} (start {self.start.X} {self.start.Y}) (end {self.end.X} {self.end.Y}) (width {self.width}) (layer "{dequote(self.layer)}") (net {self.net}) (tstamp {self.tstamp})){endline}'

@dataclass
class Via():
    """The ``via`` token defines a track via in a KiCad board

    Documentation:
        https://dev-docs.kicad.org/en/file-formats/sexpr-pcb/#_track_via
    """

    type: Optional[str] = None
    """The optional ``type`` attribute specifies the via type. Valid via types are ``blind`` and
    ``micro``. If no type is defined, the via is a through hole type"""

    locked: bool = False
    """The ``locked`` token defines if the line cannot be edited"""

    position: Position = field(default_factory=lambda: Position())
    """The ``position`` token define the coordinates of the center of the via"""

    size: float = 0.0
    """The ``size`` token define the diameter of the via annular ring"""

    drill: float = 0.0
    """The ``drill`` token define the drill diameter of the via"""

    layers: List[str] = field(default_factory=list)
    """The ``layers`` token define the canonical layer set the via connects as a list
    of strings"""

    removeUnusedLayers: bool = False
    """The ``removeUnusedLayers`` token is undocumented (as of 20.02.2022)"""

    keepEndLayers: bool = False
    """The ``keepEndLayers`` token is undocumented (as of 20.02.2022)"""

    free: bool = False
    """The ``free`` token indicates that the via is free to be moved outside it's assigned net"""

    net: int = 0
    """The ``net`` token defines by net ordinal number which net in the net section that
    the via is part of"""

    tstamp: Optional[str] = None
    """The ``tstamp`` token defines the unique identifier of the via"""

    @classmethod
    def from_sexpr(cls, exp: list) -> Via:
        """Convert the given S-Expresstion into a Via object

        Args:
            - exp (list): Part of parsed S-Expression ``(via ...)``

        Raises:
            - Exception: When given parameter's type is not a list
            - Exception: When the first item of the list is not via

        Returns:
            - Via: Object of the class initialized with the given S-Expression
        """
        if not isinstance(exp, list):
            raise Exception("Expression does not have the correct type")

        if exp[0] != 'via':
            raise Exception("Expression does not have the correct type")

        object = cls()
        for item in exp:
            if type(item) != type([]):
                if item == 'locked': object.locked = True
                if item == 'micro' or item == 'blind': object.type = item
                continue
            if item[0] == 'at': object.position = Position().from_sexpr(item)
            if item[0] == 'size': object.size = item[1]
            if item[0] == 'drill': object.drill = item[1]
            if item[0] == 'layers':
                for layer in item[1:]:
                    object.layers.append(layer)
            if item[0] == 'remove_unused_layers': object.removeUnusedLayers = True
            if item[0] == 'keep_end_layers': object.keepEndLayers = True
            if item[0] == 'free': object.free = True
            if item[0] == 'net': object.net = item[1]
            if item[0] == 'tstamp': object.tstamp = item[1]
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

        type = f' {self.type}' if self.type is not None else ''
        locked = f' locked' if self.locked else ''

        layers = ''
        for layer in self.layers:
            layers += f' "{dequote(layer)}"'
        rum = f' (remove_unused_layers)' if self.removeUnusedLayers else ''
        kel = f' (keep_end_layers)' if self.keepEndLayers else ''
        free = f' (free)' if self.free else ''
        tstamp = f' (tstamp {self.tstamp})' if self.tstamp is not None else ''

        return f'{indents}(via{type}{locked} (at {self.position.X} {self.position.Y}) (size {self.size}) (drill {self.drill}) (layers{layers}){rum}{kel}{free} (net {self.net}){tstamp}){endline}'

@dataclass
class Arc():
    """The ``arc`` token defines a track arc, which will be generated when using the length-matching
    feature on differential pairs.

    Documentation:
        https://dev-docs.kicad.org/en/file-formats/sexpr-pcb/#_track_arc
    """

    start: Position = field(default_factory=lambda: Position())
    """The ``start`` token defines the coordinates of the beginning of the arc"""

    mid: Position = field(default_factory=lambda: Position())
    """The ``mid`` token defines the coordinates of the mid point of the radius of the arc"""

    end: Position = field(default_factory=lambda: Position())
    """The ``end`` token defines the coordinates of the end of the arc"""

    width: float = 0.2
    """The ``width`` token defines the line width of the arc. Defaults to 0,2."""

    layer: str = "F.Cu"
    """The ``layer`` token defiens the canonical layer the track arc resides on. Defaults to `F.Cu`."""

    locked: bool = False
    """The ``locked`` token defines if the arc cannot be edited. Defaults to False."""

    net: int = 0
    """The ``net`` token defines the net ordinal number which net in the net section that arc is part
    of. Defaults to 0."""

    tstamp: Optional[str] = None
    """The optional ``tstamp`` token defines the unique identifier of the arc"""

    @classmethod
    def from_sexpr(cls, exp: list) -> Arc:
        """Convert the given S-Expresstion into a Arc object

        Args:
            - exp (list): Part of parsed S-Expression ``(arc ...)``

        Raises:
            - Exception: When given parameter's type is not a list
            - Exception: When the first item of the list is not ``arc``

        Returns:
            - Arc: Object of the class initialized with the given S-Expression
        """
        if not isinstance(exp, list):
            raise Exception("Expression does not have the correct type")

        if exp[0] != 'arc':
            raise Exception("Expression does not have the correct type")

        object = cls()
        for item in exp:
            if type(item) != type([]):
                if item == 'locked': object.locked = True
                continue
            if item[0] == 'start': object.start = Position().from_sexpr(item)
            elif item[0] == 'mid': object.mid = Position().from_sexpr(item)
            elif item[0] == 'end': object.end = Position().from_sexpr(item)
            elif item[0] == 'width': object.width = item[1]
            elif item[0] == 'layer': object.layer = item[1]
            elif item[0] == 'net': object.net = item[1]
            elif item[0] == 'tstamp': object.tstamp = item[1]
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

        locked = f' locked' if self.locked else ''
        tstamp = f' (tstamp {self.tstamp})' if self.tstamp is not None else ''

        expression = f'{indents}(arc{locked} (start {self.start.X} {self.start.Y}) '
        expression += f'(mid {self.mid.X} {self.mid.Y}) (end {self.end.X} {self.end.Y}) '
        expression += f'(width {self.width}) (layer "{dequote(self.layer)}") '
        expression += f'(net {self.net}){tstamp}){endline}'
        return expression


@dataclass
class Target():
    """The ``target`` token defines a target marker on the PCB

    Documentation:
        Not found in KiCad docu - 15.06.2022
    """

    type: str = "plus"
    """The ``type`` token specifies the shape of the marker. Valid types are ``plus`` and ``x``."""

    position: Position = field(default_factory=lambda: Position())
    """The ``position`` token specifies the position of the target marker"""

    size: float = 0
    """The ``size`` token sets the marker's size"""

    width: float = 0.1
    """The ``width`` token sets the marker's line width"""

    layer: str = "F.Cu"
    """The ``layer`` token sets the canonical layer where the target marker resides"""

    tstamp: Optional[str] = None
    """The ``tstamp`` token defines the unique identifier of the target"""

    @classmethod
    def from_sexpr(cls, exp: list) -> Target:
        """Convert the given S-Expresstion into a Target object

        Args:
            - exp (list): Part of parsed S-Expression ``(target ...)``

        Raises:
            - Exception: When given parameter's type is not a list
            - Exception: When the first item of the list is not target

        Returns:
            - Target: Object of the class initialized with the given S-Expression
        """
        if not isinstance(exp, list):
            raise Exception("Expression does not have the correct type")

        if exp[0] != 'target':
            raise Exception("Expression does not have the correct type")

        object = cls()
        object.type = exp[1]
        for item in exp[2:]:
            if item[0] == 'at': object.position = Position().from_sexpr(item)
            if item[0] == 'size': object.size = item[1]
            if item[0] == 'width': object.width = item[1]
            if item[0] == 'layer': object.layer = item[1]
            if item[0] == 'tstamp': object.tstamp = item[1]
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

        return f'{indents}(target {self.type} (at {self.position.X} {self.position.Y}) (size {self.size}) (width {self.width}) (layer "{self.layer}") (tstamp {self.tstamp})){endline}'
