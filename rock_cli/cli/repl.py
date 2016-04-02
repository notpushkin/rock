import click

from .. import APP_NAME, __version__
from ..globals import rocket

@click.command("repl")
def cmd_repl():
    """
    Запускает интерпретатор Python с подключенной обёрткой API Рокетбанка.
    """
    import code
    import rlcompleter  # noqa
    import readline
    import sys

    readline.parse_and_bind("tab: complete")
    shell = code.InteractiveConsole({
        "rocket": rocket,
    })
    shell.interact(banner="%s %s, Python %s on %s" %
                          (APP_NAME, __version__, sys.version, sys.platform))
