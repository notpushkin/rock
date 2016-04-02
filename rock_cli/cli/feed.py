import click
from tabulate import tabulate

from ..globals import rocket, handle_error

@click.command("feed")
def cmd_feed():
    """
    Показывает последние операции в ленте.
    """
    r = rocket.operations.cool_feed.get()
    r = handle_error(r)
    j = r.json()

    lines = []

    for date, operations in sorted(list(j["dates"].items())):
        lines += [[
            click.style("===== %s =====" % date, fg="blue", bold=True),
            None, None, None
        ]] + [[
            op["merchant"]["name"],
            "",
            op["display_money"]["amount"],
            op["display_money"]["currency_code"],
        ] for op in reversed(operations)] + [[
            None, None, None, None
        ]]

    click.echo(tabulate(lines, tablefmt="plain"))
