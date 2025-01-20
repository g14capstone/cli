from rich.align import Align as rAlign
from rich.console import Console as rConsole
from rich.panel import Panel as rPanel

from src.utils.formatters.help_formatter_base import HelpFormatterBase


class SubFrameFormatter(HelpFormatterBase):
    def __init__(self, console: rConsole) -> None:
        self.console = console
        self.width = max(60, console.width - 4)
        self.main_table = None
        self.create_main_table()

    def format_header(self, title: str, help: str) -> None:
        styled_help = rPanel(
            rAlign(f"{help}", align="center"),
            title=f"quack {title}",
            border_style="yellow",
        )
        self.main_table.add_row(styled_help)

    def format_usage(self, usage_text: str) -> None:
        self.add_section_header("USAGE")
        self.main_table.add_row(f"{self.item_padding}{usage_text}")
        self.main_table.add_row()

    def format_options(self, options: list) -> None:
        self.add_section_header("OPTIONS")
        for opt, desc in options:
            self.main_table.add_row(f"{self.item_padding}[magenta]{opt:<15}[/] {desc}")
        self.main_table.add_row()
