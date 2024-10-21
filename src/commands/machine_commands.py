import click

from src.api.machine_api import MachineAPI
from src.commands.base_command import BaseCommand


class CreateMachineCommand(BaseCommand):
    def execute(self, machine_name, machine_type):
        endpoint = MachineAPI()
        click.echo("\nAttempting to create machine...\n")
        result = endpoint.create_machine(machine_name, machine_type)
        if result["success"]:
            click.echo(f"Machine created successfully. Details: {result['data']}")
        else:
            click.echo(
                "Failed to create machine. Check machine name and type and try again."
            )


@click.command()
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
def create_machine(ctx, machine_name, machine_type):
    """Create a machine with name and type."""
    cmd = CreateMachineCommand()
    cmd.execute(machine_name=machine_name, machine_type=machine_type)


class ListMachinesCommand(BaseCommand):
    def execute(self):
        endpoint = MachineAPI()
        result = endpoint.list_user_machines()

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


@click.command()
@click.pass_context
def list_machines(ctx):
    """List all machines assigned to user."""
    cmd = ListMachinesCommand()
    cmd.execute()


class StopMachine(BaseCommand):
    def execute(self, machine_id):
        endpoint = MachineAPI()

        click.echo("\nAttempting to stop machine...\n")
        result = endpoint.stop_machine(machine_id)

        if result["success"]:
            click.echo(f"{result['data']['message']}")
        else:
            click.echo("Failed to stop machine. Check machine ID and try again.")


@click.command()
@click.option("--machine-id", "-id", required=True, prompt="Enter machine ID")
@click.pass_context
def stop_machine(ctx, machine_id):
    """Stop machine with machine ID."""
    cmd = StopMachine()
    cmd.execute(machine_id)


class StartMachine(BaseCommand):
    def execute(self, machine_id):
        endpoint = MachineAPI()

        click.echo("\nAttempting to start machine...\n")
        result = endpoint.start_machine(machine_id)

        if result["success"]:
            click.echo(f"{result['data']['message']}")
        else:
            click.echo("Failed to start machine. Check machine ID and try again.")


@click.command()
@click.option("--machine-id", "-id", required=True, prompt="Enter machine ID")
@click.pass_context
def start_machine(ctx, machine_id):
    """Start machine with machine ID."""
    cmd = StartMachine()
    cmd.execute(machine_id)


class TerminateMachine(BaseCommand):
    def execute(self, machine_id):
        endpoint = MachineAPI()

        click.echo("\nAttempting to terminate machine...\n")
        result = endpoint.terminate_machine(machine_id)

        if result["success"]:
            click.echo(f"{result['data']['message']}")
        else:
            click.echo("Failed to terminate machine. Check machine ID and try again.")


@click.command()
@click.option("--machine-id", "-id", required=True, prompt="Enter machine ID")
@click.pass_context
def terminate_machine(ctx, machine_id):
    """Terminate machine with machine ID."""
    cmd = TerminateMachine()
    cmd.execute(machine_id)


class GetMachineDetails(BaseCommand):
    def execute(self, machine_id):
        endpoint = MachineAPI()

        result = endpoint.get_machine(machine_id)

        if result["success"]:
            click.echo(f"Machine {machine_id} details:")
            click.echo(result["data"])
            return result["data"]
        else:
            click.echo("Failed to Get machine. Check machine ID and try again.")


@click.command()
@click.option("--machine-id", "-id", required=True, prompt="Enter machine ID")
@click.pass_context
def get_machine_details(ctx, machine_id):
    """Get machine details with machine ID."""
    cmd = GetMachineDetails()
    cmd.execute(machine_id)
