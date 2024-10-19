import click
from src.commands.base_command import BaseCommand


class MachineMetricsCommand(BaseCommand):
    def execute(self):
        print("Function not yet supported.")


@click.command()
@click.pass_context
def machine_metrics(ctx):
    """
    This command is not implemented yet.
    """
    cmd = MachineMetricsCommand()
    cmd.execute()
