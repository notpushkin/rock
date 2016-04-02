import click

from ..globals import rocket, handle_error

@click.command("tariffs")
def cmd_tariffs():
    """
    Посмотреть список тарифов.
    """
    r = rocket.tariffs.get()
    r = handle_error(r)

    for tariff in r.json():
        click.echo("- {name} <{url}>".format(
            name=click.style(tariff["name"], fg="green", bold=True),
            url=tariff["url"]))
