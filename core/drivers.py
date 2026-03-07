import os
import json
from rich.console import Console
from rich.table import Table
from .utils import run_powershell

console = Console()

def check_missing_drivers() -> list[dict]:
    """Uses PowerShell to query WMI for devices with missing drivers (ConfigManagerErrorCode != 0)."""
    console.print("\n[bold cyan]Checking for missing drivers...[/bold cyan]")
    
    # PowerShell command to get devices with error codes
    script = """
    Get-WmiObject Win32_PnPEntity | Where-Object { $_.ConfigManagerErrorCode -ne 0 } | Select-Object Name, DeviceID, ConfigManagerErrorCode | ConvertTo-Json
    """
    code, stdout, stderr = run_powershell(script)
    
    if code != 0:
        console.print(f"[red]✗ Failed to query drivers. Error: {stderr.strip()}[/red]")
        return []
    
    if not stdout.strip() or stdout.strip() == "null":
        console.print("[green]✓ All devices have proper drivers installed. No errors found.[/green]")
        return []
        
    try:
        data = json.loads(stdout)
        if isinstance(data, dict):
            # ConvertTo-Json returns dict if single item
            data = [data]
            
        if data:
            console.print(f"[yellow]! Found {len(data)} device(s) with missing or faulty drivers:[/yellow]")
            table = Table(title="Problematic Devices", style="red")
            table.add_column("Device Name", style="cyan", no_wrap=False)
            table.add_column("Device ID", style="magenta", no_wrap=False)
            table.add_column("Error Code", style="red", justify="center")
            
            for item in data:
                table.add_row(
                    str(item.get("Name", "Unknown")),
                    str(item.get("DeviceID", "Unknown")),
                    str(item.get("ConfigManagerErrorCode", "Unknown"))
                )
            console.print(table)
        return data
    except json.JSONDecodeError:
        console.print(f"[red]✗ Failed to parse output. Output was: {stdout}[/red]")
        return []
