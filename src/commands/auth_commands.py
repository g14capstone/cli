import click
from src.commands.base import BaseCommand
from src.api.client import APIClient


class LoginCommand(BaseCommand):
    def execute(self, email, password):
        client = APIClient()
        result = client.auth.login(email, password)
        if result.get("access_token"):
            print(f"Successfully logged in. Token: {result['access_token']}")
        else:
            print("Login failed.")


@click.command()
@click.option("--email", prompt=True)
@click.option("--password", prompt=True, hide_input=True)
@click.pass_context
def login(ctx, email, password):
    cmd = LoginCommand()
    cmd.execute(email, password)


class LogoutCommand(BaseCommand):
    def execute(self):
        client = APIClient()
        result = client.auth.logout()
        if result.get("success"):
            print("Successfully logged out.")
        else:
            print("Logout failed.")


@click.command()
@click.pass_context
def logout(ctx):
    cmd = LogoutCommand()
    cmd.execute()
