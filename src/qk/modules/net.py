import socket
import subprocess
import time

import typer
from rich.console import Console

from qk.utils.display import print_table, print_error
from qk.utils.platform import get_platform

app = typer.Typer()
console = Console()


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


@app.command()
def check(url: str):
    """Check if a URL is reachable and measure response time."""
    try:
        import requests
        start = time.time()
        resp = requests.get(url, timeout=10)
        elapsed = (time.time() - start) * 1000
        print_table("Site Check", ["Property", "Value"], [
            ["URL", url],
            ["Status", str(resp.status_code)],
            ["Response Time", f"{elapsed:.0f} ms"],
        ])
    except Exception as e:
        print_error(f"Could not reach {url}: {e}")


@app.command()
def dns(domain: str):
    """Show DNS records for a domain."""
    try:
        ips = socket.getaddrinfo(domain, None)
        unique = list({addr[4][0] for addr in ips})
        rows = [[domain, addr] for addr in unique]
        print_table(f"DNS: {domain}", ["Domain", "IP Address"], rows)
    except socket.gaierror:
        print_error(f"Could not resolve {domain}")


@app.command()
def ping(host: str, count: int = typer.Option(4, help="Number of pings")):
    """Ping a host and show summary."""
    plat = get_platform()
    flag = "-n" if plat == "windows" else "-c"
    try:
        result = subprocess.run(
            ["ping", flag, str(count), host],
            capture_output=True, text=True, timeout=30,
        )
        console.print(result.stdout)
    except FileNotFoundError:
        print_error("ping command not found.")
    except subprocess.TimeoutExpired:
        print_error("Ping timed out.")


@app.command()
def speed():
    """Run a simple download speed test."""
    import requests
    url = "https://speed.cloudflare.com/__down?bytes=10000000"
    console.print("[dim]Testing download speed...[/dim]")
    try:
        start = time.time()
        resp = requests.get(url, timeout=30)
        elapsed = time.time() - start
        size_mb = len(resp.content) / (1024 * 1024)
        speed_mbps = (size_mb * 8) / elapsed
        print_table("Speed Test", ["Metric", "Value"], [
            ["Downloaded", f"{size_mb:.1f} MB"],
            ["Time", f"{elapsed:.1f} s"],
            ["Speed", f"{speed_mbps:.1f} Mbps"],
        ])
    except Exception as e:
        print_error(f"Speed test failed: {e}")
