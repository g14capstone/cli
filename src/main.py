import click
from src.commands.auth_commands import login, logout

@click.group()
def quack():
    """Quack CLI tool"""
    pass

quack.add_command(login)
quack.add_command(logout)

if __name__ == "__main__":
    quack()