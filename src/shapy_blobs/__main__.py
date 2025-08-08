#!/usr/bin/env python3


import click

@click.group()
def greeting():
    print("starting pca analysis")

@greeting.command('generate-pca')
@click.argument('filename', nargs=-1, required=True)
@click.option('--output_name', default="pca_shape_mean.npz")
def generate_pca( image_files, output_name):
    from . import generate_pca
    generate_pca.main(image_files, output_name)

@greeting.command('fit-data')
@click.argument('component_file', nargs=1, required=True)
@click.argument('image_file', nargs=1, required=True)
@click.option("--output", default="partial_fit.npz")
def fit_data( component_file, image_file, output):
    from . import fit_data
    fit_data.main(component_file, image_file, output)

@greeting.command('plot-fit')
@click.argument('fit_file', nargs=1)
@click.argument('regions', nargs=-1, type=click.INT)
def plot_fit( fit_file, regions):
    from . import plot_fit
    plot_fit.main(fit_file, regions)

if __name__=='__main__':
    greeting()
