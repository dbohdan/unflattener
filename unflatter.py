#!/usr/bin/env python
# Copyright (C) 2013 Danyil Bohdan
# All rights Reserved.
import time
import argparse
from SpriteNormalMap import SpriteNormalMap

def main():
    t = time.time()

    parser = argparse.ArgumentParser(description='.', epilog="two files min")
    for argname in ['top', 'bottom', 'left', 'right']:
        parser.add_argument('--' + argname,
                            default=None, help="%s image file" % argname)

    args, unknown = parser.parse_known_args()

    sn = SpriteNormalMap()

    sn.create_from_files(vars(args))
    sn.save_image("result-new.png", 0.5)

    t = time.time() - t
    print("Execution time: %0.3f s" % t)

if __name__ == '__main__':
    main()
