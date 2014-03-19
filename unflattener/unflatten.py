#!/usr/bin/env python
# unflattener, a normal map generator for 2D art.
# Copyright (C) 2013, 2014 Danyil Bohdan
# All rights Reserved.
# See the file LICENSE for licensing information.
"""
Provides a command line interface for the NormalMap class.
"""

from __future__ import print_function

import time
import argparse
import numpy
from unflattener import normalmapgen

DESCRIPTION = """
Generate a normal map for 2D art
"""

EPILOG = """
One input file minimum, at least two (one for each axis) highly recommended.
Input files should be 8-bit grayscale PNGs.
"""

def main():
    run_time = time.time()

    input_file_types = ['top', 'bottom', 'left', 'right']

    # Parse command line arguments.
    parser = argparse.ArgumentParser(description=DESCRIPTION, epilog=EPILOG)
    for argname in input_file_types:
        parser.add_argument('--' + argname, '-' + argname[0],
                            default=None, help="%s image file" % argname)
    parser.add_argument('--output', '-o', default='result.png',
                        help='output file name')
    parser.add_argument('--depth', '-d', default=normalmapgen.POINT_FIVE,
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
    normal_map = normalmapgen.NormalMap()

    normal_map.create_from_files(input_file_names)
    normal_map.save_image(argsdict['output'],
                          depth=numpy.float64(argsdict['depth']))

    # Measure the time all of the above took.
    run_time = time.time() - run_time
    print("Execution time: %0.3f s" % run_time)

if __name__ == '__main__':
    main()
