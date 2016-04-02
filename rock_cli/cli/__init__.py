import click
from ..util import OrderedGroup

@click.group(cls=OrderedGroup, context_settings={
    "help_option_names": ["-h", "--help"],
})
@click.option("-v", "--verbose", count=True)
def cli(verbose):
    """
    Консольный клиент для Рокетбанка.
    """
    pass

from .register import cmd_register
cli.add_command(cmd_register)

from .balance import cmd_balance
cli.add_command(cmd_balance)

from .feed import cmd_feed
cli.add_command(cmd_feed)

from .transfer import cmd_transfer
cli.add_command(cmd_transfer)

from .tariffs import cmd_tariffs
cli.add_command(cmd_tariffs)

from .repl import cmd_repl
cli.add_command(cmd_repl)

from .version import cmd_version
cli.add_command(cmd_version)
