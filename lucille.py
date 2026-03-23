"""
Lucille - Advanced Security Reconnaissance Framework
Main entry point and command-line interface
"""

import os
import sys
import click
import json
from pathlib import Path
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress
from typing import List, Dict, Optional

from src.core.engine import LucilleEngine
from src.core.config import ConfigManager
from src.ui.terminal import TerminalUI


console = Console()

# ASCII Art Banner
BANNER = r"""
   _                _ _ _      
  | |              (_) | |     
  | |     _   _  ___ _| | | ___ 
  | |    | | | |/ __| | | |/ _ \
  | |____| |_| | (__| | | |  __/
  |_____|\__,_|\___|_|_|_|\___|
                                

    Advanced Reconnaissance Framework
    Terminal-Based • Modular • Powerful
    
"""


class Lucille:
    """Main Lucille Framework Controller"""
    
    def __init__(self):
        self.engine = LucilleEngine()
        self.config = ConfigManager()
        self.ui = TerminalUI()
        self.targets = []
        self.results = {}
        
    def show_banner(self):
        """Display welcome banner"""
        console.print(BANNER, style="cyan bold")
        console.print(f"[bold green]v1.0.0[/bold green] - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n", justify="center")


@click.group()
@click.pass_context
def cli(ctx):
    """
    Lucille - Advanced Security Reconnaissance Framework
    
    Terminal-based reconnaissance and vulnerability scanning framework
    combining the power of automated reconnaissance, web scanning, and OSINT.
    """
    ctx.ensure_object(dict)
    ctx.obj['lucille'] = Lucille()


@cli.command()
@click.option('-t', '--target', multiple=True, help='Target host(s) or IP address(es)')
@click.option('-f', '--file', type=click.File('r'), help='Read targets from file')
@click.option('-m', '--modules', default='all', help='Modules to execute (comma-separated)')
@click.option('--parallel', type=int, default=3, help='Number of parallel threads')
@click.option('--timeout', type=int, default=30, help='Timeout per scan (seconds)')
@click.option('-o', '--output', type=click.File('w'), help='Output file')
@click.option('--format', type=click.Choice(['json', 'csv', 'html', 'txt']), default='json')
@click.option('--full', is_flag=True, help='Run full comprehensive scan')
@click.option('--quick', is_flag=True, help='Run quick initial assessment')
@click.pass_context
def scan(ctx, target, file, modules, parallel, timeout, output, format, full, quick):
    """
    Scan target(s) with specified modules
    
    Examples:
        lucille scan -t example.com
        lucille scan -t example.com,another.com --full
        lucille scan -f targets.txt -m port_scan,web_scan
    """
    lucille = ctx.obj['lucille']
    lucille.show_banner()
    
    # Gather targets
    targets_list = list(target) if target else []
    if file:
        targets_list.extend([line.strip() for line in file if line.strip()])
    
    if not targets_list:
        console.print("[red]✗ No targets specified![/red]")
        console.print("Use -t or -f to specify targets")
        return
    
    console.print(f"[bold blue]📍 Targets:[/bold blue] {', '.join(targets_list)}\n")
    
    # Determine mode and modules
    if full:
        modules_to_run = 'all'
        mode = "FULL"
    elif quick:
        modules_to_run = 'quick'
        mode = "QUICK"
    else:
        modules_to_run = modules
        mode = "CUSTOM"
    
    console.print(f"[bold]Mode:[/bold] {mode} | [bold]Modules:[/bold] {modules_to_run}")
    console.print(f"[bold]Threads:[/bold] {parallel} | [bold]Timeout:[/bold] {timeout}s\n")
    
    # Execute scans
    console.print("[bold cyan]▶ Starting reconnaissance...[/bold cyan]\n")
    
    try:
        with Progress() as progress:
            for target_host in targets_list:
                task = progress.add_task(f"Scanning {target_host}", total=100)
                
                # Run scan
                results = lucille.engine.scan(
                    target=target_host,
                    modules=modules_to_run,
                    parallel=parallel,
                    timeout=timeout
                )
                
                lucille.results[target_host] = results
                progress.update(task, completed=100)
        
        console.print("\n[bold green]✓ Scans completed![/bold green]\n")
        
        # Display results summary
        lucille.ui.show_results_summary(lucille.results)
        
        # Export if requested
        if output:
            lucille.ui.export_results(lucille.results, output, format)
            console.print(f"\n[bold green]✓ Results exported to {output.name}[/bold green]")
            
    except Exception as e:
        console.print(f"\n[red]✗ Error during scan: {str(e)}[/red]")


