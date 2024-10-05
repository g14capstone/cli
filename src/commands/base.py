from abc import ABC, abstractmethod
import click

class BaseCommand(ABC):
    @abstractmethod
    def execute(self, *args, **kwargs):
        """Execute the command"""
        pass

    @classmethod
    def as_click_command(cls):
        """Wrapper to convert the command to a Click command"""
        @click.command()
        @click.pass_context
        def wrapped_command(ctx, *args, **kwargs):
            command = cls()
            return command.execute(*args, **kwargs)
        return wrapped_command
