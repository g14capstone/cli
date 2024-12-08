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
        print(f"Successfully logged in. {result['data']}")
    else:
        print(f"Login failed. {result['message']}")


@click.command()
@click.pass_context
def logout(ctx):
    """Logout from the application."""
    result = endpoint.logout()
    if result:
        print("Successfully logged out.")
    else:
        print("No action taken. You were not logged in.")
