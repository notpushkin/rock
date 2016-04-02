import click

from ..globals import rocket, handle_error

@click.command("balance")
def cmd_balance():
    """
    Посмотреть баланс основного счёта.
    """
    r = rocket.operations.cool_feed.get(params={"per_page": 1})
    r = handle_error(r)
    j = r.json()

    template = "".join([
        click.style("{rur} {code}, ", fg="green", bold=True),
        "{miles} рокетрублей"])
    click.echo(template.format(
        rur=j["balance"]["amount"],
        code=j["balance"]["currency_code"],
        miles=int(j["miles"])))
