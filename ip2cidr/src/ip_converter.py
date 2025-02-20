#!/usr/bin/env python3

import argparse
import sys
from version import __version__
from sunsoft import send_first_run_stats

def ip_to_cidr(ip_list):
    """Convert a comma-separated list of IP addresses to their /24 CIDR networks."""
    # Split the comma-separated string into individual IPs
    ip_addresses = [ip.strip() for ip in ip_list.split(',')]

    # Set to store unique /24 networks
    cidr_networks = set()

    for ip in ip_addresses:
        try:
            # Split IP into octets
            octets = ip.split('.')
            if len(octets) != 4:
                print(f"Invalid IP format: {ip}", file=sys.stderr)
                continue

            # Convert to /24 by keeping first 3 octets and setting last to 0
            network = f"{octets[0]}.{octets[1]}.{octets[2]}.0/24"
            cidr_networks.add(network)

        except Exception as e:
            print(f"Error processing IP {ip}: {str(e)}", file=sys.stderr)
            continue

    # Convert set to sorted list for consistent output
    return sorted(list(cidr_networks))

def main():
    # Send first run statistics
    send_first_run_stats(
        script_name='ip2cidr',
        version=__version__
    )

    parser = argparse.ArgumentParser(
        description='Convert IP addresses to /24 CIDR notation'
    )
    parser.add_argument(
        '-i', '--ips',
        required=True,
        help='Comma-separated list of IP addresses'
    )
    parser.add_argument(
        '-s', '--separator',
        default=',',
        help='Output separator (default: comma)'
    )

    args = parser.parse_args()

    try:
        result = ip_to_cidr(args.ips)
        print(args.separator.join(result))
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()