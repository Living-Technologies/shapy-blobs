#!/usr/bin/env python3

import numpy
import skimage
import ngff_zarr
import pathlib

from shapy_blobs import getPCA


def saveZarr(output_file, arr):
    dims = ["t", "c", "z", "y", "x"]
    scale = { "t":1, "c":1, "z":1, "y":1, "x":1 }
    translate = { "t":0, "c":0, "z":0, "y":0, "x":0 }
    img = ngff_zarr.ngff_image.NgffImage( arr, dims, scale=scale, translation=translate)
    multiscales = ngff_zarr.to_multiscales(img, scale_factors=[])
    ngff_zarr.to_ngff_zarr(output_file, multiscales, overwrite=True, version="0.4")

def saveSkio(output_file, arr):
    """
    """
    skimage.io.imsave(output_file, arr)

def saveImage(output_file, arr):
    """
    """
    if output_file.name.endswith(".zarr"):
        saveZarr(output_file, arr)
    else:
        saveSkio( output_file, arr)

def main(pca_file, output_file = "pca_modes.zarr", magnitude = 10, n_components = 20):
    every = []
    mean, comps = getPCA(pca_file)
    volume_shape = (48, 48, 48)
    mi = numpy.reshape( mean, volume_shape )


    for i in range(n_components + 1):
        if(i == 0):
            cA = numpy.reshape(mean, volume_shape)
        else:
            cA = numpy.reshape(comps[i-1], volume_shape)
        mn = numpy.min(cA);
        if mn > 0:
            mn = 0

        mx = numpy.max(cA);
        if mx < 0:
            mx = 0;
        factor = 1
        if mn > mx:
            factor = 1/mn
        else:
            factor = 1/mx

        low = cA*-1*factor
        low[numpy.where( low < 0 ) ] = 0
        high =  cA * 1*factor
        high[numpy.where(high < 0) ] = 0

        row = numpy.array([low, high], dtype="float32")
        every.append(row)
    every = numpy.array(every)
    print("saving to: ", output_file)
    saveImage(pathlib.Path(output_file), every )
