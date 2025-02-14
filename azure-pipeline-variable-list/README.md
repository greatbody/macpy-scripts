# Azure Pipeline Variable List

A tool to analyze and list variables used in Azure Pipeline YAML files.

## Installation

From this directory:

```bash
pip install -r requirements.txt
pip install .
```

## Usage

Navigate to your Azure Pipelines directory and run:

```bash
check-pipeline-variables
```

This will scan all YAML files in the current directory and subdirectories, listing all variables used in the pipeline files.

## Features

- Detects variables in $(VARIABLE) format
- Identifies variables defined in variable groups
- Supports nested directory structures
- Handles both .yml and .yaml file extensions 