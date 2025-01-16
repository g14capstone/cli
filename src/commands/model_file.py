from datetime import datetime
import json

import click
import click_spinner

from src.api.api_client import APIClient
from src.api.model_file_api import ModelFileAPI
from src.utils.groups.subcommand_group import SubCommandGroup


class ModelFileCommands:
    def __init__(self):
        self.client = APIClient()
        self.endpoint = ModelFileAPI(self.client)

    def upload(
        self,
        file_path: str,
        model_name: str | None = None,
        model_id: str | None = None,
    ):
        click.echo("\nAttempting to upload model file...\n")
        with click_spinner.spinner():
            result = self.endpoint.upload_model_file(model_name, model_id, file_path)
        if result["success"]:
            upload_date = datetime.strptime(
                result["data"]["upload_date"], "%Y-%m-%dT%H:%M:%S.%f%z"
            )
            formatted_date = upload_date.astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")
            click.echo("Model file uploaded successfully:")
            click.echo(f"  Model Name: {result['data']['model_name']}")
            click.echo(f"  Model ID: {result['data']['model_id']}")
            click.echo(f"  Upload Date: {formatted_date}")
        else:
            click.echo(f"Failed to upload model file: {result['response']['detail']}")

    def list_default(self, file_path="src/models/default_models.json"):
        click.echo("Default Models:")
        with open(file_path, "r") as file:
            default_models = json.load(file)
            for model in default_models:
                click.echo(f"  Name: {model['name']}")
                click.echo(f"  Description: {model['description']}")
                click.echo("  Availability:")
                for key, value in model["available"].items():
                    click.echo(f"    • {key}: {'Yes' if value else 'No'}")

    def list(self):
        with click_spinner.spinner():
            result = self.endpoint.get_all_models()
        self.list_default()
        if result["success"]:
            if not result["data"]:
                click.echo("No models to list.")
                return
            click.echo("User Models:")
            for model in result["data"]:
                click.echo(f"  Name: {model['model_name']}")
                click.echo(f"  ID: {model['model_id']}")
                click.echo("  Files:")
                for file in model["files"]:
                    last_modified = datetime.strptime(
                        file["last_modified"], "%Y-%m-%dT%H:%M:%SZ"
                    )
                    last_modified = last_modified.astimezone().strftime(
                        "%Y-%m-%d %H:%M:%S %Z"
                    )
                    click.echo(
                        f"    • {file['file_name']} ({file['file_size']} bytes)\n\tlast modified: {last_modified}"
                    )
        else:
            click.echo(f"Failed to list models: {result['response']['detail']}")

    def get_model(self, model_id):
        with click_spinner.spinner():
            result = self.endpoint.get_model(model_id)
        if result["success"]:
            click.echo(f"Name: {result['data']['model_name']}")
            click.echo(f"ID: {result['data']['model_id']}")
            click.echo("Files:")
            for file in result["data"]["files"]:
                last_modified = datetime.strptime(
                    file["last_modified"], "%Y-%m-%dT%H:%M:%SZ"
                )
                last_modified = last_modified.astimezone().strftime(
                    "%Y-%m-%d %H:%M:%S %Z"
                )
                click.echo(f"  • {file['file_name']} ({file['file_size']} bytes)")
                click.echo(f"      last modified: {last_modified}")
        else:
            click.echo(f"Failed to get model. {result['response']['detail']}")

    def read_file(self, model_id, file_name):
        with click_spinner.spinner():
            result = self.endpoint.read_model_file(model_id, file_name)
        if result["success"]:
            click.echo(f"File contents for {file_name}:")
            click.echo(result["data"]["content"])
        else:
            click.echo(f"Failed to read model file. {result['response']['detail']}")

    def update(
        self,
        file_path: str,
        model_name: str | None = None,
        model_id: str | None = None,
    ):
        click.echo("\nAttempting to update model file...\n")
        with click_spinner.spinner():
            result = self.endpoint.update_model_file(
                model_name=model_name, model_id=model_id, file_path=file_path
            )
        if result["success"]:
            upload_date = datetime.strptime(
                result["data"]["upload_date"], "%Y-%m-%dT%H:%M:%S.%f%z"
            )
            formatted_date = upload_date.astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")
            click.echo("Model file uploaded successfully:")
            click.echo(f"  Model Name: {result['data']['model_name']}")
            click.echo(f"  Model ID: {result['data']['model_id']}")
            click.echo(f"  Upload Date: {formatted_date}")
        else:
            click.echo(f"Failed to upload model file: {result['response']['detail']}")

    def delete_file(self, model_id, file_name):
        click.echo("\nAttempting to delete model file...\n")
        with click_spinner.spinner():
            result = self.endpoint.delete_model_file(model_id, file_name)
        if result["success"] and result["data"] is None:
            click.echo(f"Model file {file_name} deleted successfully")
        else:
            click.echo(f"Failed to delete model file. {result['response']['detail']}")

    def delete_model(self, model_id):
        click.echo("\nAttempting to delete model...\n")
        with click_spinner.spinner():
            result = self.endpoint.delete_model(model_id)
        if result["success"] and result["data"] is None:
            click.echo(f"Model {model_id} deleted successfully")
        else:
            click.echo(f"Failed to delete model. {result['response']['detail']}")


@click.group(cls=SubCommandGroup)
@click.pass_context
def model(ctx):
    """Model file management commands."""
    ctx.obj = ModelFileCommands()


@model.command()
@click.pass_context
@click.option("--model-name", "-n", required=False)
@click.option("--model-id", "-id", required=False)
@click.option(
    "--file-path",
    "-f",
    required=True,
    prompt="Enter file path",
    type=click.Path(exists=True),
    shell_complete=click.Path().shell_complete,
)
def upload(ctx, model_name, model_id, file_path):
    """Upload a model file."""
    if not model_name and not model_id:
        model_name = click.prompt("Enter model name")
    ctx.obj.upload(model_name=model_name, model_id=model_id, file_path=file_path)


@model.command()
@click.pass_context
def list(ctx):
    """List all models."""
    ctx.obj.list()


@model.command()
@click.pass_context
@click.option("--model-id", "-id", required=True, prompt="Enter model ID")
def get(ctx, model_id):
    """Get model details with model ID."""
    ctx.obj.get_model(model_id)


@model.command()
@click.pass_context
@click.option("--model-id", "-id", required=True, prompt="Enter model ID")
@click.option("--file-name", "-f", required=True, prompt="Enter file name")
def read(ctx, model_id, file_name):
    """Read contents of a model file."""
    ctx.obj.read_file(model_id, file_name)


@model.command()
@click.pass_context
@click.option("--model-name", "-n", required=False)
@click.option("--model-id", "-id", required=False)
@click.option(
    "--file-path",
    "-f",
    required=True,
    prompt="Enter file path",
    type=click.Path(exists=True),
    shell_complete=click.Path().shell_complete,
)
def update(ctx, model_name, model_id, file_path):
    """Update a model file."""
    if not model_name and not model_id:
        model_name = click.prompt("Enter model name")
    ctx.obj.update(model_name=model_name, model_id=model_id, file_path=file_path)


@model.command()
@click.pass_context
@click.option("--model-id", "-id", required=True, prompt="Enter model ID")
@click.option("--file-name", "-f", required=True, prompt="Enter file name")
def delete_file(ctx, model_id, file_name):
    """Delete a model file."""
    ctx.obj.delete_file(model_id, file_name)


@model.command()
@click.pass_context
@click.option("--model-id", "-id", required=True, prompt="Enter model ID")
def delete(ctx, model_id):
    """Delete a model."""
    ctx.obj.delete_model(model_id)
