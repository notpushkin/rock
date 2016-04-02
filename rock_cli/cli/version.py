import click

from .. import APP_NAME, __version__
from ..rocket import API_VERSION

@click.command("version")
def cmd_version():
    """
    Выводит номер версии приложения.
    """
    click.echo("%s %s" % (APP_NAME, __version__))
    click.echo("Using Rocketbank API v%s" % API_VERSION)
