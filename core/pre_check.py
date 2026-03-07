import os
import ctypes
import socket
from rich.console import Console

console = Console()

def check_admin() -> bool:
    """Checks if the script is running with Administrator privileges."""
    try:
        is_admin = os.getuid() == 0
    except AttributeError:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    
    if is_admin:
        console.print("[green]✓ Administrator privileges detected.[/green]")
        return True
    else:
        console.print("[red]✗ This script requires Administrator privileges. Please run as Administrator.[/red]")
        return False

def check_internet(host="8.8.8.8", port=53, timeout=3) -> bool:
    """Checks for active internet connection."""
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        console.print("[green]✓ Internet connection verified.[/green]")
        return True
    except socket.error as ex:
        console.print(f"[red]✗ No internet connection detected ({ex}).[/red]")
        return False

def run_pre_checks() -> bool:
    """Runs all pre-installation checks."""
    console.print("\n[bold cyan]Running Pre-Installation Checks...[/bold cyan]")
    admin_ok = check_admin()
    if not admin_ok:
        return False
        
    net_ok = check_internet()
    if not net_ok:
        console.print("[yellow]! WARNING: Proceeding without internet may cause downloads to fail.[/yellow]")
    
    return True
