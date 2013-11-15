#!/usr/bin/env python
# Copyright (C) 2013 Danyil Bohdan
# All rights Reserved.
import Image
from SpriteNormalMap import SpriteNormalMap
from SpriteNormalMap import image_to_array, array_to_image, arrays_equivalent

im_files= {'left': "zombie-left.png",
           'right': "zombie-right.png",
           'top': "zombie-top.png",
           'bottom': "zombie-bottom.png"}

for i in range(8):
    depth = 1.0 / 2**i
    print("Running normal map generation test with depth %0.4f (1 / 2^%i)" %
          (depth, i))
    sn = SpriteNormalMap()
    sn.create_from_files(im_files)
    sn.save_image('result.png', depth)
    sn1 = SpriteNormalMap()
    sn1.load_image('result.png', depth)
    sn1.save_image('res2.png', depth)
    assert(sn.compare(sn1, depth))

print("Testing image to array to image conversion.")
im = Image.open(im_files['left'])
imarr1 = image_to_array(im)
imarr2 = image_to_array(array_to_image(imarr1))
assert(arrays_equivalent(imarr1, imarr2))
