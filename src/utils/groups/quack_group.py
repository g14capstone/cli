import io

import click
from rich.console import Console as rConsole

from src.utils.formatters.quack_formatter import MainframeFormatter


class QuackGroup(click.Group):
    def format_help(self, ctx, formatter):
        sio = io.StringIO()
        console = rConsole(file=sio, force_terminal=True)
        help_formatter = MainframeFormatter(console)

        # Format header and initialize table
        help_formatter.format_header("Quack  CLI", self.help)

        help_formatter.format_usage(ctx.get_usage().removeprefix("Usage: "))
        # Get options from the context's command
        options = []
        for param in ctx.command.get_params(ctx):
            if isinstance(param, click.Option):
                opt_names = "/".join(param.opts)
                opt_help = param.help or ""
                options.append((opt_names, opt_help))

        help_formatter.format_options(options)

        if self.commands:
            commands = {
                name: cmd
                for name, cmd in self.commands.items()
                if not isinstance(cmd, click.Group)
            }
            subcommands = {
                name: cmd
                for name, cmd in self.commands.items()
                if isinstance(cmd, click.Group)
            }

            if commands:
                help_formatter.format_commands(commands, "COMMANDS")
            if subcommands:
                help_formatter.format_commands(subcommands, "SUBCOMMANDS")

        # Render the final table
        help_formatter.render()
        formatter.write(sio.getvalue())
