#!/usr/bin/env python
# unflattener, a normal map generator for 2D art.
# Copyright (C) 2013 Danyil Bohdan
# All rights Reserved.
# See the file LICENSE for licensing information.
"""
Implements simple sanity checks for NormalMap and functions from normalmapgen.
"""

from __future__ import print_function

from PIL import Image
import os
from normalmapgen import NormalMap
from normalmapgen import image_to_array, array_to_image, arrays_equivalent

TESTFILENAMES = {'left': "robot-left.png",
                 'right': "robot-right.png",
                 'top': "robot-top.png",
                 'bottom': "robot-bottom.png"
                }

TESTDIR = "test-images"

# Append directory prefix to test art file names.
TESTIMAGEFILES = {k: os.path.join(TESTDIR, TESTFILENAMES[k]) \
                  for k in TESTFILENAMES}

def map_gen_test():
    """Test generating normal maps of varying depths from image files"""

    for i in range(8):
        depth = 1.0 / 2**i
        print("Running normal map generation test with depth %0.4f (1 / 2^%i)" %
              (depth, i))
        nm1 = NormalMap()
        nm1.create_from_files(TESTIMAGEFILES)
        nm1.save_image('result1.png', depth)
        # nm1.save_image("result-%u.png" % i, depth)
        nm2 = NormalMap()
        nm2.load_image('result1.png', depth)
        nm2.save_image('result2.png', depth)
        assert(nm1.compare(nm2, depth))
        assert(nm2.compare(nm1, depth))

def image_comp_test():
    """Test `image_to_array` and `array_to_image` functions."""

    print("Testing image to array to image conversion.")
    im = Image.open(TESTIMAGEFILES['left'])
    arr_there = image_to_array(im)
    arr_back_again = image_to_array(array_to_image(arr_there))
    assert(arrays_equivalent(arr_there, arr_back_again))

def main():
    map_gen_test()
    image_comp_test()

if __name__ == "__main__":
    main()
