#!/usr/bin/env python
# Copyright (C) 2013 Danyil Bohdan
# All rights Reserved.
import Image
import numpy
import time


class SpriteNormalMap(object):
    def __init__(self):
        pass
    
    def create(self, image_file_names, depth=numpy.float64(1) / 2):
        """
        image_file_names is a dict that should contain the keys
        'left', 'right', 'top' and 'bottom'.
        """
        self.images = {}
        self.depth = depth
        self.imgshape = None
        for imagefile in image_file_names:
            im = Image.open(image_file_names[imagefile])
            self.images[imagefile] = convert(im)
            # Check if all images are the same size
            if not self.imgshape:
                self.imgshape = self.images[imagefile].shape
            else:
                if self.imgshape != self.images[imagefile].shape:
                    print image_file_names[imagefile], self.images, self.imgshape, self.images[imagefile].shape
                    raise EValueError
                    
        self.a = numpy.zeros((3, self.imgshape[0], self.imgshape[1]), dtype='float64')
        
        self.a[0] = self.images['right'] - self.images['left'] # x_N
        self.a[1] = self.images['top'] - self.images['bottom'] # y_N
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
    
    def save_image(self, filename):
        aim = self.a.copy()
        aim[0] = (aim[0] + 1) / 2
        aim[1] = (aim[1] + 1) / 2
        # Compress z_N range.
        aim[2] = aim[2] * self.depth + (1 - self.depth)

        normal_map = back(aim)
        normal_map.save(filename)
        
    def load_image(self, filename):
        pass
        
    def light(self, image, light_vector):
        pass

def convert(im):
    d = im.convert('L').getdata()
    return numpy.array(d, dtype='float64').reshape(im.size[::-1]) / 255
    
def back(arr):
    ni = range(3)
    for i in ni:
        ni[i] = Image.fromarray((arr[i] * 255).astype('uint8'))

    return Image.merge('RGB', ni)

def main():
    t = time.time()

    im_files= {'left': "zombie-left.png",
               'right': "zombie-right.png",
               'top': "zombie-top.png",
               'bottom': "zombie-bottom.png"}
    
    sn = SpriteNormalMap()
    sn.create(im_files, depth=0.5)
    sn.save_image('result.png')
    

    t = time.time() - t
    print("Execution time: %0.3f s" % t)

if __name__ == '__main__':
    main()
