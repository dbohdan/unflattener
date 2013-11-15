# Copyright (C) 2013 Danyil Bohdan
# All rights Reserved.
import Image
import numpy

pointfive=numpy.float64(1) / 2

class SpriteNormalMap(object):
    def __init__(self):
        self.normal_data = None

    def create_from_files(self, image_file_names, hor_base_level=pointfive,
                                                  vert_base_level=pointfive):
        """
        Generate a normal map from two or more image files.

        Once the files have been loaded from the disk as objects of the class
        Image they are then processed using the create_from_images method.
        """
        images = {}
        for image_file in image_file_names:
            if image_file_names[image_file]: # skip the Nones
                im = Image.open(image_file_names[image_file])
                images[image_file] = im
        self.create_from_images(images, hor_base_level, vert_base_level)

    def create_from_images(self, images, hor_base_level=pointfive,
                                         vert_base_level=pointfive):
        """
        Generate a normal map based on two or more images.

        Once the files have been loaded from the disk and converted to arrays
        they are then processed using the create_from_images method.
        """

        # Convert all Image objects we've been given to numpy arrays.
        self.images = {k: image_to_array(images[k]) for k in images}
        #print self.images
        # Check if all images are the same size
        self.imgshape = image_shape(self.images.values())

        # Create an array for normal map data.
        self.normal_data = numpy.zeros((3, self.imgshape[0],
                                           self.imgshape[1]),
                                       dtype='float64')

        # The core algorithm follows. It will be explained in detail later.

        self.normal_data[0] = (self.images['right'] if 'right' in self.images
                               else hor_base_level) -\
                              (self.images['left'] if 'left' in self.images
                               else hor_base_level) # x_N
        self.normal_data[1] = (self.images['top'] if 'top' in self.images
                               else vert_base_level) -\
                              (self.images['bottom'] if 'bottom'
                               in self.images else vert_base_level) # y_N
        self.normal_data[2] = 1.0

        xy_vector_norms = self.normal_data[0] * self.normal_data[0] +\
                          self.normal_data[1] * self.normal_data[1]

        # Generate z_N data from (x_N, y_N).
        #
        it = numpy.nditer(self.normal_data[2], flags=['multi_index'])
        while not it.finished:
            #print it, it.multi_index, it[0]
            n = xy_vector_norms[it.multi_index]
            #print it.multi_index, n
            if n > 0:
                self.normal_data[2][it.multi_index] = \
                                     numpy.sqrt(max(1 - n / numpy.sqrt(n), 0))
            it.iternext()

    def save_image(self, filename, depth=pointfive):
        """Save the normal map to the image file filename."""
        aim = self.normal_data.copy()
        # Transform x_N, y_N from the -1.0..1.0 range to 0.0..1.0.
        aim[0] = (aim[0] + 1) / 2
        aim[1] = (aim[1] + 1) / 2
        # Compress z_N range. This can be done for aesthetic reasons or due to
        # 3D engine requirements (e.g., Doom 3).
        aim[2] = aim[2] * depth + (1 - depth)

        normal_map = array_to_image(aim)
        normal_map.save(filename)

    def load_image(self, filename, depth=pointfive):
        """Load the normal map from the image file filename.

        The depth setting is explained in save_image.
        """
        im = Image.open(filename)
        r, g, b  = im.split()[:3] # Throw away the alpha channel, if any.
        self.imgshape = r.size[::-1]

        self.normal_data = numpy.zeros((3, self.imgshape[0],
                                           self.imgshape[1]),
                                       dtype='float64')

        self.normal_data[0] = image_to_array(r) # x_N
        self.normal_data[1] = image_to_array(g) # y_N
        self.normal_data[2] = image_to_array(b) # z_N

        self.normal_data[0] = self.normal_data[0] * 2 - 1 # 0..1 -> -1..1
        self.normal_data[1] = self.normal_data[1] * 2 - 1 # 0..1 -> -1..1
        # Account for depth compression of z_N.
        self.normal_data[2] = (self.normal_data[2] - (1 - depth)) / depth

    def apply_light(self, image, light_vector):
        """Not implemented."""
        pass

    def compare(self, other, depth=pointfive):
        """Compares normal map data. Returns True for equivalent maps."""
        return arrays_equivalent(self.normal_data, other.normal_data, depth)

def image_to_array(im):
    """Convert a grayscale image to a numpy array of 0.0..1.0 of float64s."""
    d = im.convert('L').getdata()
    return numpy.array(d, dtype='float64').reshape(im.size[::-1]) / 255

def array_to_image(arr, alpha=None):
    """Convert a numpy array to grayscale or RGB(A) image.

    The numpy array `arr` can either have the shape (w, h) for a grayscale
    image result or a (3, w, h) shape for an RGB image. The alpha channel
    data in `alpha` will be applied to the resulting RGB image if supplied.
    """
    def make_image(arr):
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

def arrays_equivalent(arr1, arr2, depth=pointfive):
    """Compares normal map data array. Returns True for equivalent data.

    The comparison accounts for the discretization error introduced by
    the `depth` setting when normal maps are saved as images.
    """
    max_diff = (numpy.abs(arr1 - arr2)).max() * 255
    return max_diff < max(1 / depth, 2.01)

def image_shape(images):
    """Check if all image in `images` have same shape. Returns that shape."""
    shape = None
    for image in images:
        if not shape:
            shape = image.shape
        else:
            if shape != image.shape:
                raise ValueError
    return shape

