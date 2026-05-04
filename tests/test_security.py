import hashlib
from typer.testing import CliRunner
from qk.modules.security import app

runner = CliRunner()


def test_generate_password_default():
    result = runner.invoke(app, ["pass"])
    assert result.exit_code == 0


def test_generate_password_custom_length():
    result = runner.invoke(app, ["pass", "--length", "24"])
    assert result.exit_code == 0


def test_generate_password_with_symbols():
    result = runner.invoke(app, ["pass", "--symbols"])
    assert result.exit_code == 0


def test_hash_text():
    result = runner.invoke(app, ["hash", "hello"])
    assert result.exit_code == 0
    assert "MD5" in result.output
    assert "SHA256" in result.output


def test_hash_file(tmp_path):
    f = tmp_path / "test.txt"
    f.write_text("hello world")
    result = runner.invoke(app, ["hash-file", str(f)])
    assert result.exit_code == 0


def test_checksum_valid(tmp_path):
    f = tmp_path / "test.txt"
    f.write_text("hello world")
    expected = hashlib.sha256(b"hello world").hexdigest()
    result = runner.invoke(app, ["checksum", str(f), expected])
    assert result.exit_code == 0
