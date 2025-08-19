#!/usr/bin/env python3


import click
import numpy


from crop_tools import getAttributeFileList

@click.group()
def greeting():
    print("mapping crops to meshes")

@greeting.command('crop-values')
@click.argument('fit_file', nargs=1, type = click.Path())
@click.argument('attribute_folder', type = click.Path())
@click.option('--output', type=click.Path(), default="results.txt")
def crop_values( fit_file, attribute_folder, output):
    """
        This will load the fit file, and the associated "attributes folder" then it will
        write values to a single tsv.

    """
    loaded = numpy.load( open(fit_file, 'rb') )
    for item in loaded:
        print(item)
    fits = loaded["arr_0"]
    attribute_files = getAttributeFileList( attribute_folder )
    dex = 0
    with open("results.txt", 'w') as rf:
        for frame, fname in attribute_files:
            lines = []
            with open(fname, 'r') as attrs:
                lines = [line.split("\t") for line in attrs]

            for line in lines:
                row = fits[dex]
                values = [frame, line[0], *line[4:7], *row[0:16]]
                to_write = "\t".join( "%s"%v for v in values )
                rf.write("%s\n"%to_write)
                dex += 1


if __name__=='__main__':
    greeting()
