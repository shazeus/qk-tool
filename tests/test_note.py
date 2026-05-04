from typer.testing import CliRunner
from qk.modules.note import app, _load_notes

runner = CliRunner()


def test_add_note(tmp_path, monkeypatch):
    monkeypatch.setenv("QK_DATA_DIR", str(tmp_path / ".qk"))
    result = runner.invoke(app, ["add", "meeting at 3pm", "--tag", "work"])
    assert result.exit_code == 0
    notes = _load_notes()
    assert len(notes) == 1
    assert notes[0]["content"] == "meeting at 3pm"


def test_list_notes(tmp_path, monkeypatch):
    monkeypatch.setenv("QK_DATA_DIR", str(tmp_path / ".qk"))
    runner.invoke(app, ["add", "note one", "--tag", "a"])
    runner.invoke(app, ["add", "note two", "--tag", "b"])
    result = runner.invoke(app, ["list"])
    assert "note one" in result.output
    assert "note two" in result.output


def test_list_filter_tag(tmp_path, monkeypatch):
    monkeypatch.setenv("QK_DATA_DIR", str(tmp_path / ".qk"))
    runner.invoke(app, ["add", "work note", "--tag", "work"])
    runner.invoke(app, ["add", "personal note", "--tag", "personal"])
    result = runner.invoke(app, ["list", "--tag", "work"])
    assert "work note" in result.output
    assert "personal note" not in result.output


def test_search_notes(tmp_path, monkeypatch):
    monkeypatch.setenv("QK_DATA_DIR", str(tmp_path / ".qk"))
    runner.invoke(app, ["add", "buy groceries"])
    result = runner.invoke(app, ["search", "groceries"])
    assert "buy groceries" in result.output


def test_remove_note(tmp_path, monkeypatch):
    monkeypatch.setenv("QK_DATA_DIR", str(tmp_path / ".qk"))
    runner.invoke(app, ["add", "delete me"])
    notes = _load_notes()
    note_id = notes[0]["id"]
    result = runner.invoke(app, ["remove", note_id])
    assert result.exit_code == 0
    assert len(_load_notes()) == 0


def test_export(tmp_path, monkeypatch):
    monkeypatch.setenv("QK_DATA_DIR", str(tmp_path / ".qk"))
    runner.invoke(app, ["add", "note alpha", "--tag", "x"])
    result = runner.invoke(app, ["export"])
    assert "note alpha" in result.output
    assert "#" in result.output
