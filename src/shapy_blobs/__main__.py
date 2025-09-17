#!/usr/bin/env python3


import click
import pathlib

@click.group()
def greeting():
    print("starting pca analysis")

@greeting.command('generate-pca')
@click.argument('image_files', nargs=-1, type = click.Path())
@click.option('--output_name', default="pca_shape_mean.npz", type = click.Path(), help="name of resulting npz file")
@click.option('--components', default = 256, help = "number of components saved", type = int)
def generate_pca( image_files, output_name, components):
    """
        Loads IMAGE_FILES as zarr folders and performs a PCA on them.

    """
    from . import generate_pca
    generate_pca.main(image_files, output_name, n_components=components)

@greeting.command('fit-data')
@click.argument('component_file', nargs=1, type=click.Path())
@click.argument('image_file', nargs=1, type=click.Path())
@click.option("--output", default="partial_fit.npz", type=click.Path(), help="npz to save to")
def fit_data( component_file, image_file, output):
    """
        Loads the numpy npz COMPONENT_FILE to perform a partial pca fit on the provided
        image file, which needs to be a zarr folder.
    """
    from . import fit_data
    fit_data.main(component_file, image_file, output)

@greeting.command('plot-fit')
@click.argument('fit_file', nargs=1, type=click.Path())
@click.argument('regions', nargs=-1, type=click.INT)
def plot_fit( fit_file, regions):
    """
        Plots the numpy npz FIT_FILE. Adding REGIONS as a list of numbers separates the
    fit file into regions. Otherwise the whole dataset will be treated as one group.
    """
    from . import plot_fit
    p = pathlib.Path(fit_file)
    if p.is_dir():
        fit_files = [ i for i in p.glob("*.npz") ]
        plot_fit.main(fit_files, regions)
    else:
        plot_fit.main([fit_file], regions)

@greeting.command('component-images')
@click.argument('pca_file', nargs=1, type=click.Path())
@click.option('--output_file', type=click.Path(), default="pca_modes.zarr" )
@click.option('--n_components', type = int, default = 20 )
@click.option('--magnitude', type=float, default = 10, help="magnitude of variation")
def component_images( pca_file, output_file, n_components, magnitude):
    """
        Generates an image from the first n components found in the npz PCA_FILE.
    """
    from . import grab_mode
    grab_mode.main(pca_file, output_file=output_file, n_components=n_components, magnitude=magnitude)


if __name__=='__main__':
    greeting()
