from pyfiglet import Figlet, FontNotFound
from rich.align import Align as rAlign
from rich.console import Console as rConsole
from rich.panel import Panel as rPanel

from src.utils.formatters.help_formatter_base import HelpFormatterBase


class MainframeFormatter(HelpFormatterBase):
    def __init__(self, console: rConsole, format: str = None) -> None:
        self.console = console
        self.format = format if format else "cricket"
        self.width = max(60, self.console.width - 4)
        self.main_table = None
        self.create_main_table()

    def format_header(self, title: str, help: str) -> None:
        # Keep ASCII art header separate
        try:
            fig = Figlet(font=self.format, width=self.width - 1)
        except FontNotFound:
            self.console.print(f"Font {self.format} not found. Using default.")
            fig = Figlet(font="cricket", width=self.width - 1)
        ascii_art = fig.renderText(title)
        styled_art = rAlign(f"[bold yellow]{ascii_art}[/]", align="center")
        styled_help = rPanel(
            rAlign(f"{help}", align="center"),
            title="by Duckington Labs",
            border_style="bright_yellow",
        )
        self.main_table.add_row(styled_art)
        self.main_table.add_row(styled_help)

    def format_usage(self, usage_text: str) -> None:
        self.add_section_header("USAGE")
        self.main_table.add_row(f"{self.item_padding}{usage_text}\n")

    def format_options(self, options: list) -> None:
        self.add_section_header("OPTIONS")
        for opt, desc in options:
            self.main_table.add_row(f"{self.item_padding}[magenta]{opt:<15}[/] {desc}")
        self.main_table.add_row()

    def format_commands(self, commands: dict, title: str) -> None:
        self.add_section_header(title)
        if title == "COMMANDS":
            prefix = "❯"
            print_newline = True
        else:
            prefix = "▶"
            print_newline = False

        for name, cmd in sorted(commands.items()):
            self.main_table.add_row(
                f"{self.item_padding}{prefix} [green]{name:<13}[/] {cmd.help or ''}"
            )
        if print_newline:
            self.main_table.add_row()

    def render(self) -> None:
        if self.main_table:
            self.console.print(self.main_table)
