from qk.config import get_data_dir, load_config, save_config, is_module_enabled, DEFAULT_CONFIG


def test_get_data_dir(tmp_path, monkeypatch):
    monkeypatch.setenv("QK_DATA_DIR", str(tmp_path / ".qk"))
    data_dir = get_data_dir()
    assert data_dir == tmp_path / ".qk"


def test_load_config_creates_default(tmp_path, monkeypatch):
    monkeypatch.setenv("QK_DATA_DIR", str(tmp_path / ".qk"))
    config = load_config()
    assert config == DEFAULT_CONFIG


def test_save_and_load_config(tmp_path, monkeypatch):
    monkeypatch.setenv("QK_DATA_DIR", str(tmp_path / ".qk"))
    custom = {"modules": {"save": True, "system": False}}
    save_config(custom)
    loaded = load_config()
    assert loaded["modules"]["system"] is False


def test_is_module_enabled(tmp_path, monkeypatch):
    monkeypatch.setenv("QK_DATA_DIR", str(tmp_path / ".qk"))
    config = {"modules": {"save": True, "system": False}}
    save_config(config)
    assert is_module_enabled("save") is True
    assert is_module_enabled("system") is False


def test_is_module_enabled_default_true(tmp_path, monkeypatch):
    monkeypatch.setenv("QK_DATA_DIR", str(tmp_path / ".qk"))
    assert is_module_enabled("save") is True
