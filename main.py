import sys
import os
from rich.console import Console
from rich.panel import Panel

# Ensure the root directory is in the sys.path so we can import 'core'
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.pre_check import run_pre_checks

console = Console()


def main():
    console.clear()
    console.print(Panel.fit(
        "[bold magenta]TechDeploy Pro[/bold magenta]\n[cyan]Post-Installation Automation Tool v2.0[/cyan]",
        border_style="green"
    ))

    # 1. Pre-checks (Admin & Internet)
    if not run_pre_checks():
        console.print("\n[bold red]Terminating execution due to failed pre-checks.[/bold red]")
        sys.exit(1)

    # 2. Launch the full GUI (all features)
    console.print("\n[bold cyan]Launching TechDeploy Pro GUI...[/bold cyan]")
    try:
        from gui.main_gui import launch
        launch()
    except Exception as e:
        console.print(f"[bold red]Failed to launch GUI: {e}[/bold red]")
        sys.exit(1)

    console.print("\n[bold green]✓ TechDeploy Pro GUI closed.[/bold green]")
    console.print("[dim]Note: Some changes may require a restart to fully take effect.[/dim]")


if __name__ == "__main__":
    main()
