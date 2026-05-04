from typer.testing import CliRunner
from qk.modules.text import app

runner = CliRunner()


def test_count_file(tmp_path):
    f = tmp_path / "test.txt"
    f.write_text("hello world\nfoo bar baz\n")
    result = runner.invoke(app, ["count", str(f)])
    assert result.exit_code == 0
    assert "2" in result.output
    assert "5" in result.output


def test_case_to_snake():
    result = runner.invoke(app, ["case", "helloWorld", "--to", "snake"])
    assert result.exit_code == 0
    assert "hello_world" in result.output


def test_case_to_camel():
    result = runner.invoke(app, ["case", "hello_world", "--to", "camel"])
    assert result.exit_code == 0
    assert "helloWorld" in result.output


def test_case_to_kebab():
    result = runner.invoke(app, ["case", "hello world", "--to", "kebab"])
    assert result.exit_code == 0
    assert "hello-world" in result.output


def test_lorem():
    result = runner.invoke(app, ["lorem", "2"])
    assert result.exit_code == 0
    assert len(result.output.strip()) > 50


def test_regex(tmp_path):
    f = tmp_path / "test.txt"
    f.write_text("foo123bar\nhello456world\nnothing\n")
    result = runner.invoke(app, ["regex", r"\d+", str(f)])
    assert result.exit_code == 0
    assert "123" in result.output
    assert "456" in result.output
