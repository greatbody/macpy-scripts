"""Sunsoft utilities for tracking first-run statistics."""
import os
import json
import sys
from datetime import datetime
from termcolor import colored

# Centralized tracking configuration
TRACKING_BASE_URL = "https://package-download-logger.sunruicode.workers.dev/pip"
STATS_FILE = os.path.expanduser("~/.sunsoft.json")

def load_stats():
    """Load stats from the stats file."""
    stats = {}
    if os.path.exists(STATS_FILE):
        try:
            with open(STATS_FILE, 'r') as f:
                stats = json.load(f)
        except Exception:
            stats = {}
    return stats

def save_stats(stats):
    """Save stats to the stats file."""
    try:
        with open(STATS_FILE, 'w') as f:
            json.dump(stats, f, indent=2)
    except Exception as e:
        print(colored("Note: Could not save installation statistics. This does not affect functionality.", "yellow"))

def register_script(script_name, version):
    """Register a new script in the stats file."""
    stats = load_stats()

    if script_name not in stats:
        print(colored(f"Notice: First time seeing script '{script_name}'", "blue"))
        stats[script_name] = {
            'first_run_complete': False,
            'version': version,
            'registration_date': datetime.now().isoformat()
        }
        save_stats(stats)
    return stats[script_name]

def send_first_run_stats(script_name, version):
    """Send anonymous statistics on first run of a script.

    Args:
        script_name (str): Name of the script being tracked
        version (str): Version of the script
    """
    # First ensure script is registered
    script_stats = register_script(script_name, version)

    if not script_stats.get('first_run_complete'):
        if not "--no-track-install" in sys.argv:
            try:
                import requests
                print(colored("Notice: Submitting anonymous installation metrics. This occurs once and collects no personal data.", "yellow"))
                url = f"{TRACKING_BASE_URL}/{script_name}/{version}"
                print(f"Sending GET request to {url}")
                requests.get(url, timeout=2)
                print(colored("✓ Thank you for helping us improve!", "green"))
            except Exception as e:
                print(colored("Note: Could not send installation count. This does not affect functionality.", "yellow"))

        # Update script stats
        stats = load_stats()
        stats[script_name].update({
            'first_run_complete': True,
            'version': version,
            'first_run_date': datetime.now().isoformat()
        })
        save_stats(stats)

    return script_stats