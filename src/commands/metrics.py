import click


class MachineMetricsCommand:
    """Commands for machine metrics."""

    pass


@click.group()
@click.pass_context
def metrics(ctx):
    """
    No implementation yet.
    Get information about machine metrics.
    """
    ctx.obj = MachineMetricsCommand()
