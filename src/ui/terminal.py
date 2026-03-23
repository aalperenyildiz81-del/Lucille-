"""
Terminal UI components for Lucille using Rich library
"""

from typing import Dict, Any, TextIO
import json
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress
from rich import box
from datetime import datetime


class TerminalUI:
    """Terminal-based user interface for Lucille"""
    
    def __init__(self):
        self.console = Console()
    
    def show_results_summary(self, results: Dict[str, Any]):
        """Display scan results summary"""
        
        for target, result in results.items():
            panel = Panel.fit(
                f"[bold cyan]{target}[/bold cyan]\n"
                f"[dim]{result.get('timestamp', 'N/A')}[/dim]",
                title="Scan Result",
                border_style="blue"
            )
            self.console.print(panel)
            
            # Module results table
            modules_table = Table(show_header=True, header_style="bold blue", box=box.ROUNDED)
            modules_table.add_column("Module")
            modules_table.add_column("Status")
            modules_table.add_column("Details")
            
            for module_name, module_result in result.get('modules', {}).items():
                status = module_result.get('status', 'unknown')
                status_icon = self._get_status_icon(status)
                
                details = ""
                if status == 'success':
                    data = module_result.get('data', {})
                    details = self._format_module_data(module_name, data)
                else:
                    details = module_result.get('error', 'Unknown error')
                
                modules_table.add_row(
                    module_name,
                    f"{status_icon} {status}",
                    details or "[dim]N/A[/dim]"
                )
            
            self.console.print(modules_table)
            self.console.print()
    
    def export_results(self, results: Dict, output_file: TextIO, format: str):
        """Export results to file"""
        
        if format == 'json':
            output_file.write(json.dumps(results, indent=2, default=str))
        elif format == 'csv':
            self._export_csv(results, output_file)
        elif format == 'html':
            self._export_html(results, output_file)
        elif format == 'txt':
            self._export_txt(results, output_file)
    
    def _export_csv(self, results: Dict, output_file: TextIO):
        """Export as CSV"""
        import csv
        
        writer = csv.writer(output_file)
        writer.writerow(['Target', 'Module', 'Status', 'Data'])
        
        for target, result in results.items():
            for module_name, module_result in result.get('modules', {}).items():
                writer.writerow([
                    target,
                    module_name,
                    module_result.get('status', 'unknown'),
                    json.dumps(module_result.get('data', {}))
                ])
    
    def _export_html(self, results: Dict, output_file: TextIO):
        """Export as HTML"""
        from jinja2 import Template
        
        html_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Lucille Scan Report</title>
            <style>
                * { margin: 0; padding: 0; box-sizing: border-box; }
                body {
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background: #f5f5f5;
                    padding: 20px;
                }
                .container {
                    max-width: 1200px;
                    margin: 0 auto;
                    background: white;
                    padding: 30px;
                    border-radius: 8px;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                }
                h1 {
                    color: #333;
                    margin-bottom: 10px;
                    border-bottom: 3px solid #2196F3;
                    padding-bottom: 10px;
                }
                .timestamp {
                    color: #999;
                    font-size: 0.9em;
                    margin-bottom: 20px;
                }
                .target-section {
                    margin: 30px 0;
                    padding: 20px;
                    background: #f9f9f9;
                    border-left: 4px solid #2196F3;
                    border-radius: 4px;
                }
                .target-section h2 {
                    color: #2196F3;
                    margin-bottom: 15px;
                    font-size: 1.3em;
                }
                table {
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 15px;
                }
                th {
                    background: #2196F3;
                    color: white;
                    padding: 12px;
                    text-align: left;
                }
                td {
                    padding: 10px 12px;
                    border-bottom: 1px solid #ddd;
                }
                tr:hover {
                    background: #f0f0f0;
                }
                .status-success { color: #4CAF50; font-weight: bold; }
                .status-error { color: #f44336; font-weight: bold; }
                .status-running { color: #FF9800; font-weight: bold; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>⭐ Lucille Reconnaissance Report</h1>
                <p class="timestamp">Generated: {{ timestamp }}</p>
                
                {% for target, result in results.items() %}
                <div class="target-section">
                    <h2>Target: {{ target }}</h2>
                    <p>Scan Time: {{ result.timestamp }}</p>
                    <table>
                        <tr>
                            <th>Module</th>
                            <th>Status</th>
                            <th>Details</th>
                        </tr>
                        {% for module_name, module_data in result.modules.items() %}
                        <tr>
                            <td><strong>{{ module_name }}</strong></td>
                            <td class="status-{{ module_data.status }}">{{ module_data.status }}</td>
                            <td>
                                {% if module_data.status == 'success' %}
                                    <pre>{{ module_data.data | tojson(indent=2) }}</pre>
                                {% else %}
                                    <code>{{ module_data.error }}</code>
                                {% endif %}
                            </td>
                        </tr>
                        {% endfor %}
                    </table>
                </div>
                {% endfor %}
            </div>
        </body>
        </html>
        """
        
        template = Template(html_template)
        html_content = template.render(
            results=results,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        output_file.write(html_content)
    
    def _export_txt(self, results: Dict, output_file: TextIO):
        """Export as plain text"""
        
        output_file.write("=" * 80 + "\n")
        output_file.write("LUCILLE RECONNAISSANCE REPORT\n")
        output_file.write("=" * 80 + "\n\n")
        output_file.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        for target, result in results.items():
            output_file.write(f"\n{'─' * 80}\n")
            output_file.write(f"TARGET: {target}\n")
            output_file.write(f"Timestamp: {result.get('timestamp', 'N/A')}\n")
            output_file.write(f"{'─' * 80}\n\n")
            
            for module_name, module_result in result.get('modules', {}).items():
                status = module_result.get('status', 'unknown')
                output_file.write(f"\n[{module_name.upper()}] Status: {status}\n")
                
                if status == 'success':
                    data = module_result.get('data', {})
                    output_file.write(json.dumps(data, indent=2, default=str))
                else:
                    output_file.write(f"Error: {module_result.get('error', 'Unknown')}\n")
                
                output_file.write("\n")
    
    def show_progress(self, title: str, total: int = 100):
        """Show progress bar"""
        return Progress()
    
    def show_error(self, message: str):
        """Display error message"""
        self.console.print(f"[bold red]✗ Error:[/bold red] {message}")
    
    def show_success(self, message: str):
        """Display success message"""
        self.console.print(f"[bold green]✓ Success:[/bold green] {message}")
    
    def show_warning(self, message: str):
        """Display warning message"""
        self.console.print(f"[bold yellow]⚠ Warning:[/bold yellow] {message}")
    
    def show_info(self, message: str):
        """Display info message"""
        self.console.print(f"[bold blue]ℹ Info:[/bold blue] {message}")
    
    @staticmethod
    def _get_status_icon(status: str) -> str:
        """Get status icon"""
        icons = {
            'success': '[green]✓[/green]',
            'error': '[red]✗[/red]',
            'running': '[yellow]⟳[/yellow]',
            'completed': '[green]✓[/green]',
            'pending': '[dim]○[/dim]',
            'skipped': '[yellow]⊘[/yellow]'
        }
        return icons.get(status, '[dim]?[/dim]')
    
    @staticmethod
    def _format_module_data(module_name: str, data: Dict) -> str:
        """Format module output for display"""
        if not data:
            return "[dim]No data[/dim]"
        
        if module_name == 'port_scan':
            ports = data.get('open_ports', [])
            return f"ports: {len(ports)}"
        elif module_name == 'subdomain_enum':
            subs = data.get('subdomains', [])
            return f"subdomains: {len(subs)}"
        elif module_name == 'dns_recon':
            records = data.get('a_records', [])
            return f"A records: {len(records)}"
        elif module_name == 'web_scan':
            status = data.get('status_code', 'N/A')
            return f"status: {status}"
        else:
            return "[dim]Executed[/dim]"
