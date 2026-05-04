from typer.testing import CliRunner
from qk.modules.clean import app

runner = CliRunner()


def test_big_files(tmp_path):
    (tmp_path / "small.txt").write_text("x")
    (tmp_path / "big.txt").write_text("x" * 10000)
    (tmp_path / "medium.txt").write_text("x" * 5000)
    result = runner.invoke(app, ["big", str(tmp_path), "--top", "2"])
    assert result.exit_code == 0
    assert "big.txt" in result.output


def test_duplicates_dry(tmp_path):
    (tmp_path / "a.txt").write_text("same content")
    (tmp_path / "b.txt").write_text("same content")
    (tmp_path / "c.txt").write_text("different")
    result = runner.invoke(app, ["duplicates", str(tmp_path), "--dry"])
    assert result.exit_code == 0
    assert "a.txt" in result.output or "b.txt" in result.output


def test_temp_dry(tmp_path, monkeypatch):
    monkeypatch.setenv("QK_TEMP_SCAN_DIR", str(tmp_path))
    (tmp_path / "file.tmp").write_text("temp")
    (tmp_path / "thumbs.db").write_text("thumbs")  # won't match Thumbs.db on case-sensitive FS
    (tmp_path / "real.txt").write_text("keep")
    result = runner.invoke(app, ["temp", "--dry"])
    assert result.exit_code == 0
