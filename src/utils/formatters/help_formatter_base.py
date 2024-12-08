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

    @abstractmethod
    def format_options(self, console: rConsole, options: list) -> None:
        pass

    @abstractmethod
    def format_commands(self, console: rConsole, commands: dict, title: str) -> None:
        pass

    @abstractmethod
    def render(self, console: rConsole) -> None:
        pass

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

    def add_section_header(self, title: str):
        title = f"━━━ {title.upper()}"
        right_sep = "━" * (self.width - len(title) - 3)
        self.main_table.add_row(
            rAlign(f"[bold cyan]{title} {right_sep}[/]"), style="on black"
        )
