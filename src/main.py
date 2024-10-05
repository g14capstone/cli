import click
from src.commands.auth_commands import login, logout

@click.group()
def quack():
    """Quack CLI tool"""
    pass

quack.add_command(login)
quack.add_command(logout)

@click.group()
def main():
    """Main entry point for the CLI."""
    pass

main.add_command(quack)

if __name__ == "__main__":
    main()