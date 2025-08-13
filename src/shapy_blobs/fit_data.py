#!/usr/bin/env python3

import sys, pathlib
import numpy
import ngff_zarr

from shapy_blobs import getPCA

class PartialPCA:
    def __init__(self, mean, shape):
        self.mean = mean
        self.shape = shape
    def fit(self, data):
        """
            Fits the provided data.

            TODO vectorize the calculation. This is incredibly slow.

        """
        delta = data - self.mean


        y1  = numpy.sum(
            numpy.reshape(delta, (delta.shape[0], 1, delta.shape[1]))*self.shape, axis=2
            )

        return y1

def main( shape_path, image_path , output_path="partialfit_fit.npz"):
    """
        Loads pca data and the image data as a zarr. Fits the data
    and then saves the resulting fit.
    """
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
