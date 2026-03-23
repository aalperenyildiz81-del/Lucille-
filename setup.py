#!/usr/bin/env python3
"""
Lucille Setup and Installation Script
"""

import os
import sys
import subprocess
from pathlib import Path


def install_dependencies():
    """Install Python dependencies"""
    print("[*] Installing Python dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("[+] Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[-] Failed to install dependencies: {e}")
        return False


def setup_directories():
    """Create necessary directories"""
    print("[*] Setting up directories...")
    directories = [
        "results",
        "results/workspaces",
        "config",
        "data/wordlists",
        "data/templates",
        "data/plugins",
        "logs"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"[+] Created directory: {directory}")


def check_requirements():
    """Check system requirements"""
    print("[*] Checking system requirements...")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("[-] Python 3.8+ required")
        return False
    
    print(f"[+] Python version: {sys.version.split()[0]}")
    
    # Check required commands
    required_commands = ["nmap"]
    optional_commands = ["whois", "dig"]
    
    for cmd in required_commands:
        if os.system(f"which {cmd} > /dev/null 2>&1") != 0:
            print(f"[-] Required command not found: {cmd}")
            print(f"    Install with: apt-get install {cmd} (Debian/Ubuntu) or brew install {cmd} (macOS)")
            return False
        print(f"[+] Found command: {cmd}")
    
    for cmd in optional_commands:
        if os.system(f"which {cmd} > /dev/null 2>&1") != 0:
            print(f"[!] Optional command not found: {cmd} (some features may be limited)")
        else:
            print(f"[+] Found optional command: {cmd}")
    
    return True


def setup_configuration():
    """Setup configuration files"""
    print("[*] Setting up configuration...")
    
    config_file = Path("config/lucille.conf")
    if not config_file.exists():
        print("[+] Configuration file created")
    else:
        print("[+] Configuration file already exists")


def test_installation():
    """Test installation"""
    print("\n[*] Testing installation...")
    
    try:
        import src.core.engine
        import src.ui.terminal
        import src.core.config
        print("[+] Core modules imported successfully")
        
        # Try to instantiate main components
        from src.core.engine import LucilleEngine
        from src.core.config import ConfigManager
        
        engine = LucilleEngine()
        config = ConfigManager()
        
        print("[+] Engine and Config initialized successfully")
        print(f"[+] Available modules: {len(engine.list_modules())}")
        
        return True
    except Exception as e:
        print(f"[-] Installation test failed: {e}")
        return False


def main():
    """Run setup"""
    print("=" * 60)
    print("LUCILLE - Setup and Installation")
    print("=" * 60 + "\n")
    
    # Check requirements
    if not check_requirements():
        print("\n[-] System requirements not met")
        sys.exit(1)
    
    # Setup directories
    setup_directories()
    
    # Setup configuration
    setup_configuration()
    
    # Install dependencies
    if not install_dependencies():
        print("\n[-] Failed to install dependencies")
        sys.exit(1)
    
    # Test installation
    print()
    if not test_installation():
        print("\n[-] Installation test failed")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("[+] Installation completed successfully!")
    print("=" * 60)
    print("\nNext steps:")
    print("  1. Configure API keys in config/lucille.conf")
    print("  2. Run: python lucille.py --help")
    print("  3. Start scanning: python lucille.py scan -t example.com")
    print("\nFor interactive mode: python lucille.py console")
    print()


if __name__ == "__main__":
    main()
