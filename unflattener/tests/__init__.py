#!/usr/bin/env python
# unflattener, a normal map generator for 2D art.
# Copyright (c) 2013, 2014, 2015, 2016, 2017 dbohdan
# All rights reserved.
# See the file LICENSE for licensing information.
"""
Implements simple sanity checks for NormalMap and functions from normalmapgen.
"""

from __future__ import print_function

from unflattener.normalmapgen import NormalMap
from unflattener.normalmapgen import image_to_array, array_to_image, \
                                       arrays_equivalent

from PIL import Image
import os
import unittest

TEST_FILE_NAMES = {'left': "robot-left.png",
                 'right': "robot-right.png",
                 'top': "robot-top.png",
                 'bottom': "robot-bottom.png"
                }

TEST_DIR = "test-images"

# Append directory prefix to test art file names.
TEST_IMAGE_FILES = {k: os.path.join(TEST_DIR, TEST_FILE_NAMES[k]) \
                    for k in TEST_FILE_NAMES}

class UnflattenerTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def test_map_gen(self):
        """Test generating normal maps of varying depths from image files"""

        print()
        for i in range(8):
            depth = 1.0 / 2**i
            print("Running normal map generation test with " +
                   "depth %0.4f (1 / 2^%i)" %
                   (depth, i))
            nm1 = NormalMap()
            nm1.create_from_files(TEST_IMAGE_FILES)
            nm1.save_image('result1.png', depth)
            # nm1.save_image("result-%u.png" % i, depth)
            nm2 = NormalMap()
            nm2.load_image('result1.png', depth)
            nm2.save_image('result2.png', depth)
            self.assertTrue(nm1.compare(nm2, depth))
            self.assertTrue(nm2.compare(nm1, depth))

    def test_image_comp(self):
        """Test `image_to_array` and `array_to_image` functions"""

        print()
        print("Testing image to array to image conversion.")
        im = Image.open(TEST_IMAGE_FILES['left'])
        arr_there = image_to_array(im)
        arr_back_again = image_to_array(array_to_image(arr_there))
        self.assertTrue(arrays_equivalent(arr_there, arr_back_again))


def suite():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTest(loader.loadTestsFromTestCase(UnflattenerTestCase))
    return suite


if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(suite())
