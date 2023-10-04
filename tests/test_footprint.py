"""Unittests of footprint related classes

Authors:
    (C) Marvin Mager - @mvnmgrx - 2022

License identifier:
    GPL-3.0
"""

import unittest
from os import path

from tests.testfunctions import to_file_and_compare, prepare_test, cleanup_after_test, TEST_BASE
from kiutils.footprint import Footprint

FOOTPRINT_BASE = path.join(TEST_BASE, 'footprint')

class Tests_Footprint_Legacy(unittest.TestCase):
    """Test cases for Footprints from legacy KiCad versions (<= 5)"""

    def setUp(self) -> None:
        prepare_test(self)
        return super().setUp()

    def test_moduleNameOnlyNumbers(self):
        """Constraints the behavior of legacy footprint names that are only numbers. As they are not
        quoted strings, our parser does parse them as numbers. The behavior was changed in PR #91
        to convert numbers back to strings when exporting to S-Expression"""
        self.testData.pathToTestFile = path.join(FOOTPRINT_BASE, 'legacy', 'test_moduleNameOnlyNumbers')
        footprint = Footprint().from_file(self.testData.pathToTestFile)
        self.assertTrue(to_file_and_compare(footprint, self.testData))

class Tests_Footprint(unittest.TestCase):
    """Test cases for Footprints"""

    def setUp(self) -> None:
        prepare_test(self)
        return super().setUp()

    def test_allFootprintItems(self):
        """Tests the parsing of all available footprint items"""
        self.testData.pathToTestFile = path.join(FOOTPRINT_BASE, 'test_allFootprintItems')
        footprint = Footprint().from_file(self.testData.pathToTestFile)
        self.assertTrue(to_file_and_compare(footprint, self.testData))

    def test_footprintPadNewLines(self):
        """Tests the ability of the parser to create the correct new-line breaks when using
        exotic footprint pad combinations"""
        self.testData.compareToTestFile = True
        self.testData.pathToTestFile = path.join(FOOTPRINT_BASE, 'test_footprintPadNewLines')
        footprint = Footprint().from_file(self.testData.pathToTestFile)
        self.assertTrue(to_file_and_compare(footprint, self.testData))

    def test_footprintEmptyAttributes(self):
        """Tests the correct parsing of a footprint with empty ``Attributes`` field

        </p><b>Note:</b> Some earlier versions of KiCad seemed to include the ``(attr ..)`` token in footprints even
        when no attributes are set (or when using standard attributes). This test includes an empty
        attribute token in the footprint and expects it to be gone after parsing. </p>
        """
        self.testData.pathToTestFile = path.join(FOOTPRINT_BASE, 'test_footprintEmptyAttributes')
        footprint = Footprint().from_file(self.testData.pathToTestFile)
        self.assertTrue(to_file_and_compare(footprint, self.testData))

    def test_createNewFootprintTypeSMD(self):
        """Tests the ``create_new()`` function to create a new footprint with the type ``smd``"""
        self.testData.compareToTestFile = True
        self.testData.pathToTestFile = path.join(FOOTPRINT_BASE, 'test_createNewFootprintTypeSMD')

        # Create footprint with correct type
        footprint = Footprint().create_new(
            type = 'smd',
            library_id = 'empty-footprint-smd',
            value = 'empty-footprint-smd'
        )

        # Set timestamps to be the same as in the expected test output
        footprint.tedit = '6328915F'

        self.assertTrue(to_file_and_compare(footprint, self.testData))

    def test_createNewFootprintTypeTHT(self):
        """Tests the ``create_new()`` function to create a new footprint with the type ``through_hole``"""
        self.testData.compareToTestFile = True
        self.testData.pathToTestFile = path.join(FOOTPRINT_BASE, 'test_createNewFootprintTypeTHT')

        # Create footprint with correct type
        footprint = Footprint().create_new(
            type = 'through_hole',
            library_id = 'empty-footprint-through_hole',
            value = 'empty-footprint-through_hole'
        )

        # Set timestamps to be the same as in the expected test output
        footprint.tedit = '63289145'

        self.assertTrue(to_file_and_compare(footprint, self.testData))

    def test_createNewFootprintTypeOther(self):
        """Tests the ``create_new()`` function to create a new footprint with the type ``other``"""
        self.testData.compareToTestFile = True
        self.testData.pathToTestFile = path.join(FOOTPRINT_BASE, 'test_createNewFootprintTypeOther')

        # Create footprint with correct type
        footprint = Footprint().create_new(
            type = 'other',
            library_id = 'empty-footprint-other',
            value = 'empty-footprint-other'
        )
        # Set timestamps to be the same as in the expected test output
        footprint.tedit = '6328916A'

        self.assertTrue(to_file_and_compare(footprint, self.testData))
    
    def test_3dModelHideProperty(self):
        """Tests the 3d model hide property (see issue #96)"""
        self.testData.compareToTestFile = True
        self.testData.pathToTestFile = path.join(FOOTPRINT_BASE, 'test_3dModelHideProperty')
        footprint = Footprint().from_file(self.testData.pathToTestFile)
        self.assertTrue(to_file_and_compare(footprint, self.testData))

