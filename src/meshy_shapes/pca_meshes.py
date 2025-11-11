import struct
import sklearn
from shapy_blobs import SHAPE_KEY, MEAN_KEY
import numpy
import math
import binarymeshformat as bmf
from shapy_blobs.fit_data import loadPCAFitter

def loadMeshFile( mesh_file ):
    with open(mesh_file, 'rb') as opend:
        n = opend.read(4)
        n_indexes = struct.unpack_from(">i", n, 0)[0]
        n_bytes = n_indexes*4
        tindexes = struct.unpack_from(">%si"%n_indexes, opend.read(n_bytes), 0)

        n = opend.read(4)
        n_indexes = struct.unpack_from(">i", n, 0)[0]
        n_bytes = n_indexes*4
        cindexes = struct.unpack_from(">%si"%n_indexes, opend.read(n_bytes), 0)

        n = opend.read(4)
        values = []

        frame = 0
        while len(n) == 4:
            n_floats = struct.unpack_from(">i", n, 0)[0]
            n_bytes = n_floats*8
            f_bytes = opend.read(n_bytes)
            if len(f_bytes) != n_bytes:
                print("final mesh truncated!")
                break
            positions = struct.unpack_from(">%sd"%n_floats, f_bytes, 0)
            if any( math.isnan(x) for x in positions ):
                print(frame, "broken mesh")
            else:
                values.append(numpy.array(positions))
            n = opend.read(4)
            frame += 1

        return {"triangles" : tindexes,"connections":cindexes}, numpy.array(values)

def loadTopology( mesh_file ):
    with open(mesh_file, 'rb') as opend:
        n = opend.read(4)
        n_indexes = struct.unpack_from(">i", n, 0)[0]
        n_bytes = n_indexes*4
        tindexes = struct.unpack_from(">%si"%n_indexes, opend.read(n_bytes), 0)

        n = opend.read(4)
        n_indexes = struct.unpack_from(">i", n, 0)[0]
        n_bytes = n_indexes*4
        cindexes = struct.unpack_from(">%si"%n_indexes, opend.read(n_bytes), 0)
    return {"triangles" : tindexes,"connections":cindexes}

def main( mesh_files, output_file, n_components=None ):
    values = None
    indexes = None
    for mesh_file in mesh_files:
        indexes, vi = loadMeshFile(mesh_file)
        if values is None:
            values = vi
        else:
            numpy.concatenate(values, vi, axis=0)

    data = values
    print("fitting data: ", data.shape)
    pca  = sklearn.decomposition.PCA(n_components=n_components)
    pca = pca.fit(data)
    shape_ave = pca.mean_
    shape_comps = pca.components_
    data = {SHAPE_KEY : shape_comps, MEAN_KEY : shape_ave}
    print("saving to %s"%output_file)

    numpy.savez( output_file, **data )


def fitPca( pca_file, quick_mesh_file, output, n_components):
    indexes, values = loadMeshFile(quick_mesh_file)
    print("loaded")
    all_values = numpy.array(values)

    print(all_values.shape)
    fitter = loadPCAFitter( pca_file )
    fits = []
    for i in range(0, all_values.shape[0], 100):
        fits.append( fitter.fit(all_values[i:i+100]) )
    print(len(fits), fits[0].shape, fits[1].shape)
    fin = numpy.concatenate( fits, axis=0 )
    print(fin.shape)
    print("saving to: ", output)
    numpy.savez(output, numpy.array(fin))

def saveModes(pca_file, quick_mesh_file, bmf_name, modes = 100):
    fitter = loadPCAFitter(pca_file)
    topo = loadTopology(quick_mesh_file)
    mesh = bmf.Mesh(fitter.mean, topo["connections"], topo["triangles"])
    track = bmf.Track("mean")
    track.addMesh( 0, mesh)
    plus = bmf.Track("plus")
    minus = bmf.Track("minus")
    for i in range(modes):
        mesh = bmf.Mesh(fitter.mean - fitter.shape[i], topo["connections"], topo["triangles"])
        minus.addMesh( i, mesh)
        mesh = bmf.Mesh(fitter.mean + fitter.shape[i], topo["connections"], topo["triangles"])
        plus.addMesh( i, mesh)


    bmf.saveMeshTracks( [track, plus, minus], bmf_name)

def extractMeshes( quick_mesh_file, bmf_name="extraction.bmf" ):
    topo, data = loadMeshFile(quick_mesh_file)
    print("loaded: ", data.shape[0])
    dex = 0
    suspect = range(64)
    track = bmf.Track("mean")
    for i in suspect:
        mesh = bmf.Mesh(data[i], topo["connections"], topo["triangles"])
        track.addMesh( dex, mesh)
        dex += 1
    bmf.saveMeshTracks( [track], bmf_name)

def reconstructMeshes( quick_mesh_file, pca_file, fits_file, bmf_name="reconstructed.bmf", modes=8):
    topo = loadTopology(quick_mesh_file)
    fitter = loadPCAFitter(pca_file)
    loaded = numpy.load( open(fits_file, 'rb') )
    fits = loaded["arr_0"]
    track = bmf.Track("reconstructed")
    for m in range(64):
        fit = fits[m]
        construct = numpy.zeros( fitter.mean.shape ) + fitter.mean
        for i in range(modes):
            construct += fitter.shape[i]*fit[i]
        mesh = bmf.Mesh(construct, topo["connections"], topo["triangles"])
        track.addMesh(m, mesh)
    bmf.saveMeshTracks( [track], bmf_name)
