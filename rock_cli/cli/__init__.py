import click

@click.group(context_settings={
    "help_option_names": ["-h", "--help"],
})
@click.option("-v", "--verbose", count=True)
def cli(verbose):
    """
    Консольный клиент для Рокетбанка.
    """
    pass

from .balance import cmd_balance
cli.add_command(cmd_balance)

from .feed import cmd_feed
cli.add_command(cmd_feed)

from .register import cmd_register
cli.add_command(cmd_register)

from .repl import cmd_repl
cli.add_command(cmd_repl)

from .tariffs import cmd_tariffs
cli.add_command(cmd_tariffs)

from .transfer import cmd_transfer
cli.add_command(cmd_transfer)

from .version import cmd_version
cli.add_command(cmd_version)