class Tests_Footprint_Since_V7(unittest.TestCase):
    """Test cases for Footprints since KiCad 7"""

    def setUp(self) -> None:
        prepare_test(self)
        return super().setUp()

    def test_textBoxAllVariants(self):
        """Tests all variants of the ``text_box`` token for text boxes in footprints"""
        self.testData.compareToTestFile = True
        self.testData.pathToTestFile = path.join(FOOTPRINT_BASE, 'since_v7', 'test_textBoxAllVariants')
        footprint = Footprint().from_file(self.testData.pathToTestFile)
        self.assertTrue(to_file_and_compare(footprint, self.testData))

    def test_imageWithLayerToken(self):
        """Tests the new ``layer`` token for images in footprints"""
        self.testData.compareToTestFile = True
        self.testData.pathToTestFile = path.join(FOOTPRINT_BASE, 'since_v7', 'test_imageWithLayerToken')
        footprint = Footprint().from_file(self.testData.pathToTestFile)
        self.assertTrue(to_file_and_compare(footprint, self.testData))
        
    def test_textsWithRenderCaches(self):
        """Tests text elements with the ``render_cache`` token"""
        self.testData.compareToTestFile = True
        self.testData.pathToTestFile = path.join(FOOTPRINT_BASE, 'since_v7', 'test_textsWithRenderCaches')
        footprint = Footprint().from_file(self.testData.pathToTestFile)
        self.assertTrue(to_file_and_compare(footprint, self.testData))     

    def test_exemptFromCourtyardToken(self):
        """Tests the ``allow_missing_courtyard`` token"""
        self.testData.compareToTestFile = True
        self.testData.pathToTestFile = path.join(FOOTPRINT_BASE, 'since_v7', 'test_exemptFromCourtyardToken')
        footprint = Footprint().from_file(self.testData.pathToTestFile)
        self.assertTrue(to_file_and_compare(footprint, self.testData))

    def test_3dModelOpacityToken(self):
        """Tests the ``opacity`` token of a 3d-model"""
        self.testData.compareToTestFile = True
        self.testData.pathToTestFile = path.join(FOOTPRINT_BASE, 'since_v7', 'test_3dModelOpacityToken')
        footprint = Footprint().from_file(self.testData.pathToTestFile)
        self.assertTrue(to_file_and_compare(footprint, self.testData))

    def test_privateLayersToken(self):
        """Tests the ``private_layers`` token of a footprint"""
        self.testData.compareToTestFile = True
        self.testData.pathToTestFile = path.join(FOOTPRINT_BASE, 'since_v7', 'test_privateLayersToken')
        footprint = Footprint().from_file(self.testData.pathToTestFile)
        self.assertTrue(to_file_and_compare(footprint, self.testData))
        
    def test_netTiePadGroups(self):
        """Tests the ``net_tie_pad_groups`` token of a footprint"""
        self.testData.compareToTestFile = True
        self.testData.pathToTestFile = path.join(FOOTPRINT_BASE, 'since_v7', 'test_netTiePadGroups')
        footprint = Footprint().from_file(self.testData.pathToTestFile)
        self.assertTrue(to_file_and_compare(footprint, self.testData))

