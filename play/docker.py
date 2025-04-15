#!/usr/bin/env python3

import subprocess
import json
import re
from tabulate import tabulate
from pathlib import Path

def get_overlay2_folder_sizes():
    """Get sizes of overlay2 folders as a dict: {folder_name: size_in_bytes}."""
    folder_sizes = {}
    overlay2_path = "/var/lib/docker/overlay2"

    for folder in Path(overlay2_path).iterdir():
        if folder.is_dir():
            try:
                cmd = f"du -sh {folder}"
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                size_str = result.stdout.split()[0]
                folder_sizes[folder.name] = parse_size_to_bytes(size_str)
            except (subprocess.SubprocessError, ValueError):
                continue

    return folder_sizes

def parse_size_to_bytes(size_str):
    """Convert human-readable size (e.g., '113.07M') to bytes."""
    size_str = size_str.strip()
    if not size_str:
        return 0

    match = re.match(r'^([\d.]+)([BKMGT])$', size_str, re.IGNORECASE)
    if not match:
        return 0

    num = float(match.group(1))
    unit = match.group(2).upper()
    units = {'B': 1, 'K': 1024, 'M': 1024**2, 'G': 1024**3, 'T': 1024**4}

    return int(num * units.get(unit, 1))

def get_docker_containers():
    """Get list of (container_id, container_name, inspect_data) tuples."""
    containers = []
    try:
        cmd = "docker ps -a -q"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        container_ids = result.stdout.strip().split()

        for cid in container_ids:
            cmd = f"docker inspect {cid}"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            try:
                inspect_data = json.loads(result.stdout)[0]
                container_name = inspect_data.get('Name', '').lstrip('/')
                containers.append((cid[:12], container_name, inspect_data))
            except json.JSONDecodeError:
                continue
    except subprocess.SubprocessError:
        pass

    return containers

def format_size(size_bytes):
    """Convert bytes to human-readable format (e.g., '1.23 GB')."""
    if size_bytes == 0:
        return "0 B"

    units = ['B', 'KB', 'MB', 'GB', 'TB']
    size = float(size_bytes)
    unit_index = 0

    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1

    return f"{size:.2f} {units[unit_index]}"

def main():
    # Get folder sizes
    folder_sizes = get_overlay2_folder_sizes()

    # Get containers
    containers = get_docker_containers()

    # Map folder sizes to containers
    container_sizes = {container[1]: 0 for container in containers}

    for _, container_name, inspect_data in containers:
        inspect_str = json.dumps(inspect_data)
        for folder_name, size_bytes in folder_sizes.items():
            if folder_name in inspect_str:
                container_sizes[container_name] += size_bytes

    # Build table data with size in bytes for sorting
    table_data = []
    used_folders = set()

    for container_name, size_bytes in container_sizes.items():
        if size_bytes > 0:
            for cid, cname, inspect_data in containers:
                if cname == container_name:
                    table_data.append({
                        'container_id': cid,
                        'container_name': container_name,
                        'size_bytes': size_bytes,
                        'size_str': format_size(size_bytes)
                    })
                    inspect_str = json.dumps(inspect_data)
                    for folder_name in folder_sizes:
                        if folder_name in inspect_str:
                            used_folders.add(folder_name)
                    break

    # Add unassociated folders
    unassociated_size = sum(size for folder, size in folder_sizes.items() if folder not in used_folders)
    if unassociated_size > 0:
        table_data.append({
            'container_id': 'N/A',
            'container_name': 'Unassociated',
            'size_bytes': unassociated_size,
            'size_str': format_size(unassociated_size)
        })

    # Sort by size_bytes (descending)
    table_data.sort(key=lambda x: x['size_bytes'], reverse=True)

    # Add accumulated size
    acc_size = 0
    for row in table_data:
        acc_size += row['size_bytes']
        row['acc_size'] = acc_size
        row['acc_size_str'] = format_size(acc_size)

    # Format table for output
    table_output = [
        [row['container_id'], row['container_name'], row['size_str'], row['acc_size_str']]
        for row in table_data
    ]

    # Print table
    headers = ['Container ID', 'Container Name', 'Size', 'Accumulated Size']
    print(tabulate(table_output, headers=headers, tablefmt='grid'))

    # Print list of unassociated folders
    unassociated_folders = [folder for folder in folder_sizes if folder not in used_folders]
    if unassociated_folders:
        print("\nUnassociated folders:")
        for folder in unassociated_folders:
            print(f" - {folder}")
    else:
        print("\nNo unassociated folders found.")

if __name__ == "__main__":
    main()
