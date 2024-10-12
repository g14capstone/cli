import click
from src.commands.base import BaseCommand
from src.api.client import APIClient
from src.api.auth_api import AuthAPI
from src.utils.helpers.validity_enum import ValidityEnum


class LoginCommand(BaseCommand):
    def execute(self, email, password):
        client = APIClient()
        endpoint = AuthAPI(client)
        result = endpoint.login(email, password)
        if result["success"]:
            print(f"Successfully logged in. {result['data']}")
        else:
            print(f"Login failed. {result['message']}")


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
        endpoint = AuthAPI(client)
        logout_result = endpoint.logout()

        if logout_result:
            print("Successfully logged out.")
        else:
            print("No action taken. You were not logged in.")

        return logout_result


@click.command()
@click.pass_context
def logout(ctx):
    cmd = LogoutCommand()
    cmd.execute()


class CreateAPIKeyCommand(BaseCommand):
    def execute(self, validity):
        client = APIClient()
        endpoint = AuthAPI(client)
        result = endpoint.create_api_key(ValidityEnum[validity])
        if result["success"]:
            print(f"API key created successfully: {result['data']}")
        else:
            print(f"Failed to create API key. {result['message']}")


@click.command()
@click.option(
    "--validity",
    type=click.Choice(["ONE_HOUR", "ONE_DAY", "ONE_WEEK", "ONE_MONTH", "ONE_YEAR"]),
    prompt=True,
)
@click.pass_context
def create_api_key(ctx, validity):
    cmd = CreateAPIKeyCommand()
    cmd.execute(validity)


class ListAPIKeysCommand(BaseCommand):
    def execute(self):
        client = APIClient()
        endpoint = AuthAPI(client)
        result = endpoint.list_api_keys()
        if result["success"]:
            print("API Keys:")
            for key in result["data"]:
                print(
                    f"Token: {key['token']}, Created At: {key['created_at']}, Validity: {key['validity']}"
                )
        else:
            print(f"Failed to retrieve API keys. {result['message']}")


@click.command()
@click.pass_context
def list_api_keys(ctx):
    cmd = ListAPIKeysCommand()
    cmd.execute()


class DeleteAPIKeyCommand(BaseCommand):
    def execute(self, token):
        client = APIClient()
        endpoint = AuthAPI(client)
        result = endpoint.delete_api_key(token)
        if result["success"]:
            print(f"API key deleted successfully. {result['data']}")
        else:
            print(f"Failed to delete API key. {result['message']}")


@click.command()
@click.option("--token", prompt=True)
@click.pass_context
def delete_api_key(ctx, token):
    cmd = DeleteAPIKeyCommand()
    cmd.execute(token)


class SetAPIKeyCommand(BaseCommand):
    def execute(self, api_key):
        client = APIClient()
        endpoint = AuthAPI(client)
        result = endpoint.set_api_key(api_key)
        if result:
            print("API key set successfully.")


@click.command()
@click.option("--api-key", prompt=True, hide_input=True)
@click.pass_context
def set_api_key(ctx, api_key):
    cmd = SetAPIKeyCommand()
    cmd.execute(api_key)


class RemoveAPIKeyCommand(BaseCommand):
    def execute(self):
        client = APIClient()
        endpoint = AuthAPI(client)
        result = endpoint.clear_api_key()
        if result:
            print("API key removed successfully.")
        else:
            print("No API key was set.")


@click.command()
@click.pass_context
def remove_api_key(ctx):
    cmd = RemoveAPIKeyCommand()
    cmd.execute()
