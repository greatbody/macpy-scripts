# ip2cidr

A Python tool to convert IP addresses to /24 CIDR notation.

## Installation

```bash
pip install ip2cidr
```

## Usage

The tool can be used from the command line:

```bash
# Convert a single IP
ip2cidr -i "10.200.2.132"

# Convert multiple IPs (comma-separated)
ip2cidr -i "10.200.2.132,192.168.1.100,172.16.5.200"

# Use a different separator for output (default is comma)
ip2cidr -i "10.200.2.132,192.168.1.100" -s " "
```

### Arguments

- `-i, --ips`: Required. Comma-separated list of IP addresses to convert
- `-s, --separator`: Optional. Output separator (default: comma)

### Example Output

```bash
$ ip2cidr -i "10.200.2.132,192.168.1.100,172.16.5.200"
10.200.2.0/24,172.16.5.0/24,192.168.1.0/24

$ ip2cidr -i "10.200.2.132,192.168.1.100" -s " "
10.200.2.0/24 192.168.1.0/24
```

## Python Usage

You can also use the tool in your Python code:

```python
from ip_converter import ip_to_cidr

# Convert IPs to CIDR
ips = "10.200.2.132,192.168.1.100"
cidrs = ip_to_cidr(ips)
print(cidrs)  # ['10.200.2.0/24', '192.168.1.0/24']
```

## Development

### Running Tests

To run the tests, first install the development dependencies:

```bash
pip install -e ".[test]"
```

Then run the tests with pytest:

```bash
pytest
```

This will run all tests and generate a coverage report. The tests cover various scenarios including:
- Single IP conversion
- Multiple IP conversion
- Duplicate network handling
- Invalid IP handling
- Empty input
- Whitespace handling
- Partial IP addresses
- Special IP addresses (localhost, etc.)

## Features

- Converts IP addresses to their corresponding /24 CIDR networks
- Handles multiple IP addresses
- Removes duplicates and sorts the output
- Customizable output separator
- Error handling for invalid IP addresses
- Comprehensive test suite with 100% coverage

## Requirements

- Python 3.8 or higher
- argparse>=1.4.0

## License

MIT License 