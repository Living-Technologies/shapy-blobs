#!/usr/bin/env python3

import numpy, sys
import sklearn
from matplotlib import pyplot
import ngff_zarr
from shapy_blobs import SHAPE_KEY, MEAN_KEY

def pcaData(data, n_components=256):
    pca  = sklearn.decomposition.PCA(n_components=n_components)
    pca = pca.fit(data)
    return pca

if __name__=="__main__":
    lin = None
    for img_pth in sys.argv[1:]:
        img = ngff_zarr.from_ngff_zarr(img_pth).images[0]
        data = img.data
        n = 1
        print(data.shape)
        for s in data.shape[1:]:
            n = n*s
        rs = data.reshape((data.shape[0], n))
        if lin is None:
            lin = rs
        else:
            lin = numpy.concatenate( (lin, rs), axis=0 )

    shape_pca = pcaData( lin )

    shape_ave = shape_pca.mean_
    shape_comps = shape_pca.components_
    data = {SHAPE_KEY : shape_comps, MEAN_KEY : shape_ave}
    fname = "pca_shape_mean.npz"
    print("saving to %s"%fname)
    numpy.savez( fname, **data )

