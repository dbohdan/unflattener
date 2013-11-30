#!/usr/bin/env python
# unflatterer, a normal map generator for 2D art.
# Copyright (C) 2013 Danyil Bohdan
# All rights Reserved.
# See the file LICENSE for licensing information.

import time
import argparse
import numpy
import normalmapgen

descr = """
Generate a normal map for 2D art
"""

epi = """
One input file minimum, at least two (one for each axis) highly recommended.
Input files should be 8-bit grayscale PNGs.
"""

def main():
    t = time.time()

    input_file_types = ['top', 'bottom', 'left', 'right']

    # Parse command line arguments.
    parser = argparse.ArgumentParser(description=descr, epilog=epi)
    for argname in input_file_types:
        parser.add_argument('--' + argname, '-' + argname[0],
                            default=None, help="%s image file" % argname)
    parser.add_argument('--output', '-o', default='result.png',
                        help='output file name')
    parser.add_argument('--depth', '-d', default=normalmapgen.POINTFIVE,
                        help='normal map z_N range')
    args = parser.parse_args()
    argsdict = vars(args)
    # Filter input files from other arguments.
    input_file_names = {k: argsdict[k] for k in input_file_types}
    # Must have at least one input.
    if all(input_file_names[k] is None for k in input_file_names):
        parser.print_help()
        exit(1)

    # Process input files and create a normal map.
    sn = normalmapgen.NormalMap()

    sn.create_from_files(input_file_names)
    sn.save_image(argsdict['output'], depth=numpy.float64(argsdict['depth']))

    # Measure the time all of the above took.
    t = time.time() - t
    print("Execution time: %0.3f s" % t)

if __name__ == '__main__':
    main()
