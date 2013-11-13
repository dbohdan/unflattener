# Copyright (C) 2013 Danyil Bohdan
# All rights Reserved.
import Image
import numpy

pointfive=numpy.float64(1) / 2

class SpriteNormalMap(object):
    def __init__(self):
        self.a = None

    def create_from_files(self, image_file_names):
        images = {}
        for image_file in image_file_names:
            if image_file_names[image_file]: # skip the Nones
                im = Image.open(image_file_names[image_file])
                images[image_file] = im
                #images[image_file] = image_to_array(im)
        self.create_from_images(images)

    def create_from_images(self, images, hor_level=pointfive, vert_level=pointfive):
        """
        image_file_names is a dict that should contain the keys
        'left', 'right', 'top' and 'bottom'.
        """
        self.images = {k: image_to_array(images[k]) for k in images}
        print self.images
        # Check if all images are the same size
        self.imgshape = image_shape(self.images.values())

        self.a = numpy.zeros((3, self.imgshape[0], self.imgshape[1]), dtype='float64')
        #self.a[0] = self.images['right'] - self.images['left'] # x_N
        #self.a[1] = self.images['top'] - self.images['bottom'] # y_N
        print 'right' in self.images, 'left' in self.images, 'top' in self.images, 'bottom' in self.images
        self.a[0] = (self.images['right'] if 'right' in self.images else hor_level) -\
                    (self.images['left'] if 'left' in self.images else hor_level) # x_N
        self.a[1] = (self.images['top'] if 'top' in self.images else vert_level) -\
                    (self.images['bottom'] if 'bottom' in self.images else vert_level) # y_N
        self.a[2] = 1.0

        norm = self.a[0] * self.a[0] + self.a[1] * self.a[1]
        it = numpy.nditer(self.a[2], flags=['multi_index'])
        while not it.finished:
            #print it, it.multi_index, it[0]
            n = norm[it.multi_index]
            #print it.multi_index, n
            if n > 0:
                self.a[2][it.multi_index] = numpy.sqrt(max(1 - n / numpy.sqrt(n), 0))
            it.iternext()

    def save_image(self, filename, depth=pointfive):
        aim = self.a.copy()
        aim[0] = (aim[0] + 1) / 2
        aim[1] = (aim[1] + 1) / 2
        # Compress z_N range.
        aim[2] = aim[2] * depth + (1 - depth)

        normal_map = array_to_image(aim)
        normal_map.save(filename)

    def load_image(self, filename, depth=pointfive):
        im = Image.open(filename)
        r, g, b  = im.split()[:3] # throw away alpha
        self.imgshape = r.size[::-1]
        self.a = numpy.zeros((3, self.imgshape[0], self.imgshape[1]), dtype='float64')

        self.a[0] = image_to_array(r)
        self.a[1] = image_to_array(g)
        self.a[2] = image_to_array(b)

        self.a[0] = self.a[0] * 2 - 1
        self.a[1] = self.a[1] * 2 - 1
        self.a[2] = (self.a[2] - (1 - depth)) / depth

    def apply_light(self, image, light_vector):
        pass

    def compare(self, other, depth=pointfive):
        return (self.a - other.a).max() < 2 * depth

def image_to_array(im):
    d = im.convert('L').getdata()
    return numpy.array(d, dtype='float64').reshape(im.size[::-1]) / 255

def array_to_image(arr, alpha=None):
    ni = range(3)
    for i in ni:
        ni[i] = Image.fromarray((arr[i] * 255).astype('uint8'))
    if alpha:
        res = Image.merge('RGBA', ni + [alpha])
    else:
        res = Image.merge('RGB', ni)

    return res

def image_shape(images):
    shape = None
    for image in images:
        if not shape:
            shape = image.shape
        else:
            if shape != image.shape:
                raise ValueError
    return shape
