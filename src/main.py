import click


@click.command()
@click.option(
    "--msg", prompt="test message", help="message will be output to click terminal"
)
def main(msg):
    """main cli entrypoint (dummy for now)"""
    click.echo(f"{msg}")


if __name__ == "__main__":
    main()