@cli.command()
@click.option('-w', '--workspace', required=True, help='Workspace name')
@click.option('-t', '--target', help='Add target to workspace')
@click.option('-d', '--delete', is_flag=True, help='Delete workspace')
@click.option('--list', 'list_workspaces', is_flag=True, help='List all workspaces')
@click.pass_context
def workspace(ctx, workspace, target, delete, list_workspaces):
    """Manage workspaces"""
    lucille = ctx.obj['lucille']
    lucille.show_banner()
    
    if list_workspaces:
        console.print("[bold cyan]📁 Workspaces:[/bold cyan]\n")
        workspaces_path = Path("results/workspaces")
        if workspaces_path.exists():
            table = Table(show_header=True, header_style="bold blue")
            table.add_column("Workspace")
            table.add_column("Targets")
            table.add_column("Created")
            
            for ws in workspaces_path.iterdir():
                if ws.is_dir():
                    targets_count = len(list(ws.glob("*/scan.json")))
                    created = datetime.fromtimestamp(ws.stat().st_ctime).strftime("%Y-%m-%d %H:%M")
                    table.add_row(ws.name, str(targets_count), created)
            
            console.print(table)
        else:
            console.print("[yellow]No workspaces found[/yellow]")
        return
    
    if delete:
        if lucille.engine.delete_workspace(workspace):
            console.print(f"[green]✓ Workspace '{workspace}' deleted[/green]")
        else:
            console.print(f"[red]✗ Failed to delete workspace '{workspace}'[/red]")
        return
    
    if target:
        if lucille.engine.add_to_workspace(workspace, target):
            console.print(f"[green]✓ Target '{target}' added to workspace '{workspace}'[/green]")
        else:
            console.print(f"[red]✗ Failed to add target[/red]")
        return
    
    console.print(f"[cyan]Workspace: {workspace}[/cyan]")


@cli.command()
@click.option('-w', '--workspace', help='Workspace name')
@click.option('--format', type=click.Choice(['json', 'csv', 'html', 'txt']), default='json')
@click.option('-o', '--output', help='Output file')
@click.pass_context
def export(ctx, workspace, format, output):
    """Export scan results"""
    lucille = ctx.obj['lucille']
    lucille.show_banner()
    
    if not workspace:
        console.print("[red]✗ Workspace name required[/red]")
        return
    
    try:
        data = lucille.engine.export_workspace(workspace, format)
        
        if output:
            output_path = Path(output)
            output_path.write_text(data if format == 'json' else str(data))
            console.print(f"[green]✓ Exported to {output}[/green]")
        else:
            console.print(data)
            
    except Exception as e:
        console.print(f"[red]✗ Export failed: {str(e)}[/red]")


