import click
from src.api.machine_api import MachineAPI


class MachineCommands:
    def __init__(self):
        self.endpoint = MachineAPI()

    def create(self, machine_name, machine_type):
        click.echo("\nAttempting to create machine...\n")
        result = self.endpoint.create_machine(machine_name, machine_type)
        if result["success"]:
            click.echo(f"Machine created successfully. Details: {result['data']}")
        else:
            click.echo(
                "Failed to create machine. Check machine name and type and try again."
            )

    def list(self):
        result = self.endpoint.list_user_machines()
        if result["success"]:
            if not result["data"]:
                click.echo("No machines to list.")
                return
            click.echo("Machines:")
            for machine in result["data"]:
                click.echo(machine)
            return result
        else:
            click.echo("Failed to retrieve list of machines.")

    def stop(self, machine_id):
        click.echo("\nAttempting to stop machine...\n")
        result = self.endpoint.stop_machine(machine_id)
        if result["success"]:
            click.echo(f"{result['data']['message']}")
        else:
            click.echo("Failed to stop machine. Check machine ID and try again.")

    def start(self, machine_id):
        click.echo("\nAttempting to start machine...\n")
        result = self.endpoint.start_machine(machine_id)
        if result["success"]:
            click.echo(f"{result['data']['message']}")
        else:
            click.echo("Failed to start machine. Check machine ID and try again.")

    def terminate(self, machine_id):
        click.echo("\nAttempting to terminate machine...\n")
        result = self.endpoint.terminate_machine(machine_id)
        if result["success"]:
            click.echo(f"{result['data']['message']}")
        else:
            click.echo("Failed to terminate machine. Check machine ID and try again.")

    def get_details(self, machine_id):
        result = self.endpoint.get_machine(machine_id)
        if result["success"]:
            click.echo(f"Machine {machine_id} details:")
            click.echo(result["data"])
            return result["data"]
        else:
            click.echo("Failed to get machine. Check machine ID and try again.")


@click.group()
@click.pass_context
def machine(ctx):
    """Machine management commands."""
    ctx.obj = MachineCommands()


@machine.command()
@click.pass_context
@click.option("--machine-name", "-n", required=True, prompt="Enter machine name")
@click.option(
    "--machine-type",
    "-t",
    required=True,
    prompt="Choose machine type",
    type=click.Choice(["t2.micro", "f1.2xlarge", "f1.4xlarge", "f1.16xlarge"]),
    default="f1.2xlarge",
    show_default=True,
)
def create(ctx, machine_name, machine_type):
    """Create a machine with name and type."""
    ctx.obj.create(machine_name=machine_name, machine_type=machine_type)


@machine.command()
@click.pass_context
def list(ctx):
    """List all machines assigned to user."""
    ctx.obj.list()


@machine.command()
@click.option("--machine-id", "-id", required=True, prompt="Enter machine ID")
@click.pass_context
def stop(ctx, machine_id):
    """Stop machine with machine ID."""
    ctx.obj.stop(machine_id)


@machine.command()
@click.option("--machine-id", "-id", required=True, prompt="Enter machine ID")
@click.pass_context
def start(ctx, machine_id):
    """Start machine with machine ID."""
    ctx.obj.start(machine_id)


@machine.command()
@click.option("--machine-id", "-id", required=True, prompt="Enter machine ID")
@click.pass_context
def terminate(ctx, machine_id):
    """Terminate machine with machine ID."""
    ctx.obj.terminate(machine_id)


@machine.command()
@click.option("--machine-id", "-id", required=True, prompt="Enter machine ID")
@click.pass_context
def details(ctx, machine_id):
    """Get machine details with machine ID."""
    ctx.obj.get_details(machine_id)
