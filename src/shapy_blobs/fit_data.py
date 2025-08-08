#!/usr/bin/env python3

import sys, pathlib
import numpy
import ngff_zarr

from shapy_blobs import SHAPE_KEY, MEAN_KEY

class PartialPCA:
    def __init__(self, mean, shape):
        self.mean = mean
        self.shape = shape
    def fit(self, data):
        """

        """
        delta = data - self.mean

        y = numpy.zeros( (data.shape[0], self.shape.shape[0]) )
        for i, comp in enumerate(self.shape):
            dots = numpy.sum(comp*delta, axis=1)
            y[:, i] = dots
        return y

def getPCA(pth):
    opened = numpy.load(pth)
    mean = opened[MEAN_KEY]
    shape = opened[SHAPE_KEY]
    return mean, shape

def main( shape_path, image_path , output_path="part_fit.npz"):
    mean, shape = getPCA( shape_path )
    print("fitting mean %s with components %s"%( mean.shape, shape.shape) )

    img = ngff_zarr.from_ngff_zarr(image_path).images[0]

    data = img.data
    print(" to transform %s"%( data.shape,  ) )
    n = 1
    for s in data.shape[1:]:
        n = n*s
    rs = data.reshape((data.shape[0], n))
    out = numpy.zeros((rs.shape[0], shape.shape[0]))
    ppca = PartialPCA(mean, shape)
    value = ppca.fit(rs)
    print(value.shape)
    print("saving to: ", output_path)
    numpy.savez(output_path, value)

if __name__=="__main__":
    main(sys.argv[1], sys.argv[2])
