from rich.console import Console
from rich.table import Table

console = Console()
rich_print = console.print

DOT_CHAR = "•"


def newline():
    print("\n", end="")


def print_both_sides(left, right):
    grid = Table.grid(expand=True)
    grid.add_column()
    grid.add_column(justify="right")
    grid.add_row(left, right)

    rich_print(grid)


def print_line(rule_style="dim green", char="─"):
    console.rule(style=rule_style, characters=char)


def observer_message(message, style="yellow"):
    return f"[{style}]observer[/{style}] [dim]{DOT_CHAR}[/dim] {message}"
