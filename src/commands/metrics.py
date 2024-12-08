import click

from src.utils.groups.subcommand_group import SubCommandGroup


class MachineMetricsCommand:
    """Commands for machine metrics."""

    pass


@click.group(cls=SubCommandGroup)
@click.pass_context
def metrics(ctx):
    """No implementation yet."""
    ctx.obj = MachineMetricsCommand()
