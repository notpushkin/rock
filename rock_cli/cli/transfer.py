import click

from ..globals import rocket, handle_error

@click.command("transfer")
@click.option("--recipient", prompt="Получатель",
              metavar="<4242424242424242>", help="Номер карты получателя")
@click.option("--amount", prompt="Сумма (в рублях)",
              metavar="<10>", help="Сумма перевода в рублях")
def cmd_transfer(recipient, amount):
    """
    Перевести деньги на номер карты.
    """
    r = rocket.card2card.transfer.post(params={
        "source_card": recipient,
        "amount": amount
    })
    r = handle_error(r)
    j = r.json()

    if j["status"] == "approved":
        template = "".join([
            click.style("Платёж принят! ", fg="green", bold=True),
            "Остаток: {rur} рублей"])
        click.echo(template.format(rur=j["balance"]))
    else:
        click.secho(j["errors"], fg="red", bold=True)
