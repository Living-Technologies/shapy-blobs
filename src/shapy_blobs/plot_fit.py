#!/usr/bin/env python3

import numpy
from matplotlib import pyplot
import sys

def plotMagnitude(values):
    v2 = values*values
    v2 = numpy.sum(v2, axis=0)
    v2 = v2/values.shape[0]
    x = numpy.array([i for i in range( values.shape[1] ) ])
    pyplot.plot(x, v2)

def getHistogram( values ):
    hist, edges = numpy.histogram( values, bins=25 )
    mid = 0.5*(edges[1:] + edges[:-1])
    return mid, hist


def main( fit_files, regions=[] ):

    n, m = (4, 4)
    pyplot.style.use("dark_background")
    fig, axes = pyplot.subplots( n, m)
    fits = []
    files = []
    for fit_file in fit_files:

        loaded = numpy.load( open(fit_file, 'rb') )
        for item in loaded:
            print(item)
        fits.append(loaded["arr_0"])
        files.append( fits[-1].shape[0] )
        print("loaded shape", loaded["arr_0"].shape)

    fits = numpy.concatenate(fits, axis=0)
    for j, row in enumerate(fits):
        if row[3] > 5:
            print(j)

    print("final shape: ", fits.shape);
    pyplot.figure(0)
    plotMagnitude(fits)

    if len(regions)==0:
        regions = files
    else:
        t0 = 0
        for tr in regions:
            plotMagnitude( fits[t0:t0 + tr] )
            t0 += tr


    for i in range(n*m):
        j = i//m
        k = i%m
        axis = axes[j, k]

        t0 = 0
        for tr in regions:
            print(t0, tr)
            x, y = getHistogram(fits[t0:t0+tr, i])
            axis.plot(x, y, ".-", label="%s : %s, %s"%(i+1, t0, t0+tr))
            t0 += tr

    axis.legend()

    fig2, axes2 = pyplot.subplots( n, m)
    for i in range(n*m):
        j = i//m
        k = i%m
        axis = axes2[j, k]

        t0 = 0
        for tr in regions:
            print(t0, tr)
            y = fits[t0:t0+tr, 2*i]
            x = fits[t0:t0+tr, 2*i + 1]
            axis.plot(x, y, ".", label="%s : %s, %s"%(i+1, t0, t0+tr))
            t0 += tr

    axis.legend()
    pyplot.show()



if __name__=="__main__":
    if len(sys.argv) > 2:
        regions = [ int( region ) for region in sys.argv[2:]]
    else:
        regions = []
    main(sys.argv[1], regions)
