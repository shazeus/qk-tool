import os
import platform
import shutil
import socket
import subprocess

import typer
from rich.console import Console

from qk.utils.display import print_table, print_success, print_error, print_warning
from qk.utils.platform import get_platform, get_flush_dns_cmd, get_trash_cmd

app = typer.Typer()
console = Console()


@app.command()
def port(port_number: int):
    """Check what's using a port."""
    plat = get_platform()
    try:
        if plat == "windows":
            result = subprocess.run(["netstat", "-ano"], capture_output=True, text=True)
            lines = [l for l in result.stdout.splitlines() if f":{port_number}" in l]
        else:
            result = subprocess.run(["lsof", "-i", f":{port_number}"], capture_output=True, text=True)
            lines = result.stdout.strip().splitlines()
        if len(lines) <= 1 and not any(str(port_number) in l for l in lines):
            print_warning(f"Nothing is using port {port_number}.")
        else:
            for line in lines:
                console.print(line)
    except FileNotFoundError:
        print_error("Required command not found (lsof/netstat).")


@app.command("kill-port")
def kill_port(port_number: int):
    """Kill the process using a port."""
    plat = get_platform()
    try:
        if plat == "windows":
            result = subprocess.run(["netstat", "-ano"], capture_output=True, text=True)
            for line in result.stdout.splitlines():
                if f":{port_number}" in line and "LISTENING" in line:
                    pid = line.strip().split()[-1]
                    subprocess.run(["taskkill", "/PID", pid, "/F"], capture_output=True)
                    print_success(f"Killed process {pid} on port {port_number}.")
                    return
        else:
            result = subprocess.run(["lsof", "-ti", f":{port_number}"], capture_output=True, text=True)
            pids = result.stdout.strip().split()
            if not pids or pids == [""]:
                print_warning(f"Nothing is using port {port_number}.")
                return
            for pid in pids:
                subprocess.run(["kill", "-9", pid])
            print_success(f"Killed process(es) on port {port_number}.")
    except FileNotFoundError:
        print_error("Required command not found.")


def _get_local_ip() -> str:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        try:
            return socket.gethostbyname(socket.gethostname())
        except Exception:
            return "Could not determine"


@app.command()
def ip():
    """Show public and local IP addresses."""
    local_ip = _get_local_ip()
    try:
        import requests
        public_ip = requests.get("https://api.ipify.org", timeout=5).text
    except Exception:
        public_ip = "Could not determine (offline?)"
    print_table("IP Addresses", ["Type", "Address"], [["Local", local_ip], ["Public", public_ip]])


@app.command("flush-dns")
def flush_dns():
    """Flush DNS cache."""
    cmd = get_flush_dns_cmd()
    try:
        subprocess.run(cmd, capture_output=True, text=True, check=True)
        print_success("DNS cache flushed.")
    except subprocess.CalledProcessError:
        print_error("Failed to flush DNS. May need sudo/admin privileges.")
    except FileNotFoundError:
        print_error("Required command not found.")


@app.command()
def trash():
    """Empty the trash/recycle bin."""
    cmd = get_trash_cmd()
    confirm = typer.confirm("Empty trash? This cannot be undone")
    if not confirm:
        return
    try:
        subprocess.run(cmd, capture_output=True, text=True, check=True)
        print_success("Trash emptied.")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print_error("Failed to empty trash.")


@app.command()
def info():
    """Show system information summary."""
    disk = shutil.disk_usage("/")
    rows = [
        ["OS", f"{platform.system()} {platform.release()}"],
        ["Architecture", platform.machine()],
        ["Hostname", platform.node()],
        ["Python", platform.python_version()],
        ["CPU Cores", str(os.cpu_count() or "Unknown")],
        ["Disk Total", f"{disk.total / (1024**3):.1f} GB"],
        ["Disk Used", f"{disk.used / (1024**3):.1f} GB ({disk.used * 100 // disk.total}%)"],
        ["Disk Free", f"{disk.free / (1024**3):.1f} GB"],
    ]
    print_table("System Info", ["Property", "Value"], rows)
