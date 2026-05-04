from typer.testing import CliRunner
from qk.modules.convert import app

runner = CliRunner()


def test_convert_weight():
    result = runner.invoke(app, ["unit", "100", "kg", "lb"])
    assert result.exit_code == 0
    assert "220.5" in result.output


def test_convert_temperature():
    result = runner.invoke(app, ["unit", "100", "c", "f"])
    assert result.exit_code == 0
    assert "212" in result.output


def test_convert_px_to_rem():
    result = runner.invoke(app, ["unit", "16", "px", "rem"])
    assert result.exit_code == 0
    assert "1" in result.output


def test_convert_color_hex_to_rgb():
    result = runner.invoke(app, ["color", "#ff5733"])
    assert result.exit_code == 0
    assert "255" in result.output


def test_base64_encode():
    result = runner.invoke(app, ["base64", "hello world"])
    assert result.exit_code == 0
    assert "aGVsbG8gd29ybGQ=" in result.output


def test_base64_decode():
    result = runner.invoke(app, ["base64", "aGVsbG8gd29ybGQ=", "--decode"])
    assert result.exit_code == 0
    assert "hello world" in result.output


def test_json_pretty():
    result = runner.invoke(app, ["json-fmt", '{"a":1,"b":2}'])
    assert result.exit_code == 0
    assert '"a"' in result.output


def test_json_mini():
    result = runner.invoke(app, ["json-fmt", '{"a": 1, "b": 2}', "--mini"])
    assert result.exit_code == 0
