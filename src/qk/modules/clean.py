import hashlib
import os
from pathlib import Path

import typer
from rich.console import Console

from qk.utils.display import print_table, print_success, print_warning
from qk.utils.platform import get_temp_dirs

app = typer.Typer()
console = Console()

TEMP_PATTERNS = ["*.tmp", "*.temp", "*.log", "Thumbs.db", ".DS_Store", "*.bak", "*~"]


def _human_size(size: int) -> str:
    for unit_name in ["B", "KB", "MB", "GB"]:
        if size < 1024:
            return f"{size:.1f} {unit_name}"
        size /= 1024
    return f"{size:.1f} TB"


@app.command()
def temp(dry: bool = typer.Option(False, help="Preview without deleting")):
    """Find and clean temporary files."""
    scan_dir = os.environ.get("QK_TEMP_SCAN_DIR")
    dirs = [Path(scan_dir)] if scan_dir else get_temp_dirs()
    found = []
    for d in dirs:
        if not d.exists():
            continue
        for pattern in TEMP_PATTERNS:
            for f in d.rglob(pattern):
                if f.is_file():
                    try:
                        size = f.stat().st_size
                        found.append((f, size))
                    except OSError:
                        pass
    if not found:
        print_warning("No temporary files found.")
        return
    rows = [[str(f), _human_size(s)] for f, s in found]
    print_table("Temporary Files", ["Path", "Size"], rows)
    if dry:
        console.print(f"\n[dim]Dry run — {len(found)} file(s) found, none deleted.[/dim]")
        return
    confirm = typer.confirm(f"Delete {len(found)} file(s)?")
    if not confirm:
        return
    deleted = 0
    for f, _ in found:
        try:
            f.unlink()
            deleted += 1
        except OSError:
            pass
    print_success(f"Deleted {deleted} file(s).")


@app.command()
def big(directory: str, top: int = typer.Option(10, help="Number of files to show")):
    """Find the largest files in a directory."""
    path = Path(directory)
    if not path.is_dir():
        typer.echo(f"Not a directory: {directory}")
        raise typer.Exit(1)
    files = []
    for f in path.rglob("*"):
        if f.is_file():
            try:
                files.append((f, f.stat().st_size))
            except OSError:
                pass
    files.sort(key=lambda x: x[1], reverse=True)
    files = files[:top]
    if not files:
        print_warning("No files found.")
        return
    rows = [[str(f.relative_to(path)), _human_size(s)] for f, s in files]
    print_table(f"Largest Files in {directory}", ["File", "Size"], rows)


@app.command()
def duplicates(directory: str, dry: bool = typer.Option(False, help="Preview without deleting")):
    """Find duplicate files by content hash."""
    path = Path(directory)
    if not path.is_dir():
        typer.echo(f"Not a directory: {directory}")
        raise typer.Exit(1)
    hashes: dict[str, list[Path]] = {}
    for f in path.rglob("*"):
        if f.is_file():
            try:
                h = hashlib.md5(f.read_bytes()).hexdigest()
                hashes.setdefault(h, []).append(f)
            except OSError:
                pass
    dupes = {h: file_list for h, file_list in hashes.items() if len(file_list) > 1}
    if not dupes:
        print_warning("No duplicate files found.")
        return
    rows = []
    for h, file_list in dupes.items():
        for f in file_list:
            rows.append([str(f.relative_to(path)), _human_size(f.stat().st_size), h[:12]])
    print_table("Duplicate Files", ["File", "Size", "Hash"], rows)
    if dry:
        console.print(f"\n[dim]Dry run — no files deleted.[/dim]")
