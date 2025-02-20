# sunsoft-utils

Shared utilities for Sunsoft packages.

## Installation

```bash
pip install sunsoft-utils
```

## Usage

### Download Tracking

```python
from sunsoft import send_first_run_stats

def main():
    # Send first run statistics
    send_first_run_stats(
        script_name='your-package-name',
        version='1.0.0'
    )

    # Your code here...
```

### Features

- Anonymous download tracking
- First-run detection
- Version tracking
- Support for `--no-track-install` flag
- Colored console output

### Configuration

The tracking data is stored in `~/.sunsoft.json` and includes:
- First run date
- Registration date
- Version information
- Installation status

## Requirements

- Python 3.8 or higher
- requests>=2.32.3
- termcolor>=2.3.0

## License

MIT License