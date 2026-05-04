import json
import os
from pathlib import Path

ALL_MODULES = ["save", "system", "organize", "convert", "note", "security", "clean", "text", "net"]

MODULE_DESCRIPTIONS = {
    "save": "Command saver",
    "system": "System actions (port, IP, DNS flush)",
    "organize": "File organizer",
    "convert": "Unit/format converter",
    "note": "Quick notes",
    "security": "Password & security tools",
    "clean": "System cleaner",
    "text": "Text processing",
    "net": "Network tools",
}

DEFAULT_CONFIG = {
    "modules": {mod: True for mod in ALL_MODULES},
}


def get_data_dir() -> Path:
    override = os.environ.get("QK_DATA_DIR")
    if override:
        return Path(override)
    return Path.home() / ".qk"


def _config_path() -> Path:
    return get_data_dir() / "config.json"


def load_config() -> dict:
    path = _config_path()
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return DEFAULT_CONFIG.copy()


def save_config(config: dict) -> None:
    path = _config_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(config, indent=2, ensure_ascii=False), encoding="utf-8")


def is_module_enabled(name: str) -> bool:
    config = load_config()
    return config.get("modules", {}).get(name, True)


def config_exists() -> bool:
    return _config_path().exists()
