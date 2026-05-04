from typer.testing import CliRunner
from qk.modules.organize import app, _load_rules, _save_rules, DEFAULT_RULES

runner = CliRunner()


def test_default_rules_loaded(tmp_path, monkeypatch):
    monkeypatch.setenv("QK_DATA_DIR", str(tmp_path / ".qk"))
    rules = _load_rules()
    assert len(rules) > 0
    assert any(r["ext"] == ".pdf" for r in rules)


def test_add_rule(tmp_path, monkeypatch):
    monkeypatch.setenv("QK_DATA_DIR", str(tmp_path / ".qk"))
    result = runner.invoke(app, ["add-rule", ".xyz", "XYZFolder"])
    assert result.exit_code == 0
    rules = _load_rules()
    assert any(r["ext"] == ".xyz" for r in rules)


def test_remove_rule(tmp_path, monkeypatch):
    monkeypatch.setenv("QK_DATA_DIR", str(tmp_path / ".qk"))
    _save_rules(DEFAULT_RULES)
    rules = _load_rules()
    rule_id = rules[0]["id"]
    result = runner.invoke(app, ["remove-rule", rule_id])
    assert result.exit_code == 0


def test_run_dry(tmp_path, monkeypatch):
    monkeypatch.setenv("QK_DATA_DIR", str(tmp_path / ".qk"))
    source = tmp_path / "downloads"
    source.mkdir()
    (source / "report.pdf").write_text("pdf content")
    (source / "photo.jpg").write_text("jpg content")
    result = runner.invoke(app, ["run", str(source), "--dry"])
    assert result.exit_code == 0
    assert "report.pdf" in result.output
    assert (source / "report.pdf").exists()


def test_run_moves_files(tmp_path, monkeypatch):
    monkeypatch.setenv("QK_DATA_DIR", str(tmp_path / ".qk"))
    source = tmp_path / "downloads"
    source.mkdir()
    (source / "report.pdf").write_text("pdf content")
    result = runner.invoke(app, ["run", str(source)])
    assert result.exit_code == 0
    assert (source / "Documents" / "report.pdf").exists()
