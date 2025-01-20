import subprocess

import click
import click_spinner

from src.api.api_client import APIClient
from src.api.auth_api import AuthAPI
from src.api.user_api import UserAPI

endpoint = AuthAPI(APIClient())
user_endpoint = UserAPI(APIClient())


@click.command()
@click.option("--email", prompt=True)
@click.option("--password", prompt=True, hide_input=True)
def login(email, password):
    """Login to the application."""
    with click_spinner.spinner():
        result = endpoint.login(email, password)
    if result["success"]:
        click.echo(f"Successfully logged in. {result['data']}")
        subprocess.run("quack", shell=True)
    else:
        click.echo(f"Login failed. {result['message']}")


@click.command()
def logout():
    """Logout from the application."""
    with click_spinner.spinner():
        result = endpoint.logout()
    if result:
        click.echo("Successfully logged out.")
    else:
        click.echo("No action taken. You were not logged in.")


@click.command()
@click.pass_context
@click.option("--username", prompt=True)
@click.option("--email", prompt=True)
@click.option("--password", prompt=True, hide_input=True)
def register(ctx, username, email, password):
    """Register with Duckington Labs."""
    with click_spinner.spinner():
        result = user_endpoint.register(username, email, password)
    if result["success"]:
        click.echo("Welcome to Duckington Labs, you've successfully registered as:")
        click.echo(f"  - Username: {result['data']['user_name']}")
        click.echo(f"  - Email: {result['data']['email']}")
        click.echo(f"  - User ID: {result['data']['user_id']}")
        ctx.invoke(login, email=email, password=password)
    else:
        click.echo(f"Login failed. {result['message']}")
