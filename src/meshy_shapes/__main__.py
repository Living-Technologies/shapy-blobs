import click

@click.group()
def greeting():
    print("mesh based pca")


@greeting.command('pca-meshes')
@click.argument('mesh_files', nargs=-1, type = click.Path())
@click.option('--output', default="pca_shape_mean.npz", type = click.Path(), help="name of resulting npz file")
@click.option('--components', default = None, help = "number of components saved", type = int)
def pca_meshes( mesh_files, output, components):
    """
        Loads IMAGE_FILES as zarr folders and performs a PCA on them.

    """
    from . import pca_meshes
    pca_meshes.main(mesh_files, output, n_components=components)

@greeting.command('fit-meshes')
@click.argument('pca_file', nargs=1, type = click.Path())
@click.argument('mesh_file', nargs=1, type = click.Path())
@click.option('--output', default="fit-mesh-based.npz", type = click.Path(), help="name of resulting npz file")
@click.option('--components', default = None, help = "number of components saved", type = int)
def fit_meshes( pca_file, mesh_file, output, components):
    """
        Loads IMAGE_FILES as zarr folders and performs a PCA on them.

    """
    from . import pca_meshes
    pca_meshes.fitPca(pca_file, mesh_file, output, components)

@greeting.command('save-modes')
@click.argument('pca_file', nargs=1, type = click.Path())
@click.argument('mesh_file', nargs=1, type = click.Path())
@click.option('--output', default="pca-modes.bmf", type = click.Path(), help="name of resulting bmf file")
@click.option('--modes', default = 100, help = "number of modes to save", type = int)
def save_modes( pca_file, mesh_file, output, modes):
    """
        Generates meshes to represent the PCA_FILE modes
    """
    from . import pca_meshes
    pca_meshes.saveModes(pca_file, mesh_file, output, modes)


if __name__=='__main__':
    greeting()
