from typer.testing import CliRunner
from qk.modules.save import app, _load_saves

runner = CliRunner()


def test_add_command(tmp_path, monkeypatch):
    monkeypatch.setenv("QK_DATA_DIR", str(tmp_path / ".qk"))
    result = runner.invoke(app, ["add", "list containers", "docker ps -a", "--tag", "docker"])
    assert result.exit_code == 0
    saves = _load_saves()
    assert len(saves) == 1
    assert saves[0]["description"] == "list containers"
    assert saves[0]["command"] == "docker ps -a"
    assert "docker" in saves[0]["tags"]


def test_list_commands(tmp_path, monkeypatch):
    monkeypatch.setenv("QK_DATA_DIR", str(tmp_path / ".qk"))
    runner.invoke(app, ["add", "test cmd", "echo hi", "--tag", "misc"])
    result = runner.invoke(app, ["list"])
    assert result.exit_code == 0
    assert "test cmd" in result.output


def test_list_filter_by_tag(tmp_path, monkeypatch):
    monkeypatch.setenv("QK_DATA_DIR", str(tmp_path / ".qk"))
    runner.invoke(app, ["add", "docker cmd", "docker ps", "--tag", "docker"])
    runner.invoke(app, ["add", "git cmd", "git log", "--tag", "git"])
    result = runner.invoke(app, ["list", "--tag", "docker"])
    assert "docker cmd" in result.output
    assert "git cmd" not in result.output


def test_search(tmp_path, monkeypatch):
    monkeypatch.setenv("QK_DATA_DIR", str(tmp_path / ".qk"))
    runner.invoke(app, ["add", "remove all containers", "docker rm -f $(docker ps -aq)", "--tag", "docker"])
    result = runner.invoke(app, ["search", "container"])
    assert "remove all containers" in result.output


def test_remove(tmp_path, monkeypatch):
    monkeypatch.setenv("QK_DATA_DIR", str(tmp_path / ".qk"))
    runner.invoke(app, ["add", "test", "echo test", "--tag", "misc"])
    saves = _load_saves()
    save_id = saves[0]["id"]
    result = runner.invoke(app, ["remove", save_id])
    assert result.exit_code == 0
    assert len(_load_saves()) == 0
