# Lucille - Usage Guide

## Table of Contents
1. [Quick Start](#quick-start)
2. [Command Reference](#command-reference)
3. [Advanced Usage](#advanced-usage)
4. [Configuration](#configuration)
5. [Modules](#modules)
6. [Examples](#examples)

---

## Quick Start

### Installation

```bash
# Clone or extract Lucille
cd Lucille

# Install dependencies
python setup.py

# Or manually
pip install -r requirements.txt
```

### First Scan

```bash
# Simple scan
python lucille.py scan -t example.com

# Full comprehensive scan
python lucille.py scan -t example.com --full

# Quick initial assessment
python lucille.py scan -t example.com --quick
```

---

## Command Reference

### Scan Command

```
lucille.py scan [OPTIONS]

OPTIONS:
  -t, --target TEXT             Target host or IP (can be used multiple times)
  -f, --file FILE              Read targets from file (one per line)
  -m, --modules TEXT           Modules to execute (comma-separated, default: all)
  -o, --output FILE            Output file path
  --format [json|csv|html|txt] Output format (default: json)
  --full                       Run full comprehensive scan
  --quick                      Run quick initial assessment
  --parallel INTEGER           Number of parallel threads (default: 3)
  --timeout INTEGER            Timeout per scan in seconds (default: 30)
```

#### Examples

```bash
# Scan single target
python lucille.py scan -t example.com

# Scan multiple targets
python lucille.py scan -t example.com -t another.com

# Scan from file
python lucille.py scan -f targets.txt

# Specific modules only
python lucille.py scan -t example.com -m port_scan,web_scan,ssl_cert

# Full scan with output
python lucille.py scan -t example.com --full -o results.json

# CSV output
python lucille.py scan -t example.com --full --format csv -o results.csv

# Parallel scanning
python lucille.py scan -f targets.txt --parallel 5 --timeout 60
```

### Workspace Command

```
lucille.py workspace [OPTIONS]

OPTIONS:
  -w, --workspace TEXT  Workspace name (required)
  -t, --target TEXT    Add target to workspace
  -d, --delete         Delete workspace
  --list               List all workspaces
```

#### Examples

```bash
# Create/add to workspace
python lucille.py workspace -w myproject -t example.com

# List workspaces
python lucille.py workspace --list

# Delete workspace
python lucille.py workspace -w myproject -d
```

### Export Command

```
lucille.py export [OPTIONS]

OPTIONS:
  -w, --workspace TEXT         Workspace name (required)
  --format [json|csv|html|txt] Export format (default: json)
  -o, --output TEXT           Output file path
```

#### Examples

```bash
# Export as JSON
python lucille.py export -w myproject --format json -o report.json

# Export as HTML
python lucille.py export -w myproject --format html -o report.html

# Export to stdout
python lucille.py export -w myproject --format csv
```

### Console Command

```
lucille.py console

Interactive console for real-time scanning and analysis
```

### Modules Command

```
lucille.py modules

List all available modules with descriptions
```

### Status Command

```
lucille.py status

Show Lucille status, version, and system information

--check-deps    Check all dependencies
```

---

## Advanced Usage

### Interactive Console Mode

```bash
python lucille.py console
```

Console commands:

```
lucille> target example.com
lucille> scan --full
lucille> results
lucille> export json results.json
lucille> modules
lucille> config
lucille> history
lucille> help
lucille> exit
```

### Workspace Management

Create organized scans by target:

```bash
# Create workspace for client project
python lucille.py workspace -w acme-corp -t acme.com
python lucille.py workspace -w acme-corp -t api.acme.com
python lucille.py workspace -w acme-corp -t mail.acme.com

# Run scans
python lucille.py scan -t acme.com --full
python lucille.py scan -t api.acme.com --full

# Export full project report
python lucille.py export -w acme-corp --format html -o acme-report.html
```

### Batch Scanning

Create targets file and scan:

```bash
# targets.txt
example.com
another.com
third-target.com
```

```bash
python lucille.py scan -f targets.txt --full --parallel 4
```

### Custom Module Selection

```bash
# Only reconnaissance modules
python lucille.py scan -t example.com -m port_scan,subdomain_enum,dns_recon

# Only vulnerability scanning
python lucille.py scan -t example.com -m web_scan,ssl_cert,header_analysis

# Specific workflow
python lucille.py scan -t example.com -m port_scan,web_scan,technology_id
```

---

## Configuration

Configuration file: `config/lucille.conf`

### API Keys

Add your API keys for enhanced scanning:

```json
{
  "api": {
    "shodan_key": "your_shodan_key",
    "virustotal_key": "your_virustotal_key",
    "censys_id": "your_censys_id",
    "censys_secret": "your_censys_secret"
  }
}
```

### Performance Tuning

```json
{
  "performance": {
    "parallel_threads": 5,
    "timeout": 60,
    "cache_results": true,
    "cache_ttl": 604800
  },
  "scanning": {
    "port_range": "1-65535",
    "threads": 10
  }
}
```

### Module Settings

Enable/disable specific modules:

```json
{
  "modules": {
    "enabled": [
      "port_scan",
      "web_scan",
      "subdomain_enum",
      "dns_recon"
    ],
    "quick_modules": [
      "port_scan",
      "web_scan"
    ]
  }
}
```

---

## Modules

### Built-in Modules

1. **port_scan** - Network port scanning and service detection
2. **subdomain_enum** - Subdomain discovery and enumeration
3. **dns_recon** - DNS records and zone information
4. **whois** - WHOIS information gathering
5. **web_scan** - HTTP/HTTPS vulnerability scanning
6. **ssl_cert** - SSL/TLS certificate analysis
7. **header_analysis** - HTTP header security review
8. **asset_search** - Shodan/Censys integration
9. **breach_check** - HaveIBeenPwned integration
10. **osint_gather** - Multi-source OSINT gathering
11. **technology_id** - Web technology fingerprinting
12. **directory_brute** - Web directory enumeration

### List Modules

```bash
python lucille.py modules
```

---

## Examples

### Scenario 1: Quick Website Assessment

```bash
python lucille.py scan -t mysite.com --quick
```

Runs quick modules for rapid assessment

### Scenario 2: Comprehensive Penetration Test

```bash
python lucille.py scan -t target.com --full --output pentest_report.json
```

Runs all modules with detailed output

### Scenario 3: Bug Bounty Reconnaissance

```bash
# Create workspace
python lucille.py workspace -w bounty-target -t target.com

# Run comprehensive scan
python lucille.py scan -t target.com --full

# Export findings
python lucille.py export -w bounty-target --format html -o bounty_findings.html
```

### Scenario 4: Continuous Monitoring

```bash
# Create workspace for target
python lucille.py workspace -w monitored -t critical-app.com

# Run scans periodically (via cron or scheduled task)
python lucille.py scan -t critical-app.com -m port_scan,web_scan

# Generate reports
python lucille.py export -w monitored --format html
```

### Scenario 5: Internal Network Assessment

```bash
# Create targets file with internal IPs
cat > internal_targets.txt << EOF
192.168.1.10
192.168.1.20
192.168.1.50
EOF

# Scan all targets
python lucille.py scan -f internal_targets.txt --parallel 3

# High verbosity for detailed analysis
python lucille.py scan -t 192.168.1.10 --full --timeout 120
```

### Scenario 6: API Security Testing

```bash
python lucille.py scan -t api.example.com -m web_scan,header_analysis,ssl_cert

# Additional configurations for APIs
# Edit config/lucille.conf to add API-specific settings
```

---

## Tips & Tricks

1. **Performance**: Adjust `-parallel` option based on target infrastructure
2. **Timeouts**: Increase `--timeout` for slow networks
3. **Output**: Use JSON for programmatic processing, HTML for reports
4. **Caching**: Enable in config to avoid re-scanning same targets
5. **Logging**: Check logs for detailed execution information
6. **Filters**: Use module selection to focus on specific areas
7. **Workspaces**: Organize different projects/clients
8. **Batch Mode**: Use file input for mass scanning

---

## Troubleshooting

### Dependencies Issue

```bash
# Reinstall all dependencies
pip install --upgrade -r requirements.txt

# Check specific modules
python -c "import nmap"
python -c "import dns.resolver"
```

### Permission Denied

Ensure script is executable:

```bash
chmod +x lucille.py
chmod +x setup.py
```

### Network Issues

Try with longer timeout:

```bash
python lucille.py scan -t example.com --timeout 60
```

### Memory Issues

Reduce parallel threads:

```bash
python lucille.py scan -f targets.txt --parallel 1 --timeout 30
```

---

## Legal Notice

Lucille should only be used for authorized security testing. Ensure you have proper authorization before scanning any target.

---

For more information visit: [GitHub repository]
