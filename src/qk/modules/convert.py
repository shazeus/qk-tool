import base64
import json

import typer
from rich.console import Console

from qk.utils.display import print_error

app = typer.Typer()
console = Console()

UNIT_TABLE = {
    ("kg", "lb"): lambda v: v * 2.20462,
    ("lb", "kg"): lambda v: v / 2.20462,
    ("km", "mi"): lambda v: v * 0.621371,
    ("mi", "km"): lambda v: v / 0.621371,
    ("m", "ft"): lambda v: v * 3.28084,
    ("ft", "m"): lambda v: v / 3.28084,
    ("cm", "in"): lambda v: v * 0.393701,
    ("in", "cm"): lambda v: v / 0.393701,
    ("c", "f"): lambda v: v * 9 / 5 + 32,
    ("f", "c"): lambda v: (v - 32) * 5 / 9,
    ("px", "rem"): lambda v: v / 16,
    ("rem", "px"): lambda v: v * 16,
    ("l", "gal"): lambda v: v * 0.264172,
    ("gal", "l"): lambda v: v / 0.264172,
}


@app.command()
def unit(value: float, from_unit: str, to_unit: str):
    """Convert between units (kg/lb, c/f, px/rem, km/mi, etc.)."""
    key = (from_unit.lower(), to_unit.lower())
    if key not in UNIT_TABLE:
        print_error(f"Unknown conversion: {from_unit} → {to_unit}")
        supported = ", ".join(f"{a}→{b}" for a, b in UNIT_TABLE)
        console.print(f"[dim]Supported: {supported}[/dim]")
        raise typer.Exit(1)
    result = UNIT_TABLE[key](value)
    console.print(f"\n[bold]{value} {from_unit}[/bold] = [bold green]{result:.4g} {to_unit}[/bold green]\n")


@app.command()
def color(hex_code: str):
    """Convert hex color to RGB."""
    hex_clean = hex_code.lstrip("#")
    if len(hex_clean) != 6:
        print_error("Invalid hex color. Use format: #ff5733 or ff5733")
        raise typer.Exit(1)
    r, g, b = int(hex_clean[:2], 16), int(hex_clean[2:4], 16), int(hex_clean[4:6], 16)
    console.print(f"\n[bold]{hex_code}[/bold] = [bold green]rgb({r}, {g}, {b})[/bold green]\n")


@app.command("base64")
def base64_convert(text: str, decode: bool = typer.Option(False, help="Decode instead of encode")):
    """Base64 encode or decode text."""
    if decode:
        try:
            result = base64.b64decode(text).decode("utf-8")
        except Exception:
            print_error("Invalid base64 input.")
            raise typer.Exit(1)
    else:
        result = base64.b64encode(text.encode("utf-8")).decode("utf-8")
    console.print(f"\n[bold green]{result}[/bold green]\n")


@app.command("json-fmt")
def json_format(text: str, mini: bool = typer.Option(False, help="Minify instead of prettify")):
    """Prettify or minify JSON."""
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        print_error("Invalid JSON input.")
        raise typer.Exit(1)
    if mini:
        result = json.dumps(data, separators=(",", ":"), ensure_ascii=False)
    else:
        result = json.dumps(data, indent=2, ensure_ascii=False)
    console.print(f"\n{result}\n")
