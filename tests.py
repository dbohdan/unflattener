#!/usr/bin/env python
# Copyright (C) 2013 Danyil Bohdan
# All rights Reserved.
from SpriteNormalMap import SpriteNormalMap

im_files= {'left': "zombie-left.png",
           'right': "zombie-right.png",
           'top': "zombie-top.png",
           'bottom': "zombie-bottom.png"}

for i in range(8):
    depth = 1.0 / 2**i
    print("Running tests with depth %0.4f (1 / 2^%i)" % (depth, i))
    sn = SpriteNormalMap()
    sn.create(im_files)
    sn.save_image('result.png', depth)
    sn1 = SpriteNormalMap()
    sn1.load_image('result.png', depth)
    sn1.save_image('res2.png', depth)
    assert(sn.compare(sn1))
