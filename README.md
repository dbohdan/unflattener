unflattener
===========

Unflattener is a free and open source Python module and a command line tool (`unflatten.py`) that helps you make normal maps for 2D sprites and other graphics. You can use the normal maps it generates to implement dynamic lighting in video games.

Example
=======

![D-lit images and the resulting normal map](readme-illustrations/illustration1.png)

![Together the diffuse and normal maps create dynamic lighting](readme-illustrations/illustration2.png)

![Dynamic lighting in gimp-normalmap in motion](readme-illustrations/animation1.gif)

How it works
============

Unflattener takes as input images of your object lit by a light source pointing directly at that object from four directions: top, bottom, left and right (we call those images "directionally lit" or "d-lit" — like "d-pad"). At least one such image is required, a least two (one with light from the top or the bottom, one with light from the left or the right) are highly recommended.

Unflattener is written in Python and requires the libraries [NumPy](http://www.numpy.org/) and [PIL](http://www.pythonware.com/products/pil/) to work. Python programs can access its functionality directly by importing the `NormalMap` class from the module `unflattener.normalmapgen`. Right now Unflattener cannot do dynamic lighting previews, so you'll need a third-party tool like the [gimp-normalmap](https://code.google.com/p/gimp-normalmap/) plugin for [GIMP](http://www.gimp.org/) for that.

This project was inspired by [Sprite Lamp](http://snakehillgames.com/spritelamp/).

The core algorithm is explained in a (rather lengthy) comment in the method `NormalMap.create_from_images` in `normalmapgen.py`. You'll find some tips on how the input artwork should look in the same comment.

The general idea is that in the d-lit images your object should look as if it were

1. uniformly matte white in color with no self-shadowing;
2. lit by a very distant light source much larger than itself that creates no highlights.

Installation
============

Unflattener has been tested to work under Linux (Ubuntu 12.04, Fedora 19 and Debian 7) and Windows (XP, 7 and 8.1).

You'll need Python 2.7 (v2.6 and earlier won't work due to the use of dict comprehensions), NumPy and either PIL (the Python Imaging Library) or its replacement Pillow to run Unflattener.

Once you've installed the dependencies (see below) clone this repository. You can run Unflattener on the test images without installing it with `run.sh` on Linux or `run-win.cmd` on Windows. To generate normal maps for other images you can either edit those files as needed, directly run `unflattener/unflatten.py` or use Setuptools to install the Unflattener package and get the command `unflatten` (on Linux / OS X).

Run the command `sudo python setup.py test` or run the test suite (`unflattener/tests/__init__.py`) directly to verify that everything works correctly.


Debian and Ubuntu
-----------------

You can install the required packages from the command line with

    sudo apt-get install python-numpy python-imaging python-setuptools

To install gimp-normalmap do

	sudo apt-get install gimp-normalmap

If you want the command `unflatten` on your system or you want to import Unflattener's normal map generator in your own Python projects install it as a package with

    sudo python setup.py install

Fedora
------

You can install the required packages from the command line with

    su -
    yum install numpy python-pillow python-setuptools

To install gimp-normalmap do

    su -
    yum install gimp-normalmap

If you want the command `unflatten` in your system or you want to import Unflattener's normal map generator in your own Python projects install it as a package with

    su -
    python setup.py install

Windows
-------

On Windows first install Python 2.7 using the official installer from <http://python.org/download/>. After that is done download and run the following package installers from <http://www.lfd.uci.edu/~gohlke/pythonlibs/>:

* numpy-MKL-1.8.0.win32-py2.7.exe
* Pillow-2.2.1.win32-py2.7.exe

Only 32-bit versions of Python and its libraries have been tested on Windows (both 32-bit and 64-bit versions), so it is recommended that you use them.

If you want to import Unflattener's normal map generator in your own Python projects install it as a package by running the command

    python setup.py install

on the Command Prompt as an administrator.

Usage
=====

    usage: unflatten.py [-h] [--top TOP] [--bottom BOTTOM] [--left LEFT]
                        [--right RIGHT] [--output OUTPUT] [--depth DEPTH]

    Generate a normal map for 2D art

    optional arguments:
      -h, --help            show this help message and exit
      --top TOP, -t TOP     top image file
      --bottom BOTTOM, -b BOTTOM
                            bottom image file
      --left LEFT, -l LEFT  left image file
      --right RIGHT, -r RIGHT
                            right image file
      --output OUTPUT, -o OUTPUT
                            output file name
      --depth DEPTH, -d DEPTH
                            normal map z_N range

    One input file minimum, at least two (one for each axis) highly recommended.
    Input files should be 8-bit grayscale PNGs.

Art requested
=============

Wanted: d-lit artwork. The developer of this project would love to see how Unflattener works for your artwork or game.

[File an issue](https://github.com/dbohdan/unflattener/issues) to have a link to your work added here.

License information
===================

Unflattener is distributed under the new (3-clause) BSD license. See the file `LICENSE`.

Robot sprite originally from the [Bits & Bots art pack](http://opengameart.org/content/bits-bots-art-pack) by MoikMellah. The sprite and its derivatives are licensed under the Creative Commons CC-BY-SA 3.0 license.
