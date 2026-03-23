"""
Configuration management for Lucille
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional


class ConfigManager:
    """Manage Lucille configuration"""
    
    DEFAULT_CONFIG = {
        'framework': {
            'version': '1.0.0',
            'name': 'Lucille',
            'parallel_threads': 3,
            'timeout': 30,
            'output_format': 'json'
        },
        'modules': {
            'enabled': ['port_scan', 'subdomain_enum', 'dns_recon', 'whois', 'web_scan'],
            'timeout': 30,
            'quick_modules': ['port_scan', 'web_scan']
        },
        'scanning': {
            'port_range': '1-65535',
            'common_ports': '22,80,443,3306,5432,8080,8443',
            'wordlist': 'data/wordlists/common.txt',
            'user_agent': 'Lucille/1.0'
        },
        'api': {
            'shodan_key': '',
            'virustotal_key': '',
            'hibp_enabled': True,
            'timeout': 10
        },
        'output': {
            'directory': 'results',
            'formats': ['json', 'csv', 'html', 'txt'],
            'include_details': True
        },
        'performance': {
            'cache_results': True,
            'cache_ttl': 86400,
            'parallel_limit': 10
        }
    }
    
    def __init__(self, config_path: str = 'config/lucille.conf'):
        self.config_path = Path(config_path)
        self.config = self.DEFAULT_CONFIG.copy()
        self.load_config()
    
    def load_config(self):
        """Load configuration from file"""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r') as f:
                    file_config = json.load(f)
                    # Deep merge with defaults
                    self.config = self._deep_merge(self.DEFAULT_CONFIG, file_config)
            except Exception as e:
                print(f"Warning: Could not load config file: {e}")
                self.config = self.DEFAULT_CONFIG.copy()
        else:
            self.save_config()
    
    def save_config(self):
        """Save configuration to file"""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=4)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default
        return value
    
    def set(self, key: str, value: Any):
        """Set configuration value"""
        keys = key.split('.')
        config = self.config
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        config[keys[-1]] = value
        self.save_config()
    
    def get_all(self) -> Dict:
        """Get all configuration"""
        return self.config.copy()
    
    def reset_to_defaults(self):
        """Reset configuration to defaults"""
        self.config = self.DEFAULT_CONFIG.copy()
        self.save_config()
    
    @staticmethod
    def _deep_merge(base: Dict, override: Dict) -> Dict:
        """Deep merge dictionaries"""
        result = base.copy()
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = ConfigManager._deep_merge(result[key], value)
            else:
                result[key] = value
        return result
