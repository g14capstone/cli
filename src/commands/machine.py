import json

import click
import click_spinner

from src.api.machine_api import MachineAPI
from src.utils.groups.subcommand_group import SubCommandGroup


machine_types = ["cpu", "gpu", "fpga"]


class MachineCommands:
    def __init__(self):
        self.cpu = machine_types[0]
        self.gpu = machine_types[1]
        self.fpga = machine_types[2]
        self.endpoint = MachineAPI()

    def create(self, hardware_type, machine_name, machine_type):
        """
        create create a machine with name and type.

        :param machine_name: descriptor of machine
        :type machine_name:  str
        :param machine_type: GPU: [g4dn.xlarge]
                             FPGA: [f1.2xlarge, f1.4xlarge, f1.16xlarge]
                             CPU: [t2.micro, m5.xlarge, m5.2xlarge]
        :type machine_type:  TBD
        """
        with click_spinner.spinner():
            match hardware_type:
                case self.gpu:
                    result = self.endpoint.create_gpu_machine(
                        machine_name, machine_type
                    )
                case self.fpga:
                    result = self.endpoint.create_fpga_machine(
                        machine_name, machine_type
                    )
                case self.cpu:
                    result = self.endpoint.create_cpu_machine(
                        machine_name, machine_type
                    )
                case _:
                    click.echo("Invalid hardware type.")
                    return -1

        if result["success"]:
            click.echo("Machine created successfully. Details:")
            click.echo(json.dumps(result["data"], indent=2))
        else:
            click.echo(
                "Failed to create machine. Check machine name and type and try again."
            )

    def pull_model(self, hardware_type, machine_id, model_name):
        click.echo(f"Pulling model {model_name} for machine {machine_id}")
        with click_spinner.spinner():
            match hardware_type:
                case self.gpu:
                    result = self.endpoint.pull_gpu_model(machine_id, model_name)
                case self.fpga:
                    click.secho("FPGA pull model not supported yet.", fg="yellow")
                    return
                case self.cpu:
                    result = self.endpoint.pull_cpu_model(machine_id, model_name)
                case _:
                    click.echo("Invalid hardware type.")
                    return -1

        if result["success"]:
            click.echo(f"Model {model_name} pulled successfully.")
        else:
            click.echo(
                "Failed to pull model. Check machine ID and model name and try again."
            )

    def delete_machine_model(self, hardware_type, machine_id, model_name):
        click.echo(f"Deleting model {model_name} for machine {machine_id}")
        with click_spinner.spinner():
            match hardware_type:
                case self.gpu:
                    result = self.endpoint.delete_gpu_model(machine_id, model_name)
                case self.fpga:
                    click.secho("FPGA delete model not supported yet.", fg="yellow")
                    return
                case self.cpu:
                    result = self.endpoint.delete_cpu_model(machine_id, model_name)
                case _:
                    click.echo("Invalid hardware type.")
                    return -1
        if result["success"]:
            click.echo(f"Model {model_name} deleted successfully.")
        else:
            click.echo(
                "Failed to delete model. Check machine ID and model name and try again."
            )

    def get_inference_url(self, hardware_type, machine_id):
        with click_spinner.spinner():
            match hardware_type:
                case self.gpu:
                    result = self.endpoint.get_gpu_inference_url(machine_id)
                case self.fpga:
                    result = self.endpoint.get_fpga_inference_url(machine_id)
                case self.cpu:
                    result = self.endpoint.get_cpu_inference_url(machine_id)
                case _:
                    click.echo("Invalid hardware type.")
                    return -1

        if result["success"]:
            click.echo(f"Inference URL: {result['data']['inference_url']}")
        else:
            click.echo("Failed to get inference URL. Check machine ID and try again.")

    def list(self):
        with click_spinner.spinner():
            result = self.endpoint.list_user_machines()
        if result["success"]:
            if not result["data"]:
                click.echo("No machines to list.")
                return
            click.echo("Machines:")
            for machine in result["data"]:
                click.echo(json.dumps(machine, indent=2))
            return result
        else:
            click.echo("Failed to retrieve list of machines.")

    def stop(self, machine_id):
        click.echo("\nAttempting to stop machine...\n")
        with click_spinner.spinner():
            result = self.endpoint.stop_machine(machine_id)
        if result["success"]:
            click.echo(f"{result['data']['message']}")
        else:
            click.echo("Failed to stop machine. Check machine ID and try again.")

    def start(self, machine_id):
        click.echo("\nAttempting to start machine...\n")
        with click_spinner.spinner():
            result = self.endpoint.start_machine(machine_id)
        if result["success"]:
            click.echo(f"{result['data']['message']}")
        else:
            click.echo("Failed to start machine. Check machine ID and try again.")

    def terminate(self, machine_id):
        click.echo("\nAttempting to terminate machine...\n")
        with click_spinner.spinner():
            result = self.endpoint.terminate_machine(machine_id)
        if result["success"]:
            click.echo(f"{result['data']['message']}")
        else:
            click.echo("Failed to terminate machine. Check machine ID and try again.")

    def get_details(self, machine_id):
        with click_spinner.spinner():
            result = self.endpoint.get_machine(machine_id)
        if result["success"]:
            click.echo(f"Machine {machine_id} details:")
            click.echo(json.dumps(result["data"], indent=2))
            return result["data"]
        else:
            click.echo("Failed to get machine. Check machine ID and try again.")


