.PHONY: help install setup clean test scan console modules status lint format

help:
	@echo "Lucille - Advanced Reconnaissance Framework"
	@echo ""
	@echo "Available commands:"
	@echo "  make install      - Install dependencies"
	@echo "  make setup        - Setup and configure"
	@echo "  make scan         - Run example scan"
	@echo "  make console      - Start interactive console"
	@echo "  make modules      - List available modules"
	@echo "  make status       - Show framework status"
	@echo "  make test         - Run tests"
	@echo "  make lint         - Check code style"
	@echo "  make format       - Format code"
	@echo "  make clean        - Clean temporary files"
	@echo "  make help         - Show this help"

install:
	@echo "[*] Installing Lucille..."
	pip install -r requirements.txt
	@echo "[+] Installation complete"

setup:
	@echo "[*] Setting up Lucille..."
	python setup.py
	@echo "[+] Setup complete"

scan:
	@echo "[*] Running example scan..."
	python lucille.py scan -t example.com --quick

scan-full:
	@echo "[*] Running full scan on example.com..."
	python lucille.py scan -t example.com --full

console:
	@echo "[*] Starting interactive Lucille console..."
	python lucille.py console

modules:
	@echo "[*] Listing available modules..."
	python lucille.py modules

status:
	@echo "[*] Checking framework status..."
	python lucille.py status --check-deps

test:
	@echo "[*] Running tests..."
	python -m pytest tests/ -v

lint:
	@echo "[*] Checking code style..."
	flake8 src/ lucille.py setup.py --max-line-length=120
	@echo "[+] Linting complete"

format:
	@echo "[*] Formatting code..."
	black src/ lucille.py setup.py
	@echo "[+] Formatting complete"

clean:
	@echo "[*] Cleaning up..."
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*~" -delete
	rm -rf build/ dist/ *.egg-info/
	@echo "[+] Cleanup complete"

docs:
	@echo "[*] Building documentation..."
	@echo "[+] Available docs: README.md, USAGE.md, ARCHITECTURE.md, CONTRIBUTING.md"

dev-setup:
	@echo "[*] Setting up development environment..."
	pip install -r requirements.txt
	pip install pytest flake8 black mypy
	@echo "[+] Development environment ready"

# Example workflows
workshop-%:
	@echo "[*] Running workshop: $*"
	python lucille.py scan -t $*.com --full -o results/$*_report.json

quick-recon-%:
	@echo "[*] Quick reconnaissance on $*"
	python lucille.py scan -t $* --quick

batch-scan-%:
	@echo "[*] Batch scanning targets from $*"
	python lucille.py scan -f $* --parallel 3

all: install setup
	@echo "[+] Lucille is ready to use!"
	@echo ""
	@echo "Next steps:"
	@echo "  - Run: make console"
	@echo "  - Or:  python lucille.py scan -t example.com --quick"
	@echo "  - Learn more: cat USAGE.md"
