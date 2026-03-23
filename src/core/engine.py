"""
Lucille Core Engine - Main scanning and handling logic
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import threading

from .config import ConfigManager
from .module_manager import ModuleManager


class LucilleEngine:
    """Main Lucille scanning engine"""
    
    def __init__(self):
        self.config = ConfigManager()
        self.module_manager = ModuleManager()
        self.lock = threading.Lock()
        self.results_dir = Path("results")
        self.results_dir.mkdir(exist_ok=True)
        
    def scan(self, target: str, modules: str = 'all', parallel: int = 3, timeout: int = 30) -> Dict[str, Any]:
        """
        Execute scan on target
        
        Args:
            target: Target host or IP
            modules: Modules to run ('all', 'quick', or comma-separated list)
            parallel: Number of parallel threads
            timeout: Timeout per module in seconds
            
        Returns:
            Dictionary with scan results
        """
        
        scan_result = {
            'target': target,
            'timestamp': datetime.now().isoformat(),
            'status': 'running',
            'modules': {},
            'summary': {},
            'vulnerabilities': [],
            'services': [],
            'technologies': []
        }
        
        # Determine which modules to run
        if modules == 'all':
            modules_to_run = self.module_manager.get_all_modules()
        elif modules == 'quick':
            modules_to_run = self.module_manager.get_quick_modules()
        else:
            modules_to_run = modules.split(',')
        
        # Execute modules in parallel
        with ThreadPoolExecutor(max_workers=parallel) as executor:
            futures = {}
            
            for module_name in modules_to_run:
                module = self.module_manager.get_module(module_name.strip())
                if module:
                    future = executor.submit(
                        self._run_module,
                        module,
                        target,
                        timeout
                    )
                    futures[future] = module_name.strip()
            
            # Collect results
            for future in as_completed(futures):
                module_name = futures[future]
                try:
                    result = future.result()
                    scan_result['modules'][module_name] = result
                except Exception as e:
                    scan_result['modules'][module_name] = {
                        'status': 'error',
                        'error': str(e)
                    }
        
        scan_result['status'] = 'completed'
        
        # Save results
        self._save_results(target, scan_result)
        
        return scan_result
    
    def _run_module(self, module: Any, target: str, timeout: int) -> Dict:
        """Execute a single module"""
        try:
            result = module.execute(target, timeout)
            return {
                'status': 'success',
                'data': result
            }
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def _save_results(self, target: str, results: Dict):
        """Save scan results to file"""
        target_dir = self.results_dir / target.replace('/', '_').replace(':', '_')
        target_dir.mkdir(exist_ok=True, parents=True)
        
        result_file = target_dir / f"scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        result_file.write_text(json.dumps(results, indent=2, default=str))
        
        # Also save a latest.json for quick access
        (target_dir / 'latest.json').write_text(json.dumps(results, indent=2, default=str))
    
    def add_to_workspace(self, workspace: str, target: str) -> bool:
        """Add target to workspace"""
        try:
            workspace_dir = self.results_dir / 'workspaces' / workspace
            workspace_dir.mkdir(exist_ok=True, parents=True)
            
            # Create target marker file
            target_file = workspace_dir / f"{target}.target"
            target_file.touch()
            
            return True
        except Exception as e:
            return False
    
    def delete_workspace(self, workspace: str) -> bool:
        """Delete workspace"""
        try:
            import shutil
            workspace_dir = self.results_dir / 'workspaces' / workspace
            if workspace_dir.exists():
                shutil.rmtree(workspace_dir)
            return True
        except Exception:
            return False
    
    def export_workspace(self, workspace: str, format: str = 'json') -> str:
        """Export workspace results"""
        workspace_dir = self.results_dir / 'workspaces' / workspace
        
        if not workspace_dir.exists():
            raise ValueError(f"Workspace '{workspace}' not found")
        
        # Collect all results from workspace
        all_results = {}
        for target_file in workspace_dir.glob("*.target"):
            target = target_file.stem
            target_results = self.results_dir / target
            if target_results.exists():
                latest = target_results / 'latest.json'
                if latest.exists():
                    all_results[target] = json.loads(latest.read_text())
        
        if format == 'json':
            return json.dumps(all_results, indent=2, default=str)
        elif format == 'csv':
            return self._results_to_csv(all_results)
        elif format == 'html':
            return self._results_to_html(all_results)
        else:
            return str(all_results)
    
    def _results_to_csv(self, results: Dict) -> str:
        """Convert results to CSV"""
        import csv
        from io import StringIO
        
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(['Target', 'Module', 'Status', 'Data'])
        
        for target, data in results.items():
            for module, module_data in data.get('modules', {}).items():
                status = module_data.get('status', 'unknown')
                writer.writerow([target, module, status, json.dumps(module_data)])
        
        return output.getvalue()
    
    def _results_to_html(self, results: Dict) -> str:
        """Convert results to HTML"""
        from jinja2 import Template
        
        template_str = """
        <html>
        <head>
            <title>Lucille Scan Results</title>
            <style>
                body { font-family: Arial; margin: 20px; }
                table { border-collapse: collapse; width: 100%; }
                th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                th { background-color: #4CAF50; color: white; }
                .success { color: green; }
                .error { color: red; }
            </style>
        </head>
        <body>
            <h1>Lucille Scan Results</h1>
            {% for target, data in results.items() %}
            <h2>{{ target }}</h2>
            <table>
                <tr><th>Module</th><th>Status</th></tr>
                {% for module, module_data in data.modules.items() %}
                <tr>
                    <td>{{ module }}</td>
                    <td class="{{ module_data.status }}">{{ module_data.status }}</td>
                </tr>
                {% endfor %}
            </table>
            {% endfor %}
        </body>
        </html>
        """
        
        template = Template(template_str)
        return template.render(results=results)
    
    def list_modules(self, detailed: bool = False) -> Any:
        """List available modules"""
        if detailed:
            return self.module_manager.get_all_modules_detailed()
        return self.module_manager.get_all_modules()
    
    def check_dependencies(self) -> Dict[str, bool]:
        """Check if required dependencies are available"""
        deps = {
            'nmap': self._check_command('nmap'),
            'python-nmap': self._check_import('nmap'),
            'requests': self._check_import('requests'),
            'beautifulsoup4': self._check_import('bs4'),
            'dnspython': self._check_import('dns'),
            'rich': self._check_import('rich'),
        }
        return deps
    
    def _check_command(self, cmd: str) -> bool:
        """Check if command exists"""
        import shutil
        return shutil.which(cmd) is not None
    
    def _check_import(self, module: str) -> bool:
        """Check if Python module can be imported"""
        try:
            __import__(module)
            return True
        except ImportError:
            return False
