# unflattener, a normal map generator for 2D art.
# Copyright (C) 2013, 2014 Danyil Bohdan
# All rights Reserved.
# See the file LICENSE for licensing information.
"""
Implements the NormalMap class.
"""

from __future__ import print_function

from PIL import Image
import numpy

POINT_FIVE = numpy.float64(1) / 2


class NormalMap(object):
    """Generates, stores and saves/loads normal maps for 2D, d-lit* art.

    * directionally lit.
    """

    def __init__(self):
        self.normal_data = None
        self.images = None
        self.image_shape = None

    def create_from_files(self, image_file_names, hor_base_level=POINT_FIVE,
                                                  vert_base_level=POINT_FIVE):
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

    def create_from_images(self, images, hor_base_level=POINT_FIVE,
                                         vert_base_level=POINT_FIVE):
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

        # (What follows is an explanation of how the algorithm works.
        # The explanation is a work in progress.)
        #
        # For our purposes 2D artwork (sprites, textures, etc.) represents
        # a projection of a 3D object on a flat surface. We can think of that
        # object itself as a surface with varying height with no overhanging
        # parts (imagine a wall relief sculpture or furniture covered with
        # a piece of cloth).
        #
        # Our goal here is to obtain per-pixel tangent-space
        # normal map data or, in other words, a map of where the normal vectors
        # point relative to the surface of the object. To do this we will use
        # grayscale images showing what our relief-type object would look like
        # when lit by a light source pointed directly at it from four
        # directions (top, bottom, left and right) if this object were
        # uniformly white in color with no self-shadowing.
        # (We call these images "directionally lit" or "d-lit" -- like
        # "d-pad"). There should also be no highlights -- as though
        # the light source were very large relative to the object and placed
        # very far away. We can use fewer
        # images than four to generate normal maps but for complex objects
        # (complex artwork) that might not yield good results.
        #
        # The motivation behind this method is that our
        # human brains seem to find it easier to produce such images for
        # imagined objects than to draw normal maps directly.
        #
        # The reason we can obtain a normal map from d-lit images is because of
        # the role normal maps play in calculating lighting. To determine how
        # brightly lit a given pixel is (to find its illumination value "I")
        # when calculating lighting we go through the image
        # and for each pixel of our graphic we calculate the scalar product
        # of its normal vector (x_N, y_N, z_N) and the vector (x_L, y_L, z_L)
        # pointing towards our light source.
        #
        # Each coordinate of both vectors is in range -1..1.
        # Below "dot" denotes the dot product of two vectors.
        #
        #     I_pr = N dot L = x_N * x_L + y_N * y_L + z_N * z_L
        #     I = max(min(I_pr, 1), 0)
        #
        # Now if we craft special images where each pixel is a product
        # of the normal vector and a pre-set lighting vector we can use them
        # to obtain normal data. This is what d-lit images are.
        #
        # Image     Vector
        # ---------------------------------
        # Right     L_right  =  ( 1,  0, 0)
        # Left      L_left   =  (-1,  0, 0)
        # Top       L_top    =  ( 0,  1, 0)
        # Bottom    L_bottom =  ( 0, -1, 0)
        #
        # For example, N dot L_right equals x_N for x_N: 0 < x_N <= 1 (but
        # _not_ x_N: -1 <= x_N < 0).
        #
        #     N dot L_right = max(min(x_N, 1), 0)
        #
        # N dot L_left equals x_N for x_N: -1 <= x_N < 0 (x_N for x_N: 0 < x_N
        # <= 1).
        #
        #     N dot L_left = max(min(-x_N, 1), 0)
        #
        # Hence,
        #
        #     x_N = (N dot L_right) - (N dot L_left)
        #
        # and, similarly,
        #
        #       y_N = (N dot L_top) - (N dot L_bottom).
        #
        # How z_N is obtained is described in a comment further below.
        #
        # Note: this explanation uses a coordinate system as pictured.
        # z_N points towards the reader.
        #
        #     ^ y
        #     |
        #     +---------------------------+
        #     | image                     |
        #     |             y_N           |
        #     |                           |
        #     |             ^             |
        #     |             |             |
        #     |             |             |
        #     |             o---> x_N     |
        #     |            /              |
        #     |          |/               |
        #     |          +--              |
        #     |      z_N                  |
        #     |                           |
        #     |                           |
        #     +---------------------------+---> x


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
                # Assume N = (x_N, y_N, z_N) to be a unit vector, i.e.,
                # N dot N = 1
                # Hence, z_N^2 = 1 - x_N^2 - y_N^2. Otherwise if
                # x_N^2 + y_N^2 >= 0 then z_N = 0.
                self.normal_data[2][it.multi_index] = \
                                     numpy.sqrt(max(1 - n / numpy.sqrt(n), 0))
            it.iternext()

    def save_image(self, filename, depth=POINT_FIVE):
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

    def load_image(self, filename, depth=POINT_FIVE):
        """Load the normal map from the image file `filename`.

        The `depth` setting is explained in `save_image`.
        """
        im = Image.open(filename)
        im.load()
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

    def compare(self, other, depth=POINT_FIVE):
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
        ni = list(range(3))
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


def arrays_equivalent(arr1, arr2, depth=POINT_FIVE):
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

