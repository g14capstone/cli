import click
import src.commands.auth_commands as auth_commands


@click.group()
def quack():
    """Quack CLI tool"""
    pass


[
    quack.add_command(getattr(auth_commands, cmd))
    for cmd in dir(auth_commands)
    if isinstance(getattr(auth_commands, cmd), click.core.Command)
]

if __name__ == "__main__":
    quack()
