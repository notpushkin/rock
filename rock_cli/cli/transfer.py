import click
from time import sleep

from ..globals import rocket, handle_error

def transfer_to_card(recipient, amount):
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


def transfer_to_phone(recipient, amount):
    click.secho("Перевод по номеру телефона пока не поддерживается",
                fg="red", bold=True)
    contact_id = 10042
    r = rocket.contacts.sync.post(json={
        "contacts": [{
            "contact_id": contact_id,
            "Email": [],
            "name": "__rock-cli_tmp__",
            "Phone": [recipient]
        }]
    })
    r = handle_error(r)
    j = r.json()

    if len(j["contacts"]) == 0:
        click.secho("Этого человека ещё нет в Рокетбанке :(",
                    fg="yellow", bold=True)
    else:
        sleep(1)
        r = rocket.friend_transfers.post(json={
            "amount": int(amount),
            "comment": "https://github.com/iamale/rock",
            "user_id": contact_id
        })
        r = handle_error(r)
        click.secho("Всё ок, деньги переведены! :)",
                    fg="green")


@click.command("transfer")
@click.option("--recipient", prompt="Получатель (телефон/карта)",
              help="Номер карты или телефона получателя")
@click.option("--amount", prompt="Сумма (в рублях)",
              help="Сумма перевода в рублях")
def cmd_transfer(recipient, amount):
    """
    Перевести деньги на номер карты.
    """
    recipient = "".join(_ for _ in recipient if _ in "+0123456789")

    if recipient.startswith("+") or len(recipient) < 16:
        transfer_to_phone(recipient, amount)
    else:
        transfer_to_card(recipient, amount)
