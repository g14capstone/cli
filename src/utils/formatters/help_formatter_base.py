from abc import ABC, abstractmethod

import rich.box as rBox
from rich.align import Align as rAlign
from rich.console import Console as rConsole
from rich.table import Table as rTable


class HelpFormatterBase(ABC):
    item_padding = " " * 4

    @abstractmethod
    def __init__(self, console: rConsole) -> None:
        pass

    @abstractmethod
    def format_header(self, console: rConsole) -> None:
        pass

    @abstractmethod
    def format_usage(self, console: rConsole, usage_text: str) -> None:
        pass

    def add_section_header(self, title: str):
        title = f"━━━ {title.upper()}"
        right_sep = "━" * (self.width - len(title) - 3)
        self.main_table.add_row(
            rAlign(f"[bold cyan]{title} {right_sep}[/]"), style="on black"
        )

    def create_main_table(self):
        self.main_table = rTable(
            show_header=False,
            box=rBox.SIMPLE,
            padding=(0, 0, 0, 0),
            width=self.width,
            border_style="cyan",
            show_edge=True,
            pad_edge=False,
        )
        self.main_table.add_column("Content", style="bright_white")

    def format_commands(self, commands: dict, title: str) -> None:
        self.add_section_header(title)
        if title == "COMMANDS":
            prefix = "❯"
            print_newline = True
        else:
            prefix = "▶"
            print_newline = False

        for name, cmd in sorted(commands.items()):
            help = cmd.help.split("\n")[0]

            self.main_table.add_row(
                f"{self.item_padding}{prefix} [green]{name:<13}[/] { help or ''}"
            )
        if print_newline:
            self.main_table.add_row()

    def format_options(self, options: list) -> None:
        self.add_section_header("OPTIONS")
        for opt, desc in options:
            self.main_table.add_row(f"{self.item_padding}[magenta]{opt:<15}[/] {desc}")
        self.main_table.add_row()

    def render(self) -> None:
        if self.main_table:
            self.console.print(self.main_table)
