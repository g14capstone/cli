import click
from types import ModuleType
from typing import List
import src.commands.auth_commands as auth_commands
import src.commands.metrics_commands as metrics_commands


@click.group()
def quack():
    """Quack CLI tool"""
    pass

def add_commands_to_cli(modules: List[ModuleType]) -> None:
    for mod in modules:
        for cmd in dir(mod):
            if isinstance(getattr(mod, cmd), click.core.Command):
                quack.add_command(getattr(mod, cmd))

command_modules = [auth_commands, metrics_commands]

add_commands_to_cli(command_modules)

if __name__ == "__main__":
    quack()
