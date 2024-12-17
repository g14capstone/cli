import click

from src.utils.groups.subcommand_group import SubCommandGroup


class MachineMetricsCommand:
    """Commands for machine metrics."""

    click.echo("Function not yet supported.")
    pass


@click.group(cls=SubCommandGroup)
@click.pass_context
def metrics(ctx):
    """Function not yet supported."""
    ctx.obj = MachineMetricsCommand()
