from rich.console import Console
from .utils import run_powershell

console = Console()

def disable_telemetry() -> None:
    """Disables Windows Telemetry using PowerShell and Registry tweaks."""
    console.print("[cyan]Disabling Windows Telemetry...[/cyan]")
    script = """
    Set-ItemProperty -Path "HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows\\DataCollection" -Name "AllowTelemetry" -Type DWord -Value 0 -ErrorAction SilentlyContinue
    Stop-Service -Name "DiagTrack" -WarningAction SilentlyContinue -ErrorAction SilentlyContinue
    Set-Service -Name "DiagTrack" -StartupType Disabled -ErrorAction SilentlyContinue
    """
    code, _, err = run_powershell(script)
    if code == 0:
        console.print("[green]✓ Telemetry disabled successfully.[/green]")
    else:
        console.print(f"[yellow]! Failed to disable telemetry (admin rights might be missing).[/yellow]")

def set_high_performance() -> None:
    """Sets the Windows Power Plan to High Performance."""
    console.print("[cyan]Setting Power Plan to High Performance...[/cyan]")
    # High Performance GUID
    code, _, err = run_powershell("powercfg -setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c")
    if code == 0:
        console.print("[green]✓ Power plan set to High Performance.[/green]")
    else:
        console.print(f"[yellow]! Failed to set power plan: {err}[/yellow]")

def run_optimizations() -> None:
    """Runs all system optimizations sequentially."""
    console.print("\n[bold cyan]Running System Optimizations...[/bold cyan]")
    disable_telemetry()
    set_high_performance()
