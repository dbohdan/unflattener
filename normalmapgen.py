# unflattener, a normal map generator for 2D art.
# Copyright (C) 2013 Danyil Bohdan
# All rights Reserved.
# See the file LICENSE for licensing information.
"""
Implements the NormalMap class.
"""

from __future__ import print_function

__author__ = 'Danyil Bohdan'
__copyright__ = 'Copyright (C) 2013 Danyil Bohdan'
__license__ = 'BSD'

import Image
import numpy

POINTFIVE = numpy.float64(1) / 2

class NormalMap(object):
    """Generates, stores and saves/loads normal maps for 2D, d-lit* art.

    * directionally lit.
    """

    def __init__(self):
        self.normal_data = None
        self.images = None
        self.image_shape = None

    def create_from_files(self, image_file_names, hor_base_level=POINTFIVE,
                                                  vert_base_level=POINTFIVE):
        """
        Generate a normal map from two or more image files.

        Loads the files from disk and converted to arrays
        They are then processed using the `create_from_images` method.
        The dict `image_file_names` must have at least one of the following
        keys: "top", "bottom", "left", "right". Keys can also be `None`.

        See `create_from_images`.
        """
        images = {}
        for image_file in image_file_names:
            if image_file_names[image_file] is not None:
                im = Image.open(image_file_names[image_file])
                images[image_file] = im
        self.create_from_images(images, hor_base_level, vert_base_level)

    def create_from_images(self, images, hor_base_level=POINTFIVE,
                                         vert_base_level=POINTFIVE):
        """
        Generate a normal map based on one or more images.

        The dict `images` must have at least one of the following keys:
        "top", "bottom", "left", "right". Keys can also be `None`.

        `hor_base_level` and `vert_base_level` are the values that replace
        pixel values for missing horizontal (left, right) and vertical (top,
        bottom) lighting images respectively.
        """

        # Convert all Image objects we've been given to numpy arrays.
        self.images = {k: image_to_array(images[k]) for k in images}
        # Check if all images are the same size, raise exception otherwise
        self.image_shape = image_shape(self.images.values())

        # Create an array for normal map data. The dimenstions are
        # [color_channel, x, y], where [0, x, y] stands for the red channel,
        # [1, x, y] for green and [2, x, y] for blue.
        self.normal_data = numpy.zeros((3, self.image_shape[0],
                                            self.image_shape[1]),
                                       dtype='float64')
        self.normal_data[0] = (self.images['right'] if 'right' in self.images
                               else hor_base_level) -\
                              (self.images['left'] if 'left' in self.images
                               else hor_base_level) # x_N
        self.normal_data[1] = (self.images['top'] if 'top' in self.images
                               else vert_base_level) -\
                              (self.images['bottom'] if 'bottom'
                               in self.images else vert_base_level) # y_N
        self.normal_data[2] = 1 # z_N; we determine its values later.

        # Vector norms squared.
        xy_vector_norms_sq = self.normal_data[0] * self.normal_data[0] +\
                             self.normal_data[1] * self.normal_data[1]

        # Generate z_N data from (x_N, y_N).
        it = numpy.nditer(self.normal_data[2], flags=['multi_index'])
        while not it.finished:
            n = xy_vector_norms_sq[it.multi_index]
            if n > 0:
                # Assume N = (x_N, y_N, z_N) to be a unit vector, i.e., N dot N = 1
                # Hence z_N^2 = 1 - x_N^2 - y_N^2. Otherwise if
                # x_N^2 + y_N^2 >= 0 then z_N = 0.
                self.normal_data[2][it.multi_index] = \
                                     numpy.sqrt(max(1 - n / numpy.sqrt(n), 0))
            it.iternext()

    def save_image(self, filename, depth=POINTFIVE):
        """Save the normal map to the image file `filename`."""
        preproc_data = self.normal_data.copy()
        # Transform x_N, y_N from the -1.0..1.0 range to 0.0..1.0.
        preproc_data[0] = (preproc_data[0] + 1) / 2
        preproc_data[1] = (preproc_data[1] + 1) / 2
        # Compress z_N range. This can be done for aesthetic reasons or due to
        # 3D engine requirements (e.g., Doom 3).
        preproc_data[2] = preproc_data[2] * depth + (1 - depth)

        normal_map = array_to_image(preproc_data)
        normal_map.save(filename)

    def load_image(self, filename, depth=POINTFIVE):
        """Load the normal map from the image file `filename`.

        The `depth` setting is explained in `save_image`.
        """
        im = Image.open(filename)
        r, g, b  = im.split()[:3] # Throw away the alpha channel, if any.
        # image_shape is array shape transposed.
        self.image_shape = r.size[::-1]

        self.normal_data = numpy.zeros((3, self.image_shape[0],
                                           self.image_shape[1]),
                                       dtype='float64')

        self.normal_data[0] = image_to_array(r) # x_N
        self.normal_data[1] = image_to_array(g) # y_N
        self.normal_data[2] = image_to_array(b) # z_N

        # Change range from 0.0..1.0 -> -1.0..1.0
        self.normal_data[0] = self.normal_data[0] * 2 - 1
        self.normal_data[1] = self.normal_data[1] * 2 - 1
        # Reverse depth compression of z_N.
        self.normal_data[2] = (self.normal_data[2] - (1 - depth)) / depth

    def apply_light(self, image, light_vector):
        """Not implemented."""
        raise NotImplementedError

    def compare(self, other, depth=POINTFIVE):
        """Compares normal map data with arrays_equivalent.

        Returns True for equivalent maps."""
        return arrays_equivalent(self.normal_data, other.normal_data, depth)

def image_to_array(im):
    """Convert a grayscale image to a numpy array of 0.0..1.0 of float64s."""
    data = im.convert('L').getdata()
    return numpy.array(data, dtype='float64').reshape(im.size[::-1]) / 255

def array_to_image(arr, alpha=None):
    """Convert a numpy array to grayscale or RGB(A) image.

    The numpy array `arr` can either have the shape (w, h) for a grayscale
    image result or a (3, w, h) shape for an RGB image. The alpha channel
    data in `alpha` will be applied to the resulting RGB image if supplied.
    `arr` is expected to have values in the range of 0.0..1.0.
    """
    def make_image(arr):
        """Convert numpy array to image."""
        return Image.fromarray((arr * 255).astype('uint8'))

    # Produce an RGB(A) image from an array with three values per point.
    if arr.ndim == 3:
        ni = range(3)
        for i in ni:
            ni[i] = make_image(arr[i])
        if alpha:
            res = Image.merge('RGBA', ni + [alpha])
        else:
            res = Image.merge('RGB', ni)
    # Produce a grayscale image from a 1-value array.
    elif arr.ndim == 2:
        res = make_image(arr)
    else:
        raise ValueError
    return res

def arrays_equivalent(arr1, arr2, depth=POINTFIVE):
    """Compares normal map data array. Returns True for equivalent data.

    "Equivalent" here doesn't mean "equal". The comparison accounts for the
    discretization error introduced by the `depth` setting when normal maps
    are saved as images.
    """
    max_diff = (numpy.abs(arr1 - arr2)).max() * 255
    return max_diff < max(1 / depth, 2.01)

def image_shape(images):
    """Check if all image in `images` have same shape and return that shape."""
    shape = None
    for image in images:
        if not shape:
            shape = image.shape
        else:
            if shape != image.shape:
                raise ValueError
    return shape

