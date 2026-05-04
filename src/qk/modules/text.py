import re
from pathlib import Path

import typer
from rich.console import Console

from qk.utils.display import print_table, print_error

app = typer.Typer()
console = Console()

LOREM_PARAGRAPH = (
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor "
    "incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud "
    "exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure "
    "dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur."
)


def _split_camel(text: str) -> list[str]:
    parts = re.sub(r"([A-Z])", r" \1", text).strip().split()
    return [p.lower() for p in parts]


def _split_any(text: str) -> list[str]:
    if "_" in text:
        return [p.lower() for p in text.split("_") if p]
    if "-" in text:
        return [p.lower() for p in text.split("-") if p]
    if " " in text:
        return [p.lower() for p in text.split() if p]
    return _split_camel(text)


@app.command()
def count(path: str):
    """Count lines, words, and characters in a file."""
    file_path = Path(path)
    if not file_path.exists():
        print_error(f"File not found: {path}")
        raise typer.Exit(1)
    content = file_path.read_text(encoding="utf-8")
    lines = content.count("\n")
    words = len(content.split())
    chars = len(content)
    print_table(f"Count: {file_path.name}", ["Metric", "Value"], [
        ["Lines", str(lines)],
        ["Words", str(words)],
        ["Characters", str(chars)],
    ])


@app.command()
def case(text: str, to: str = typer.Option(..., help="Target case: snake, camel, kebab, pascal")):
    """Convert text between cases (snake_case, camelCase, kebab-case, PascalCase)."""
    words = _split_any(text)
    if to == "snake":
        result = "_".join(words)
    elif to == "camel":
        result = words[0] + "".join(w.capitalize() for w in words[1:])
    elif to == "kebab":
        result = "-".join(words)
    elif to == "pascal":
        result = "".join(w.capitalize() for w in words)
    else:
        print_error(f"Unknown case: {to}. Use: snake, camel, kebab, pascal")
        raise typer.Exit(1)
    console.print(f"\n[bold green]{result}[/bold green]\n")


@app.command()
def lorem(paragraphs: int = typer.Argument(1)):
    """Generate lorem ipsum paragraphs."""
    for i in range(paragraphs):
        console.print(LOREM_PARAGRAPH)
        if i < paragraphs - 1:
            console.print()


@app.command()
def regex(pattern: str, path: str):
    """Find regex matches in a file."""
    file_path = Path(path)
    if not file_path.exists():
        print_error(f"File not found: {path}")
        raise typer.Exit(1)
    content = file_path.read_text(encoding="utf-8")
    matches = []
    for i, line in enumerate(content.splitlines(), 1):
        for m in re.finditer(pattern, line):
            matches.append([str(i), m.group(), line.strip()])
    if not matches:
        console.print(f"[yellow]No matches for pattern '{pattern}'[/yellow]")
        return
    print_table(f"Regex: {pattern}", ["Line", "Match", "Context"], matches)
