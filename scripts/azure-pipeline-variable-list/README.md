# MacPy Scripts

This repository contains a collection of independent Python scripts for various automation tasks. Each script is self-contained in its own directory with its own dependencies and setup.

## Repository Structure

```
macpy-scripts/
├── requirements.txt          # Common dependencies shared across scripts
├── scripts/                 # Directory containing all script packages
│   ├── script1/            # Each script has its own directory
│   │   ├── README.md       # Script-specific documentation
│   │   ├── requirements.txt # Script-specific dependencies
│   │   ├── setup.py        # Script-specific setup
│   │   └── src/            # Script source code
│   └── script2/
│       └── ...
└── template/               # Template directory for new scripts
    ├── README.md
    ├── requirements.txt
    ├── setup.py
    └── src/
```

## Adding a New Script

1. Create a new directory under `scripts/` with your script name
2. Copy the contents of the `template/` directory to your new script directory
3. Update the README.md with your script's documentation
4. Update requirements.txt with your script's specific dependencies
5. Update setup.py with your script's metadata
6. Add your script's code in the src/ directory

## Common Dependencies

Common dependencies used across multiple scripts are listed in the root `requirements.txt`. Each script can also have its own `requirements.txt` for script-specific dependencies.

## Development

Each script is independent and can be developed separately. To work on a script:

1. Create a virtual environment: `python -m venv .venv`
2. Activate the virtual environment:
   - Windows: `.venv\Scripts\activate`
   - Unix/MacOS: `source .venv/bin/activate`
3. Install common dependencies: `pip install -r requirements.txt`
4. Navigate to your script directory: `cd scripts/your-script`
5. Install script-specific dependencies: `pip install -r requirements.txt`
6. Install the script in development mode: `pip install -e .`

## Global Installation

You can install any script as a global command in your terminal using one of these methods:

### Method 1: User Installation (Recommended)

This method installs the script in your user's Python environment. **Important**: Make sure you are NOT in a virtual environment when using this method:

```bash
# First, deactivate any virtual environment if active
deactivate

# Navigate to the script directory
cd scripts/your-script

# Install script and dependencies for your user
pip install --user -r requirements.txt
pip install --user .
```

The script's commands will be available in:
- Unix/MacOS: `~/.local/bin`
- Windows: `%APPDATA%\Python\Scripts`

Make sure these directories are in your PATH.

### Method 2: System-wide Installation

This method requires administrator/root privileges and installs the script system-wide. **Important**: Make sure you are NOT in a virtual environment:

```bash
# First, deactivate any virtual environment if active
deactivate

# Navigate to the script directory
cd scripts/your-script

# Install script and dependencies system-wide
sudo pip install -r requirements.txt
sudo pip install .
```

### Method 3: pipx Installation (Recommended for CLI Tools)

[pipx](https://pypa.github.io/pipx/) is the best option for installing Python CLI applications as it creates isolated environments automatically:

```bash
# Install pipx if you haven't already
python -m pip install --user pipx
python -m pipx ensurepath

# Install the script (can be done from any directory)
pipx install ./scripts/your-script
```

After installation, you can run your script's commands from anywhere in the terminal. The actual command name will be defined in the script's `setup.py` under `entry_points`.

### Note About Virtual Environments

- For development: Use virtual environments (as described in the Development section)
- For global installation: Make sure to deactivate any virtual environment first
- For the most reliable global installation: Use pipx (Method 3)

## Contributing

1. Create a new branch for your script or changes
2. Follow the directory structure and documentation guidelines
3. Test your script thoroughly
4. Submit a pull request 