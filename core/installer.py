from rich.console import Console
from .utils import run_powershell

console = Console()

def is_winget_available() -> bool:
    """Checks if Winget is installed and available in the system."""
    code, out, err = run_powershell("winget --version")
    return code == 0

def install_app(app_id: str, app_name: str) -> bool:
    """Installs an application using Winget."""
    console.print(f"[cyan]Installing {app_name} ({app_id})...[/cyan]")
    command = f"winget install --id {app_id} -e --accept-package-agreements --accept-source-agreements --silent"
    
    code, stdout, stderr = run_powershell(command)
    
    if code == 0:
        console.print(f"[green]✓ {app_name} installed successfully.[/green]")
        return True
    elif "No applicable update found" in stdout or "has already been installed" in stdout:
        console.print(f"[yellow]✓ {app_name} is already installed.[/yellow]")
        return True
    else:
        console.print(f"[red]✗ Failed to install {app_name}. Error: {stderr}[/red]")
        console.print(f"[dim]{stdout}[/dim]")
        return False

def install_applications(apps: dict) -> None:
    """Iterates through a dictionary of app IDs and names to install them."""
    console.print("\n[bold cyan]Starting Application Installation...[/bold cyan]")
    
    if not is_winget_available():
        console.print("[bold red]✗ Winget is not available on this system. Cannot install applications.[/bold red]")
        return

    for app_id, app_name in apps.items():
        try:
            install_app(app_id, app_name)
        except Exception as e:
            console.print(f"[red]✗ Unexpected error during {app_name} installation: {e}[/red]")
