#!/usr/bin/env python
# unflatterer, a normal map generator for 2D art.
# Copyright (C) 2013 Danyil Bohdan
# All rights Reserved.
# See the file LICENSE for licensing information.

import Image
import os
from normalmapgen import NormalMap
from normalmapgen import image_to_array, array_to_image, arrays_equivalent

im_files = {'left': "zombie-left.png",
           'right': "zombie-right.png",
           'top': "zombie-top.png",
           'bottom': "zombie-bottom.png"}

test_dir = "test-images"

# Append directory prefix to test art file names.
im_files = {k: os.path.join(test_dir, im_files[k]) for k in im_files}

for i in range(8):
    depth = 1.0 / 2**i
    print("Running normal map generation test with depth %0.4f (1 / 2^%i)" %
          (depth, i))
    sn1 = NormalMap()
    sn1.create_from_files(im_files)
    sn1.save_image('result1.png', depth)
    sn2 = NormalMap()
    sn2.load_image('result1.png', depth)
    sn2.save_image('result2.png', depth)
    assert(sn1.compare(sn2, depth))
    assert(sn2.compare(sn1, depth))

print("Testing image to array to image conversion.")
im = Image.open(im_files['left'])
arr_there = image_to_array(im)
arr_back_again = image_to_array(array_to_image(arr_there))
assert(arrays_equivalent(arr_there, arr_back_again))

