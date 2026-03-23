# Lucille Architecture & Design

## Overview

Lucille is a modular, terminal-based reconnaissance and vulnerability scanning framework designed for security professionals. It combines automated reconnaissance capabilities with advanced scanning features in a cohesive package.

**Key Features:**
- Terminal-native UI (no web browser required)
- Modular scanner architecture
- Parallel execution
- Multiple output formats
- Workspace management
- Combining strengths of Sn1per, Nikto, and Recon-ng

---

## Architecture

```
┌─────────────────────────────────────────────────┐
│           LUCILLE COMMAND INTERFACE             │
│  (lucille.py - Click-based CLI)                 │
└────────────────┬────────────────────────────────┘
                 │
      ┌──────────┼──────────┐
      │          │          │
      v          v          v
 ┌────────┐ ┌────────┐ ┌────────┐
 │ Scan   │ │ Export │ │Console │
 │Command │ │Command │ │Command │
 └────────┘ └────────┘ └────────┘
      │          │          │
      └──────────┼──────────┘
                 │
      ┌──────────v────────────┐
      │  LUCILLE CORE ENGINE  │
      │  (engine.py)          │
      │  - Scan Orchestration │
      │  - Result Management  │
      │  - Workspace Handling │
      └──────────┬────────────┘
                 │
      ┌──────────v────────────────┐
      │   MODULE MANAGER          │
      │   (module_manager.py)     │
      │   - Module Loading        │
      │   - Module Execution      │
      │   - Module Selection      │
      └──────────┬────────────────┘
                 │
    ┌────────────┴────────────┐
    │ SCANNER MODULES         │
    │                         │
    ├─ PORT_SCAN            │
    ├─ SUBDOMAIN_ENUM       │
    ├─ DNS_RECON            │
    ├─ WEB_SCAN             │
    ├─ SSL_CERT             │
    ├─ HEADER_ANALYSIS      │
    ├─ TECHNOLOGY_ID        │
    ├─ ASSET_SEARCH         │
    ├─ BREACH_CHECK         │
    ├─ OSINT_GATHER         │
    └─ DIRECTORY_BRUTE      │
         │                   │
         └───────────┬───────┘
                     │
         ┌───────────v───────────┐
         │  EXTERNAL TOOLS       │
         │  - nmap              │
         │  - DNS resolvers     │
         │  - DNS transfers     │
         │  - HTTP clients      │
         │  - APIs              │
         └───────────────────────┘
```

---

## Directory Structure

```
Lucille/
├── lucille.py              # Main entry point & CLI
├── requirements.txt        # Python dependencies
├── setup.py               # Installation script
├── README.md              # Project overview
├── USAGE.md               # Usage guide
├── ARCHITECTURE.md        # This file
├── CONTRIBUTING.md        # Contributing guide
│
├── src/                   # Source code
│   ├── __init__.py
│   ├── core/             # Core framework
│   │   ├── __init__.py
│   │   ├── engine.py     # Main scanning engine
│   │   ├── config.py     # Configuration management
│   │   └── module_manager.py  # Module system
│   │
│   ├── modules/          # Scanner modules
│   │   ├── __init__.py
│   │   ├── advanced_scanners.py
│   │   └── [additional modules]
│   │
│   ├── ui/               # Terminal UI
│   │   ├── __init__.py
│   │   └── terminal.py   # Rich-based interface
│   │
│   └── utils/            # Utility functions
│       ├── __init__.py
│       ├── validators.py
│       ├── formatters.py
│       └── helpers.py
│
├── config/               # Configuration
│   └── lucille.conf     # Main configuration file
│
├── data/                # Data files
│   ├── wordlists/       # Scanning wordlists
│   │   └── common.txt
│   ├── templates/       # Report templates
│   └── plugins/         # Plugin directory
│
├── results/             # Scan results
│   ├── [targets]/
│   └── workspaces/     # Project workspaces
│
└── logs/               # Application logs
```

---

## Component Details

### 1. Core Engine (src/core/engine.py)

**Responsibilities:**
- Orchestrate scan execution
- Manage module execution (parallel)
- Handle result persistence
- Workspace management
- Export functionality

**Key Methods:**
```python
scan(target, modules, parallel, timeout)
_run_module(module, target, timeout)
_save_results(target, results)
add_to_workspace(workspace, target)
delete_workspace(workspace)
export_workspace(workspace, format)
```

### 2. Configuration Manager (src/core/config.py)

**Responsibilities:**
- Load/save configuration
- Manage API keys
- Application settings
- Default values

**Configuration Structure:**
```json
{
  "framework": {...},
  "modules": {...},
  "scanning": {...},
  "api": {...},
  "output": {...},
  "performance": {...}
}
```

### 3. Module Manager (src/core/module_manager.py)

**Responsibilities:**
- Dynamically load modules
- Manage module registry
- Enable/disable modules
- Execute modules

**Module Interface:**
```python
class LucilleModule:
    name: str
    description: str
    category: str
    enabled: bool
    
    def execute(target, timeout) -> Dict
```

### 4. Terminal UI (src/ui/terminal.py)

**Responsibilities:**
- Display results
- Format output
- Export to multiple formats
- Progress indication
- Interactive console

