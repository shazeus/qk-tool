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


def _notes_path():
    return get_data_dir() / "notes.json"


def _load_notes() -> list[dict]:
    path = _notes_path()
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return []


def _save_notes(notes: list[dict]) -> None:
    path = _notes_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(notes, indent=2, ensure_ascii=False), encoding="utf-8")


@app.command()
def add(content: str, tag: Optional[str] = typer.Option(None, help="Comma-separated tags")):
    """Add a new note."""
    notes = _load_notes()
    entry = {
        "id": uuid.uuid4().hex[:8],
        "content": content,
        "tags": [t.strip() for t in tag.split(",")] if tag else [],
        "created": datetime.now().isoformat(),
    }
    notes.append(entry)
    _save_notes(notes)
    print_success("Note added.")


@app.command("list")
def list_notes(tag: Optional[str] = typer.Option(None, help="Filter by tag")):
    """List all notes."""
    notes = _load_notes()
    if tag:
        notes = [n for n in notes if tag in n.get("tags", [])]
    if not notes:
        print_warning("No notes found.")
        return
    rows = [[n["id"], n["content"], ", ".join(n.get("tags", [])), n["created"][:10]] for n in notes]
    print_table("Notes", ["ID", "Content", "Tags", "Date"], rows)


@app.command()
def search(query: str):
    """Search notes by content."""
    notes = _load_notes()
    results = [n for n in notes if query.lower() in n["content"].lower()]
    if not results:
        print_warning(f"No results for '{query}'.")
        return
    rows = [[n["id"], n["content"], ", ".join(n.get("tags", [])), n["created"][:10]] for n in results]
    print_table(f"Search: '{query}'", ["ID", "Content", "Tags", "Date"], rows)


@app.command()
def remove(id: str):
    """Remove a note by ID."""
    notes = _load_notes()
    new_notes = [n for n in notes if n["id"] != id]
    if len(new_notes) == len(notes):
        print_error(f"No note found with ID '{id}'.")
        raise typer.Exit(1)
    _save_notes(new_notes)
    print_success(f"Removed note '{id}'.")


@app.command()
def export():
    """Export all notes as markdown."""
    notes = _load_notes()
    if not notes:
        print_warning("No notes to export.")
        return
    lines = ["# QK Notes\n"]
    for n in notes:
        tags = f" `{'`, `'.join(n['tags'])}`" if n.get("tags") else ""
        lines.append(f"## {n['created'][:10]}{tags}\n")
        lines.append(f"{n['content']}\n")
    output = "\n".join(lines)
    console.print(output)
