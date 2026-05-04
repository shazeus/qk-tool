import json
import shutil
import uuid
from pathlib import Path

import typer
from rich.console import Console

from qk.config import get_data_dir
from qk.utils.display import print_table, print_success, print_error, print_warning

app = typer.Typer()
console = Console()

DEFAULT_RULES = [
    {"id": "def1", "ext": ".pdf", "folder": "Documents"},
    {"id": "def2", "ext": ".doc", "folder": "Documents"},
    {"id": "def3", "ext": ".docx", "folder": "Documents"},
    {"id": "def4", "ext": ".txt", "folder": "Documents"},
    {"id": "def5", "ext": ".jpg", "folder": "Pictures"},
    {"id": "def6", "ext": ".jpeg", "folder": "Pictures"},
    {"id": "def7", "ext": ".png", "folder": "Pictures"},
    {"id": "def8", "ext": ".gif", "folder": "Pictures"},
    {"id": "def9", "ext": ".svg", "folder": "Pictures"},
    {"id": "def10", "ext": ".mp3", "folder": "Media"},
    {"id": "def11", "ext": ".mp4", "folder": "Media"},
    {"id": "def12", "ext": ".mov", "folder": "Media"},
    {"id": "def13", "ext": ".avi", "folder": "Media"},
    {"id": "def14", "ext": ".zip", "folder": "Archives"},
    {"id": "def15", "ext": ".rar", "folder": "Archives"},
    {"id": "def16", "ext": ".tar", "folder": "Archives"},
    {"id": "def17", "ext": ".gz", "folder": "Archives"},
    {"id": "def18", "ext": ".7z", "folder": "Archives"},
    {"id": "def19", "ext": ".exe", "folder": "Programs"},
    {"id": "def20", "ext": ".dmg", "folder": "Programs"},
    {"id": "def21", "ext": ".deb", "folder": "Programs"},
]


def _rules_path():
    return get_data_dir() / "organize_rules.json"


def _load_rules() -> list[dict]:
    path = _rules_path()
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return list(DEFAULT_RULES)


def _save_rules(rules: list[dict]) -> None:
    path = _rules_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(rules, indent=2, ensure_ascii=False), encoding="utf-8")


@app.command()
def run(directory: str, dry: bool = typer.Option(False, help="Preview without moving")):
    """Organize files in a directory by extension rules."""
    source = Path(directory)
    if not source.is_dir():
        print_error(f"Not a directory: {directory}")
        raise typer.Exit(1)
    rules = _load_rules()
    rule_map = {r["ext"]: r["folder"] for r in rules}
    moved = []
    for file in source.iterdir():
        if file.is_file():
            ext = file.suffix.lower()
            if ext in rule_map:
                dest_dir = source / rule_map[ext]
                if not dry:
                    dest_dir.mkdir(exist_ok=True)
                    shutil.move(str(file), str(dest_dir / file.name))
                moved.append([file.name, ext, rule_map[ext]])
    if not moved:
        print_warning("No files matched any rules.")
        return
    label = "Preview" if dry else "Organized"
    print_table(label, ["File", "Extension", "→ Folder"], moved)
    if dry:
        console.print("\n[dim]Dry run — no files were moved.[/dim]")
    else:
        print_success(f"Moved {len(moved)} file(s).")


@app.command("list-rules")
def list_rules():
    """List current organization rules."""
    rules = _load_rules()
    rows = [[r["id"], r["ext"], r["folder"]] for r in rules]
    print_table("Organization Rules", ["ID", "Extension", "Folder"], rows)


@app.command("add-rule")
def add_rule(ext: str, folder: str):
    """Add a new organization rule."""
    if not ext.startswith("."):
        ext = "." + ext
    rules = _load_rules()
    rules.append({"id": uuid.uuid4().hex[:8], "ext": ext, "folder": folder})
    _save_rules(rules)
    print_success(f"Rule added: {ext} → {folder}")


@app.command("remove-rule")
def remove_rule(id: str):
    """Remove an organization rule by ID."""
    rules = _load_rules()
    new_rules = [r for r in rules if r["id"] != id]
    if len(new_rules) == len(rules):
        print_error(f"No rule found with ID '{id}'.")
        raise typer.Exit(1)
    _save_rules(new_rules)
    print_success(f"Rule '{id}' removed.")