@click.group(cls=SubCommandGroup)
@click.pass_context
def machine(ctx):
    """Machine management commands."""
    ctx.obj = MachineCommands()


@machine.command()
@click.pass_context
@click.argument("hardware-type", type=click.Choice(machine_types))
@click.option("--machine-name", "-n", required=True, prompt="Enter machine name")
@click.option("--machine-type", "-t", required=True, prompt="Choose machine type")
def create(ctx, hardware_type, machine_name, machine_type):
    """Create a machine with name and type.

    Valid machine types:

    - CPU: \t[t2.micro, m5.xlarge, m5.2xlarge]

    - GPU: \t[g4dn.xlarge]

    - FPGA: \t[f1.2xlarge, f1.4xlarge, f1.16xlarge]
    """
    valid_machine_types = {
        "gpu": ["g4dn.xlarge"],
        "fpga": ["f1.2xlarge", "f1.4xlarge", "f1.16xlarge"],
        "cpu": ["t2.micro", "m5.xlarge", "m5.2xlarge"],
    }

    if machine_type not in valid_machine_types[hardware_type]:
        click.secho(
            f"Invalid machine type for {hardware_type}. See `quack machine create --help` for options.",
            fg="red",
        )
        return

    ctx.obj.create(hardware_type, machine_name, machine_type)


@machine.command()
@click.pass_context
@click.argument("hardware-type", type=click.Choice(machine_types))
@click.option("--machine-id", "-id", required=True, prompt="Enter machine ID")
@click.option("--model-name", "-m", required=True, prompt="Enter model name")
def pull_model(ctx, hardware_type, machine_id, model_name):
    """Pull model for machine to machine with machine ID.

    See `quack model list` for available models.
    """
    with open("src/models/default_models.json", "r") as f:
        models = json.loads(f.read())
    for item in models:
        if model_name == item["name"] and item["available"][f"{hardware_type}"]:
            ctx.obj.pull_model(hardware_type, machine_id, model_name)
            return
    else:
        click.secho(
            "Invalid parameters. See `quack machine pull-model --help` for options.",
            fg="red",
        )
        return


@machine.command()
@click.pass_context
@click.argument("hardware-type", type=click.Choice(machine_types))
@click.option("--machine-id", "-id", required=True, prompt="Enter machine ID")
@click.option("--model-name", "-m", required=True, prompt="Enter model name")
def delete_model(ctx, hardware_type, machine_id, model_name):
    """Delete model for machine with machine ID."""
    ctx.obj.delete_machine_model(hardware_type, machine_id, model_name)


@machine.command()
@click.pass_context
@click.argument("hardware-type", type=click.Choice(machine_types))
@click.option("--machine-id", "-id", required=True, prompt="Enter machine ID")
def infer_url(ctx, hardware_type, machine_id):
    """Get inference URL for machine with machine ID."""
    ctx.obj.get_inference_url(hardware_type, machine_id)


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
