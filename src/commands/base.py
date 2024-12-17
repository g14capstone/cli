import click

from src.api.api_client import APIClient
from src.api.auth_api import AuthAPI

endpoint = AuthAPI(APIClient())


@click.command()
@click.option("--email", prompt=True)
@click.option("--password", prompt=True, hide_input=True)
def login(email, password):
    """Login to the application."""
    result = endpoint.login(email, password)
    if result["success"]:
        click.echo(f"Successfully logged in. {result['data']}")
    else:
        click.echo(f"Login failed. {result['message']}")


@click.command()
@click.pass_context
def logout(ctx):
    """Logout from the application."""
    result = endpoint.logout()
    if result:
        click.echo("Successfully logged out.")
    else:
        click.echo("No action taken. You were not logged in.")
