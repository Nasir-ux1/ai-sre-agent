import sys
import argparse
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.syntax import Syntax
from rich.progress import Progress, SpinnerColumn, TextColumn
from ai_sre.agent import SREAgent

# Reconfigure standard output streams for UTF-8 compatibility on all Windows consoles
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

console = Console()

def run_interactive_cli(query: str):
    console.print(Panel(Text("AI-SRE Autonomous Linux Troubleshooting Agent", style="bold green", justify="center"), subtitle="v1.0.0"))
    
    if not query:
        console.print("[bold yellow]Please enter your system warning or issue query:[/bold yellow]")
        query = input("SRE > ")
        
    if not query.strip():
        console.print("[bold red]Empty query. Exiting diagnostics daemon.[/bold red]")
        return

    agent = SREAgent(mode="mock")
    
    console.print("\n[bold cyan][*] Launching Diagnostic Investigation Loop...[/bold cyan]")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True
    ) as progress:
        task1 = progress.add_task(description="Running local port check...", total=None)
        
        def trace(msg):
            progress.update(task1, description=msg)
            
        res = agent.run(query, trace_callback=trace)
        
    console.print("\n[bold green][OK] Diagnostic Audit Complete![/bold green]")
    
    # Render Analysis
    console.print("\n", Panel(
        Text(res["analysis"], style="white"),
        title="[bold red][Analysis] Root Cause Findings[/bold red]",
        border_style="red"
    ))
    
    # Render Bash Script
    syntax = Syntax(res["bash_fix"], "bash", theme="monokai", line_numbers=True)
    console.print("\n", Panel(
        syntax,
        title="[bold green][Safe-Fix] Recommended Bash Script[/bold green]",
        subtitle="Review before executing on production",
        border_style="green"
    ))
    
    # Render Explanation
    console.print("\n", Panel(
        Text(res["explanation"], style="yellow"),
        title="[bold yellow][Safety] Safe Execution Assurance[/bold yellow]",
        border_style="yellow"
    ))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI-SRE Troubleshooting Agent Command-Line Tool")
    parser.add_argument("query", type=str, nargs="?", default=None, help="The system error or issue query to diagnose")
    args = parser.parse_args()
    
    try:
        run_interactive_cli(args.query)
    except KeyboardInterrupt:
        console.print("\n[bold red]Audit interrupted by user. Exiting.[/bold red]")
        sys.exit(0)