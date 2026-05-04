import json
import uuid
from datetime import datetime
from typing import Optional

import typer
from rich.console import Console

from qk.config import get_data_dir
from qk.utils.display import print_table, print_success, print_error, print_warning

app = typer.Typer()
console = Console()


def _saves_path():
    return get_data_dir() / "saves.json"


def _load_saves() -> list[dict]:
    path = _saves_path()
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return []


def _save_saves(saves: list[dict]) -> None:
    path = _saves_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(saves, indent=2, ensure_ascii=False), encoding="utf-8")


@app.command()
def add(description: str, command: str, tag: Optional[str] = typer.Option(None, help="Comma-separated tags")):
    """Save a command with description and optional tags."""
    saves = _load_saves()
    entry = {
        "id": uuid.uuid4().hex[:8],
        "description": description,
        "command": command,
        "tags": [t.strip() for t in tag.split(",")] if tag else [],
        "created": datetime.now().isoformat(),
    }
    saves.append(entry)
    _save_saves(saves)
    print_success(f"Saved: {description}")


@app.command("list")
def list_saves(tag: Optional[str] = typer.Option(None, help="Filter by tag")):
    """List all saved commands."""
    saves = _load_saves()
    if tag:
        saves = [s for s in saves if tag in s.get("tags", [])]
    if not saves:
        print_warning("No saved commands found.")
        return
    rows = [[s["id"], s["description"], s["command"], ", ".join(s.get("tags", []))] for s in saves]
    print_table("Saved Commands", ["ID", "Description", "Command", "Tags"], rows)


@app.command()
def search(query: str):
    """Search saved commands by description or command text."""
    saves = _load_saves()
    results = [s for s in saves if query.lower() in s["description"].lower() or query.lower() in s["command"].lower()]
    if not results:
        print_warning(f"No results for '{query}'.")
        return
    rows = [[s["id"], s["description"], s["command"], ", ".join(s.get("tags", []))] for s in results]
    print_table(f"Search: '{query}'", ["ID", "Description", "Command", "Tags"], rows)


@app.command()
def remove(id: str):
    """Remove a saved command by ID."""
    saves = _load_saves()
    new_saves = [s for s in saves if s["id"] != id]
    if len(new_saves) == len(saves):
        print_error(f"No command found with ID '{id}'.")
        raise typer.Exit(1)
    _save_saves(new_saves)
    print_success(f"Removed command '{id}'.")


@app.command()
def copy(id: str):
    """Copy a saved command to clipboard."""
    import pyperclip
    saves = _load_saves()
    match = [s for s in saves if s["id"] == id]
    if not match:
        print_error(f"No command found with ID '{id}'.")
        raise typer.Exit(1)
    pyperclip.copy(match[0]["command"])
    print_success(f"Copied to clipboard: {match[0]['command']}")