**Features:**
- Rich-based formatting
- Tables, panels, progress bars
- HTML/CSV/JSON/TXT export
- Color-coded messages

### 5. Scanner Modules (src/modules/)

Each module implements reconnaissance or scanning capability:

- **port_scan**: Network port discovery
- **subdomain_enum**: Subdomain enumeration
- **dns_recon**: DNS information gathering
- **web_scan**: Web vulnerability scanning
- **ssl_cert**: Certificate analysis
- And more...

---

## Data Flow

### Scan Execution Flow

```
1. User Input (CLI)
   ↓
2. Argument Parsing (Click)
   ↓
3. Target Validation
   ↓
4. Engine Initialization
   ↓
5. Module Selection
   ↓
6. Parallel Execution   ← ThreadPoolExecutor
   │
   ├─ Module 1
   ├─ Module 2
   ├─ Module 3
   └─ Module N
   ↓
7. Result Collection
   ↓
8. Result Persistence (JSON)
   ↓
9. UI Display
   ↓
10. Export (if requested)
```

### Module Execution

```
Module.execute(target, timeout)
├─ Connect to target/service
├─ Execute reconnaissance
├─ Parse responses
├─ Check for vulnerabilities
├─ Format results
└─ Return Dict[str, Any]
```

---

## Threading Model

**Parallel Execution:**
- Uses `ThreadPoolExecutor` (configurable pool size)
- Each module runs in separate thread
- Lock-protected result collection
- Timeout per module

**Configuration:**
```python
parallel = 3  # Number of threads
timeout = 30  # Timeout per module (seconds)

with ThreadPoolExecutor(max_workers=parallel) as executor:
    futures = {
        executor.submit(module.execute, target, timeout): name
        for name, module in modules.items()
    }
```

---

## Result Storage

**Structure:**
```
results/
├── example.com/
│   ├── scan_20240115_120000.json  # Timestamped scan
│   ├── scan_20240115_130000.json  # Another scan
│   └── latest.json                # Latest scan (symlink/copy)
│
└── workspaces/
    └── myproject/
        ├── example.com.target
        └── api.example.com.target
```

**Result Format:**
```json
{
  "target": "example.com",
  "timestamp": "2024-01-15T12:00:00",
  "status": "completed",
  "modules": {
    "port_scan": {
      "status": "success",
      "data": {...}
    },
    "web_scan": {
      "status": "success",
      "data": {...}
    }
  },
  "summary": {...},
  "vulnerabilities": [...],
  "services": [...],
  "technologies": [...]
}
```

---

## Integration Points

### External Tools
- **nmap**: Network scanning
- **dnspython**: DNS queries
- **requests**: HTTP/HTTPS
- **beautifulsoup4**: HTML parsing
- **rich**: Terminal UI

### External APIs
- **Shodan**: Asset discovery
- **VirusTotal**: Malware scanning
- **HaveIBeenPwned**: Breach database
- **Censys**: Asset inventory

---

## Extension Points

### Adding New Modules

1. Create module class inheriting from `LucilleModule`
2. Implement `execute()` method
3. Register in `ModuleManager`

```python
class MyModule(LucilleModule):
    name = "my_module"
    description = "My custom scanner"
    category = "custom"
    
    def execute(self, target: str, timeout: int) -> Dict:
        # Implementation
        return results
```

### Custom Plugins

Place Python files in `data/plugins/` directory

---

## Performance Considerations

- **Caching**: Results cached (configurable TTL)
- **Parallel Processing**: Configurable thread count
- **Memory**: Results streamed to disk
- **Timeouts**: Per-module timeout limits
- **Wordlist Size**: Configurable dictionary
- **Rate Limiting**: Built-in request throttling

---

## Security Considerations

- No HTTP-based interface (terminal only)
- API keys stored locally (encrypt in production)
- No remote code execution
- Input validation on targets
- SSL verification configurable
- Audit logging support

---

## Comparison with Similar Tools

| Feature | Sn1per | Nikto | Recon-ng | Lucille |
|---------|--------|-------|----------|---------|
| Terminal UI | ✓ | ✓ | ✓ | ✓+ |
| Web GUI | ~ | ✗ | ✓ | ✗ |
| Modular | ✓ | ✗ | ✓+ | ✓+ |
| Python | ~ | ✗ | ✓ | ✓ |
| Web Scanning | ✓ | ✓+ | ✗ | ✓ |
| OSINT | ✓ | ✗ | ✓+ | ✓ |
| Port Scan | ✓ | ✗ | ✗ | ✓ |
| Workspaces | ✓ | ✗ | ✓ | ✓ |
| Parallel | ✓ | ✗ | ✗ | ✓+ |

---

## Development Roadmap

- [ ] Add more scanner modules
- [ ] Database backend (PostgreSQL/SQLite)
- [ ] Report templates (CVSS scoring)
- [ ] Plugin system (Python plugins)
- [ ] Scheduled scans (cron support)
- [ ] API server (REST API)
- [ ] Distribution packages
- [ ] Docker support

---

## License & Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.

GPL-3.0 License

---

**Last Updated:** 2024-01-15
