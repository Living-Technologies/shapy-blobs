#!/usr/bin/env python3

import numpy
import skimage

from shapy_blobs import getPCA

def main(pca_file, output_file = "pca_modes.tif", magnitude = 10, n_components = 20):

    every = []
    mean, comps = getPCA(pca_file)
    print(comps.shape)
    for i in range(n_components):
        cA = numpy.reshape(comps[i], (48, 48, 48))
        low = -magnitude*cA
        high =  magnitude*cA
        row = [low, high]
        every.append(row)
    every = numpy.array(every)
    every = numpy.reshape(every, (every.shape[0], 2,  48, 48, 48))
    skimage.io.imsave(output_file, every )
