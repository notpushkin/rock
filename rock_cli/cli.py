import os
import sys

import click
from yamlcfg import YAMLConfig

from tabulate import tabulate

from .rocket import Rocket
from .util import SuperDict

from . import __version__
from .rocket import API_VERSION

APP_NAME = "rock-cli"
CONTEXT_SETTINGS = {
    "help_option_names": ["-h", "--help"],
}

g = SuperDict()


def do_login(password=None):
    email = g.config.email
    if not email:
        click.secho("Похоже, вы не авторизовывались с этого компьютера.",
                    fg="red", bold=True)
        click.echo("Для авторизации выполните:")
        click.echo("    rock register")
        return

    if not password:
        password = click.prompt("Введите рокеткод", hide_input=True)

    r = g.rocket.login.get(json={
        "email": email,
        "password": password
    })

    if r.status_code >= 400:
        return handle_error(r)

    j = r.json()
    g.config.token = j["token"]
    g.config.write()

    g.rocket.set_token(j["token"])
    return j


def handle_error(r):
    if r.status_code >= 400:
        resp = r.json()["response"]

        if resp["show_it"]:
            click.secho(resp["description"], fg="red")

        if resp["code"] == "INCORRECT_TOKEN":
            do_login()
            req = r.request.copy()
            req.prepare_auth(g.rocket.session.auth)
            return g.rocket.send(req)
        else:
            sys.exit(1)


@click.group(context_settings=CONTEXT_SETTINGS)
@click.option("-v", "--verbose", count=True)
def cli(verbose):
    """
    Консольный клиент для Рокетбанка.
    """

    os.makedirs(click.get_app_dir(APP_NAME), exist_ok=True)
    g.config = YAMLConfig(
        paths=[os.path.join(click.get_app_dir(APP_NAME), "config.yml")])

    if g.config.device_id is None:
        g.config.device_id = Rocket.generate_id("ROCKCLI")
        g.config.write()

    g.rocket = Rocket(
        device_id=g.config.device_id,
        token=g.config.token,
        user_agent="rock-cli/%s (ale@songbee.net)" % __version__)


@cli.command()
@click.argument("phone", required=False)
def register(phone):
    if phone is None:
        phone = click.prompt("Номер телефона")

    r = g.rocket.devices.register.post(data={"phone": phone})
    r = handle_error(r)

    id = r.json()["sms_verification"]["id"]
    code = click.prompt("Введите код из SMS", type=int)

    r = g.rocket.sms_verifications[id]["verify"].patch(data={"code": code})
    r = handle_error(r)
    j = r.json()

    click.secho("Добро пожаловать, {}!".format(j["user"]["first_name"]), fg="green")

    g.config.email = j["user"]["email"]
    g.config.write()


@cli.command()
@click.option("--password", hide_input=True)
def login(password=None):
    click.secho("Теперь rock сам спрашивает рокеткод при необходимости. "
                "Больше не надо выполнять `rock login` каждый раз, ура!",
                fg="yellow")


@cli.command()
def tariffs():
    """
    Посмотреть список тарифов.
    """
    r = g.rocket.tariffs.get()
    r = handle_error(r)

    for tariff in r.json():
        click.echo("- {name} <{url}>".format(
            name=click.style(tariff["name"], fg="green", bold=True),
            url=tariff["url"]))

@cli.command()
def balance():
    """
    Посмотреть баланс основного счёта.
    """
    r = g.rocket.operations.cool_feed.get(params={"per_page": 1})
    r = handle_error(r)
    j = r.json()

    template = "".join([
        click.style("{rur} {code}, ", fg="green", bold=True),
        "{miles} рокетрублей"])
    click.echo(template.format(
        rur=j["balance"]["amount"],
        code=j["balance"]["currency_code"],
        miles=int(j["miles"])))

@cli.command()
def feed():
    """
    Показывает последние операции в ленте.
    """
    r = g.rocket.operations.cool_feed.get()
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


@cli.command()
@click.option("--recipient", prompt="Получатель",
              metavar="<4242424242424242>", help="Номер карты получателя")
@click.option("--amount", prompt="Сумма (в рублях)",
              metavar="<10>", help="Сумма перевода в рублях")
def transfer(recipient, amount):
    """
    Перевести деньги на номер карты.
    """
    r = g.rocket.card2card.transfer.post(params={
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


@cli.command()
def repl():
    """
    Запускает интерпретатор Python с подключенной обёрткой API Рокетбанка.
    """
    import code
    import rlcompleter  # noqa
    import readline
    import sys

    readline.parse_and_bind("tab: complete")
    shell = code.InteractiveConsole(g)
    shell.interact(banner="rock-cli %s, Python %s on %s" %
                          (__version__, sys.version, sys.platform))


@cli.command()
def version():
    """
    Выводит номер версии приложения.
    """
    click.echo("rock-cli %s" % __version__)
    click.echo("Using Rocketbank API v%s" % API_VERSION)
