from rich.console import Console
from rich.table import Table
from qk.config import ALL_MODULES, MODULE_DESCRIPTIONS, save_config

console = Console()


def parse_toggle_input(text: str) -> list[int]:
    text = text.strip()
    if not text:
        return []
    indices = []
    for part in text.split():
        if part.isdigit():
            indices.append(int(part) - 1)
    return indices


def apply_toggles(modules: dict[str, bool], indices: list[int]) -> dict[str, bool]:
    result = dict(modules)
    for idx in indices:
        if 0 <= idx < len(ALL_MODULES):
            name = ALL_MODULES[idx]
            result[name] = not result[name]
    return result


def _show_module_table(modules: dict[str, bool]) -> None:
    table = Table(title="QK Modules", show_lines=False)
    table.add_column("#", style="dim", width=3)
    table.add_column("Status", width=4)
    table.add_column("Module", style="cyan")
    table.add_column("Description")
    for i, mod in enumerate(ALL_MODULES):
        status = "[green]✓[/green]" if modules.get(mod, True) else "[red]✗[/red]"
        table.add_row(str(i + 1), status, mod, MODULE_DESCRIPTIONS[mod])
    console.print(table)


def run_setup() -> dict:
    console.print("\n[bold blue]🔧 QK Setup — Hoş geldin! / Welcome![/bold blue]\n")
    modules = {mod: True for mod in ALL_MODULES}

    while True:
        _show_module_table(modules)
        console.print("\nToggle modules by entering their numbers (e.g. '3 5 7').")
        response = console.input("[dim]Press Enter to confirm: [/dim]")
        indices = parse_toggle_input(response)
        if not indices:
            break
        modules = apply_toggles(modules, indices)
        console.print()

    config = {"modules": modules}
    save_config(config)
    console.print("\n[green]✓ Setup complete! Run [bold]qk --help[/bold] to get started.[/green]\n")
    return config
