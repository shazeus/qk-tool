from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()


def format_table(title: str, columns: list[str], rows: list[list[str]]) -> Table:
    table = Table(title=title, show_lines=False)
    for col in columns:
        table.add_column(col, style="cyan")
    for row in rows:
        table.add_row(*row)
    return table


def format_panel(title: str, content: str) -> Panel:
    return Panel(content, title=title, border_style="blue")


def print_success(msg: str) -> None:
    console.print(f"[green]✓[/green] {msg}")


def print_error(msg: str) -> None:
    console.print(f"[red]✗[/red] {msg}")


def print_warning(msg: str) -> None:
    console.print(f"[yellow]![/yellow] {msg}")


def print_table(title: str, columns: list[str], rows: list[list[str]]) -> None:
    console.print(format_table(title, columns, rows))


def print_panel(title: str, content: str) -> None:
    console.print(format_panel(title, content))
