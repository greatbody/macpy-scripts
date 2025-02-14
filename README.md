# MacPy Scripts

This repository contains a collection of independent Python scripts for various automation tasks. Each script is self-contained in its own directory with its own dependencies and setup.

This repository is completed with assistance from [Cursor](https://cursor.sh/).

这个项目是使用 [Cursor](https://cursor.sh/) 完成的。

| Script    | Status                                                                                                                                                                              |
| -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| azpipvar | [![azpipvar](https://github.com/greatbody/macpy-scripts/actions/workflows/azpipvar-test.yml/badge.svg)](https://github.com/greatbody/macpy-scripts/actions/workflows/azpipvar-test.yml) |



## Repository Structure

```
macpy-scripts/
├── azpipvar/               # Azure Pipeline Variable List tool
│   ├── README.md          # Script-specific documentation
│   ├── requirements.txt   # Script-specific dependencies
│   ├── setup.py          # Script-specific setup
│   └── src/              # Script source code
└── template/             # Template directory for new scripts
    ├── README.md
    ├── requirements.txt
    ├── setup.py
    └── src/
```

## Available Scripts

### [Azure Pipeline Variable List (azpipvar)](azpipvar/README.md)
A tool to analyze and list variables used in Azure Pipeline YAML files. It helps you track and manage variables across your Azure Pipeline configurations.

## Adding a New Script

1. Create a new directory in the root with your script name
2. Copy the contents of the `template/` directory to your new script directory
3. Update the README.md with your script's documentation
4. Update requirements.txt with your script's specific dependencies
5. Update setup.py with your script's metadata
6. Add your script's code in the src/ directory

## Development

Each script is independent and can be developed separately. To work on a script:

1. Create a virtual environment: `python -m venv .venv`
2. Activate the virtual environment:
   - Windows: `.venv\Scripts\activate`
   - Unix/MacOS: `source .venv/bin/activate`
3. Navigate to your script directory: `cd your-script-directory`
4. Install script-specific dependencies: `pip install -r requirements.txt`
5. Install the script in development mode: `pip install -e .`

## Installation Methods

You can install any script as a global command using one of these methods:

### Method 1: pipx Installation (Recommended)

[pipx](https://pypa.github.io/pipx/) is the best option for installing Python CLI applications as it creates isolated environments automatically:

```bash
# Install pipx if you haven't already
python -m pip install --user pipx
python -m pipx ensurepath

# Install the script
pipx install ./script-directory
```

### Method 2: User Installation

This method installs the script in your user's Python environment:

```bash
# Navigate to the script directory
cd script-directory

# Install script and dependencies for your user
pip install --user -r requirements.txt
pip install --user .
```

The script's commands will be available in:
- Unix/MacOS: `~/.local/bin`
- Windows: `%APPDATA%\Python\Scripts`

Make sure these directories are in your PATH.

### Method 3: System-wide Installation

This method requires administrator/root privileges:

```bash
# Navigate to the script directory
cd script-directory

# Install script and dependencies system-wide
sudo pip install -r requirements.txt
sudo pip install .
```

### Note About Virtual Environments

- For development: Use virtual environments (as described in the Development section)
- For global installation: Make sure to deactivate any virtual environment first
- For the most reliable global installation: Use pipx (Method 1)

## Contributing

1. Create a new branch for your script or changes
2. Follow the directory structure and documentation guidelines
3. Test your script thoroughly
4. Submit a pull request