import json
from typer.testing import CliRunner
from qk import __version__
from qk.cli import create_app

runner = CliRunner()


def test_all_modules_registered(tmp_path, monkeypatch):
    monkeypatch.setenv("QK_DATA_DIR", str(tmp_path / ".qk"))
    app = create_app(skip_setup=True)
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    for module in ["save", "system", "organize", "convert", "note", "security", "clean", "text", "net"]:
        assert module in result.output, f"Module '{module}' not in help output"


def test_disabled_module_hidden(tmp_path, monkeypatch):
    monkeypatch.setenv("QK_DATA_DIR", str(tmp_path / ".qk"))
    config_path = tmp_path / ".qk" / "config.json"
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config = {"modules": {
        "save": True, "system": True, "organize": True, "convert": True,
        "note": True, "security": True, "clean": True, "text": True, "net": False,
    }}
    config_path.write_text(json.dumps(config))
    app = create_app(skip_setup=True)
    result = runner.invoke(app, ["--help"])
    assert "net" not in result.output


def test_end_to_end_save_flow(tmp_path, monkeypatch):
    monkeypatch.setenv("QK_DATA_DIR", str(tmp_path / ".qk"))
    app = create_app(skip_setup=True)
    result = runner.invoke(app, ["save", "add", "test cmd", "echo hello", "--tag", "test"])
    assert result.exit_code == 0
    result = runner.invoke(app, ["save", "list"])
    assert "test cmd" in result.output
    result = runner.invoke(app, ["save", "search", "test"])
    assert "test cmd" in result.output


def test_version_flag_returns_package_version():
    app = create_app(skip_setup=True)
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert f"qk-tool {__version__}" in result.output
