import os
import sys
import click
from yamlcfg import YAMLConfig

from .rocket import Rocket
from . import APP_NAME, __version__

os.makedirs(click.get_app_dir(APP_NAME), exist_ok=True)
config = YAMLConfig(
    paths=[os.path.join(click.get_app_dir(APP_NAME), "config.yml")])

if config.device_id is None:
    config.device_id = Rocket.generate_id("ROCKCLI")
    config.write()

rocket = Rocket(
    device_id=config.device_id,
    token=config.token,
    user_agent="rock-cli/%s (ale@songbee.net)" % __version__)

def do_login(password=None):
    email = config.email
    if not email:
        click.secho("Похоже, вы не авторизовывались с этого компьютера.",
                    fg="red", bold=True)
        click.echo("Для авторизации выполните:")
        click.echo("    rock register")
        sys.exit(1)

    if not password:
        password = click.prompt("Введите рокеткод", hide_input=True)

    r = rocket.login.get(json={
        "email": email,
        "password": password
    })

    if r.status_code >= 400:
        return handle_error(r)

    j = r.json()
    config.token = j["token"]
    config.write()

    rocket.set_token(j["token"])
    return j


def handle_error(r):
    if r.status_code >= 400:
        resp = r.json()["response"]

        if resp["show_it"]:
            click.secho(resp["description"], fg="red")

        if resp["code"] == "INCORRECT_TOKEN":
            do_login()
            req = r.request.copy()
            req.prepare_auth(rocket.session.auth)
            return rocket.send(req)
        else:
            sys.exit(1)

    return r
