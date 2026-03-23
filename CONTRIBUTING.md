# Contributing to Lucille

Thank you for considering contributing to Lucille! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

- Be respectful and inclusive
- Focus on the code, not the person
- Help others learn and grow
- Report issues constructively

## Ways to Contribute

- **Bug Reports**: Report issues you find
- **Feature Requests**: Suggest new features or modules
- **Code**: Submit pull requests with improvements
- **Documentation**: Improve guides and comments
- **Testing**: Test on different systems
- **Modules**: Create new scanner modules

## Getting Started

### 1. Fork & Clone

```bash
git clone https://github.com/YOUR_USERNAME/Lucille.git
cd Lucille
```

### 2. Set Up Development Environment

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate  # Windows

pip install -r requirements.txt
pip install -r requirements-dev.txt  # Development dependencies
```

### 3. Create a Branch

```bash
git checkout -b feature/my-feature
# or
git checkout -b fix/issue-name
```

## Development Guidelines

### Code Style

- Follow PEP 8
- Use meaningful variable names
- Add docstrings to functions
- Use type hints where possible

```python
def execute(self, target: str, timeout: int = 30) -> Dict[str, Any]:
    """
    Execute scan on target.
    
    Args:
        target: Target host or IP
        timeout: Timeout in seconds
        
    Returns:
        Dictionary with scan results
    """
    pass
```

### Commit Messages

- Use clear, descriptive commit messages
- Start with verb: "Add", "Fix", "Update", "Improve"
- Keep messages under 72 characters
- Reference issues when applicable

```
Good:
- "Add port_scan module"
- "Fix DNS enumeration timeout"
- "Update documentation (closes #42)"

Bad:
- "stuff"
- "dsljkfdl"
- "fixed it"
```

### Testing

Write tests for new features:

```python
def test_port_scan_module():
    """Test port scanning functionality"""
    module = PortScanModule()
    result = module.execute("localhost", timeout=10)
    assert result['status'] == 'success'
    assert 'open_ports' in result
```

Run tests:

```bash
python -m pytest tests/
```

## Creating New Modules

### Module Template

Create new file in `src/modules/`:

```python
"""
My Module Description
"""

from src.core.module_manager import LucilleModule
from typing import Dict, Any


class MyModule(LucilleModule):
    """My scanner module"""
    
    name = "my_module"
    description = "Brief description of what this module does"
    category = "reconnaissance"  # or vulnerability_scan, osint, etc.
    enabled = True
    
    def execute(self, target: str, timeout: int = 30) -> Dict[str, Any]:
        """
        Execute module scan.
        
        Args:
            target: Target host/IP/domain
            timeout: Timeout in seconds
            
        Returns:
            Dictionary with scan results
        """
        results = {
            'target': target,
            'status': 'pending',
            'data': {}
        }
        
        try:
            # Your scanning logic here
            
            results['status'] = 'success'
            results['data'] = {...}
        except Exception as e:
            results['status'] = 'error'
            results['error'] = str(e)
        
        return results
```

### Register Module

In `src/core/module_manager.py`:

```python
def load_modules(self):
    """Dynamically load available modules"""
    self.modules = {
        'my_module': MyModule(),
        # ... other modules
    }
```

## Pull Request Process

1. **Ensure tests pass**:
   ```bash
   python -m pytest tests/
   ```

2. **Check code style**:
   ```bash
   flake8 src/
   black src/
   ```

3. **Update documentation** if adding features

4. **Create descriptive PR** with:
   - Clear title
   - Description of changes
   - Related issues
   - Screenshots (if UI changes)

5. **Wait for review** and address feedback

## Documentation

### Updating Documentation

- Edit relevant `.md` files
- Keep documentation current
- Use clear language
- Add examples where helpful

### API Documentation

Use docstrings for functions:

```python
def scan(self, target: str, modules: str = 'all') -> Dict:
    """
    Execute scan on target.
    
    Args:
        target: Target host or IP
        modules: Modules to run ('all', 'quick', or comma-separated)
        
    Returns:
        Dictionary containing scan results with keys:
        - target: Target scanned
        - timestamp: When scan was run
        - modules: Results from each module
        
    Raises:
        ValueError: If target is invalid
        TimeoutError: If scan exceeds timeout
    """
```

## Bug Reports

When reporting bugs:

1. **Check existing issues** first
2. **Be specific** about the problem
3. **Provide reproduction steps**
4. **Include system information**:
   - OS and version
   - Python version
   - Lucille version

Template:

```markdown
## Bug Description
Brief description of the bug

## Reproduction Steps
1. Run command: ...
2. ...
3. Error occurs

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## System Information
- OS: Linux/MacOS/Windows
- Python: 3.X
- Lucille: version

## Additional Context
Any other relevant information
```

## Feature Requests

For feature requests:

1. **Describe the feature** clearly
2. **Explain the use case**
3. **Show how it would work**
4. **Consider edge cases**

Template:

```markdown
## Feature Request
Brief title

## Description
Detailed description of feature

## Use Case
Why is this feature needed?

## Example Usage
How would user interact with it?

## Additional Context
Related issues, discussions, etc.
```

## Coding Tasks

- Good first issues are labeled `good-first-issue`
- Help wanted issues need community contributions
- Check Issues tab for current work

## Questions?

- Open an issue with the `question` label
- Check existing documentation
- Contact maintainers

## License

By contributing, you agree that your contributions will be licensed under GPL-3.0.

## Recognition

Contributors will be recognized in:
- README.md
- CONTRIBUTORS.md
- Release notes

Thank you for contributing to Lucille! 🌟
