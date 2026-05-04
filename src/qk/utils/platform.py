import platform
from pathlib import Path


def get_platform() -> str:
    system = platform.system().lower()
    if system == "darwin":
        return "darwin"
    elif system == "windows":
        return "windows"
    return "linux"


def get_flush_dns_cmd() -> list[str]:
    plat = get_platform()
    if plat == "darwin":
        return ["sudo", "dscacheutil", "-flushcache"]
    elif plat == "windows":
        return ["ipconfig", "/flushdns"]
    return ["sudo", "systemd-resolve", "--flush-caches"]


def get_trash_cmd() -> list[str]:
    plat = get_platform()
    if plat == "darwin":
        return ["osascript", "-e", 'tell app "Finder" to empty trash']
    elif plat == "windows":
        return ["powershell", "-Command", "Clear-RecycleBin -Force"]
    return ["gio", "trash", "--empty"]


def get_temp_dirs() -> list[Path]:
    plat = get_platform()
    dirs = [Path("/tmp")]
    if plat == "darwin":
        dirs.append(Path.home() / "Library" / "Caches")
    elif plat == "windows":
        import tempfile
        dirs = [Path(tempfile.gettempdir())]
    return dirs