@cli.command()
@click.pass_context
def console_mode(ctx):
    """
    Interactive console mode
    
    Commands:
        target <host>          Set target
        scan [--full|--quick]  Execute scan
        results                Show results
        export <format>        Export results
        history                Show scan history
        help                   Show help
        exit                   Exit console
    """
    lucille = ctx.obj['lucille']
    lucille.show_banner()
    
    console.print("[bold cyan]Entering interactive console mode...[/bold cyan]\n")
    console.print("[yellow]Type 'help' for commands or 'exit' to quit\n[/yellow]")
    
    current_target = None
    scan_history = []
    
    while True:
        try:
            user_input = console.input("[bold cyan]lucille>[/bold cyan] ").strip()
            
            if not user_input:
                continue
            
            parts = user_input.split()
            command = parts[0].lower()
            
            if command == 'exit':
                console.print("[yellow]Goodbye![/yellow]")
                break
            
            elif command == 'target':
                if len(parts) > 1:
                    current_target = parts[1]
                    console.print(f"[green]✓ Target set to: {current_target}[/green]")
                else:
                    console.print(f"[cyan]Current target: {current_target or 'None'}[/cyan]")
            
            elif command == 'scan':
                if not current_target:
                    console.print("[red]✗ No target set[/red]")
                    continue
                
                mode = "--full" in user_input
                console.print(f"[cyan]Scanning {current_target}... (this may take a while)[/cyan]")
                # Scan execution
                result = lucille.engine.scan(current_target, 'all' if mode else 'quick')
                scan_history.append({'target': current_target, 'time': datetime.now(), 'result': result})
                console.print("[green]✓ Scan completed![/green]")
            
            elif command == 'results':
                if scan_history:
                    table = Table(show_header=True, header_style="bold blue")
                    table.add_column("Target")
                    table.add_column("Time")
                    table.add_column("Status")
                    for entry in scan_history:
                        table.add_row(entry['target'], entry['time'].strftime("%H:%M:%S"), "✓ Complete")
                    console.print(table)
                else:
                    console.print("[yellow]No results yet[/yellow]")
            
            elif command == 'help':
                console.print(Panel("""
[bold]Available Commands:[/bold]

[cyan]target <host>[/cyan]           Set target host
[cyan]scan [--full|--quick][/cyan]   Run scan (full or quick mode)
[cyan]results[/cyan]                 Display previous scan results
[cyan]export <format>[/cyan]        Export results (json/csv/html/txt)
[cyan]history[/cyan]                Show scan history
[cyan]modules[/cyan]                List available modules
[cyan]config[/cyan]                 Show configuration
[cyan]help[/cyan]                   Show this help
[cyan]exit[/cyan]                   Exit console

[yellow]Examples:[/yellow]
  > target example.com
  > scan --full
  > export json
                """, title="Lucille Console Help"))
            
            elif command == 'modules':
                console.print("[bold]Available Modules:[/bold]\n")
                modules_list = lucille.engine.list_modules()
                for module in modules_list:
                    console.print(f"  [cyan]•[/cyan] {module}")
            
            elif command == 'config':
                console.print("[bold]Current Configuration:[/bold]\n")
                config = lucille.config.get_all()
                for key, value in config.items():
                    console.print(f"  {key}: {value}")
            
            else:
                console.print(f"[red]Unknown command: {command}[/red]. Type 'help' for available commands.")
        
        except KeyboardInterrupt:
            console.print("\n[yellow]Interrupted. Type 'exit' to quit.[/yellow]")
        except Exception as e:
            console.print(f"[red]Error: {str(e)}[/red]")


@cli.command()
@click.pass_context
def modules(ctx):
    """List all available modules"""
    lucille = ctx.obj['lucille']
    lucille.show_banner()
    
    console.print("[bold cyan]📦 Available Modules:[/bold cyan]\n")
    
    modules_info = lucille.engine.list_modules(detailed=True)
    
    table = Table(show_header=True, header_style="bold blue")
    table.add_column("Module")
    table.add_column("Description")
    table.add_column("Category")
    table.add_column("Status")
    
    for module_name, info in modules_info.items():
        status = "[green]✓[/green]" if info.get('enabled', True) else "[yellow]⊘[/yellow]"
        table.add_row(
            module_name,
            info.get('description', 'N/A'),
            info.get('category', 'Core'),
            status
        )
    
    console.print(table)


@cli.command()
@click.option('--check-deps', is_flag=True, help='Check dependencies')
@click.pass_context
def status(ctx, check_deps):
    """Show Lucille status and system information"""
    lucille = ctx.obj['lucille']
    lucille.show_banner()
    
    info_table = Table(show_header=False, box=None)
    info_table.add_row("[bold cyan]Framework Version:[/bold cyan]", "[green]1.0.0[/green]")
    info_table.add_row("[bold cyan]Python Version:[/bold cyan]", f"[green]{sys.version.split()[0]}[/green]")
    info_table.add_row("[bold cyan]OS:[/bold cyan]", f"[green]{sys.platform}[/green]")
    info_table.add_row("[bold cyan]Available Modules:[/bold cyan]", f"[green]{len(lucille.engine.list_modules())}[/green]")
    
    console.print(info_table)
    
    if check_deps:
        console.print("\n[bold cyan]Checking dependencies...[/bold cyan]\n")
        deps_status = lucille.engine.check_dependencies()
        
        for dep, status in deps_status.items():
            status_icon = "[green]✓[/green]" if status else "[red]✗[/red]"
            console.print(f"  {status_icon} {dep}")


if __name__ == '__main__':
    cli(obj={})
