import click

import src.commands as commands


@click.group()
def quack():
    """Quack CLI tool"""
    pass


cmds = {}
# register all groups and only standalone commands
for mod in commands.__all__:
    groups = [
        getattr(mod, attr)
        for attr in dir(mod)
        if isinstance(getattr(mod, attr), click.core.Group)
    ]
    all_cmds = [
        getattr(mod, attr)
        for attr in dir(mod)
        if isinstance(getattr(mod, attr), click.core.Command)
    ]

    # Register groups and track their commands
    for group in groups:
        cmds.update({sub_cmd.name: sub_cmd for sub_cmd in group.commands.values()})
        quack.add_command(group)

    # Register standalone commands not part of any group
    for cmd in all_cmds:
        if cmd.name not in cmds:
            quack.add_command(cmd)

if __name__ == "__main__":
    quack()
