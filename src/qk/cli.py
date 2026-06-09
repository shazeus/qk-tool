import sys
from typing import Annotated

import typer

from qk import __version__
from qk.config import config_exists, is_module_enabled

HELP_TEXT = "QK — Your Swiss army knife for daily computer tasks."
SKIP_SETUP_FLAGS = {"--help", "--version", "--show-completion", "--install-completion"}


def create_app(skip_setup: bool = False) -> typer.Typer:
    app = typer.Typer(name="qk", help=HELP_TEXT, no_args_is_help=True)

    @app.callback(invoke_without_command=True)
    def main(
        version: Annotated[
            bool,
            typer.Option(
                "--version",
                help="Show the QK version and exit.",
                is_eager=True,
            ),
        ] = False,
    ) -> None:
        if version:
            typer.echo(f"qk-tool {__version__}")
            raise typer.Exit()

    @app.command()
    def setup():
        """Re-run the setup wizard to enable/disable modules."""
        from qk.setup_wizard import run_setup
        run_setup()

    if is_module_enabled("save"):
        from qk.modules.save import app as save_app
        app.add_typer(save_app, name="save", help="Save & search commands")

    if is_module_enabled("system"):
        from qk.modules.system import app as system_app
        app.add_typer(system_app, name="system", help="System actions")

    if is_module_enabled("organize"):
        from qk.modules.organize import app as organize_app
        app.add_typer(organize_app, name="organize", help="Organize files")

    if is_module_enabled("convert"):
        from qk.modules.convert import app as convert_app
        app.add_typer(convert_app, name="convert", help="Unit & format converter")

    if is_module_enabled("note"):
        from qk.modules.note import app as note_app
        app.add_typer(note_app, name="note", help="Quick notes")

    if is_module_enabled("security"):
        from qk.modules.security import app as security_app
        app.add_typer(security_app, name="security", help="Password & security tools")

    if is_module_enabled("clean"):
        from qk.modules.clean import app as clean_app
        app.add_typer(clean_app, name="clean", help="System cleaner")

    if is_module_enabled("text"):
        from qk.modules.text import app as text_app
        app.add_typer(text_app, name="text", help="Text processing")

    if is_module_enabled("net"):
        from qk.modules.net import app as net_app
        app.add_typer(net_app, name="net", help="Network tools")

    return app


def app_entry() -> None:
    if not config_exists() and not any(arg in SKIP_SETUP_FLAGS for arg in sys.argv[1:]):
        from qk.setup_wizard import run_setup
        run_setup()
    app = create_app()
    app()
