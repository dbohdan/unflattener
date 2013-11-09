#!/usr/bin/env python
import Image
import numpy
import time

t = time.time()

def convert(im):
    d = im.convert('L').getdata()
    return numpy.array(d, dtype='float64').reshape(im.size, order='F') / 255

fn = "zombie"
image_types = "left", "right", "top", "bottom"
images = {}

imgshape = None
for imagefile in image_types:
    im = Image.open("%s-%s.png" % (fn, imagefile))
    images[imagefile] = convert(im)
    # Check if all images are the same size
    if not imgshape:
        imgshape = images[imagefile].shape
    else:
        if imgshape != images[imagefile].shape:
            raise EValueError

a = numpy.zeros((3, imgshape[0], imgshape[1]), dtype='float64')
#print(images['top'].shape, a.shape)

a[0] = images['right'] - images['left'] # x_N
a[1] = images['top'] - images['bottom'] # y_N
a[2] = 1.0

norm = a[0] * a[0] + a[1] * a[1]
it = numpy.nditer(a[2], flags=['multi_index'])
while not it.finished:
    #print it, it.multi_index, it[0]
    n = norm[it.multi_index]
    #print it.multi_index, n
    if n > 0:
        a[2][it.multi_index] = numpy.sqrt(max(1 - n / numpy.sqrt(n), 0))
    it.iternext()
                          
for i in range(3):
    print a[i].min(), a[i].max()
print a[:, 0, 0]

aim = a.copy()
aim[0] = (a[0] + 1) / 2
aim[1] = (a[1] + 1) / 2
aim *= 255
aim = aim.astype('uint8')
print aim[:, 0, 0]

for i in range(3):
    print aim[i].min(), aim[i].max()

normal_map = Image.new('RGB', imgshape)
for i in range(a.shape[1]):
    for j in range(a.shape[2]):
        #print aim[:, i, j]
        normal_map.putpixel((i, j), tuple(aim[:, i, j]))
normal_map.save('result.png')

t = time.time() - t
print("Execution time: %0.3f s" % t)
