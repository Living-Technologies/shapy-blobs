import numpy

SHAPE_KEY="shape"
MEAN_KEY="mean"

def getPCA(pth):
    """
       Loads a .npz file which should contain to arrays saved with
        the package described keys.
    """
    opened = numpy.load(pth)
    mean = opened[MEAN_KEY]
    shape = opened[SHAPE_KEY]
    return mean, shape
