import hashlib
import secrets
import string
from pathlib import Path

import typer
from rich.console import Console

from qk.utils.display import print_success, print_error, print_table

app = typer.Typer()
console = Console()


@app.command("pass")
def generate_password(
    length: int = typer.Option(16, help="Password length"),
    symbols: bool = typer.Option(False, help="Include symbols"),
):
    """Generate a secure random password."""
    chars = string.ascii_letters + string.digits
    if symbols:
        chars += string.punctuation
    password = "".join(secrets.choice(chars) for _ in range(length))
    console.print(f"\n[bold green]{password}[/bold green]\n")
    print_success(f"Generated {length}-character password.")


@app.command("hash")
def hash_text(text: str):
    """Show MD5 and SHA256 hashes of text."""
    md5 = hashlib.md5(text.encode()).hexdigest()
    sha256 = hashlib.sha256(text.encode()).hexdigest()
    print_table("Hash", ["Algorithm", "Value"], [["MD5", md5], ["SHA256", sha256]])


@app.command("hash-file")
def hash_file(path: str):
    """Show MD5 and SHA256 hashes of a file."""
    file_path = Path(path)
    if not file_path.exists():
        print_error(f"File not found: {path}")
        raise typer.Exit(1)
    data = file_path.read_bytes()
    md5 = hashlib.md5(data).hexdigest()
    sha256 = hashlib.sha256(data).hexdigest()
    print_table(f"Hash: {file_path.name}", ["Algorithm", "Value"], [["MD5", md5], ["SHA256", sha256]])


@app.command()
def checksum(path: str, expected: str):
    """Verify a file's SHA256 hash against an expected value."""
    file_path = Path(path)
    if not file_path.exists():
        print_error(f"File not found: {path}")
        raise typer.Exit(1)
    actual = hashlib.sha256(file_path.read_bytes()).hexdigest()
    if actual == expected.lower():
        print_success("Checksum matches!")
    else:
        print_error(f"Mismatch!\n  Expected: {expected}\n  Actual:   {actual}")
        raise typer.Exit(1)
