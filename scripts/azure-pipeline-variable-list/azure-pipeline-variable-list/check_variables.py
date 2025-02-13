import os
import re
import yaml
from pathlib import Path

def extract_variables(content):
    """Extract all variables in $(VARIABLE) format from a string.
    Only matches valid variable names, not commands or expressions.
    Valid variable names consist of letters, numbers, underscores, and dots."""
    pattern = r'\$\(([a-zA-Z][a-zA-Z0-9_\.]*)\)'
    matches = re.findall(pattern, content)
    return set(matches)

def extract_variable_names(content):
    """Extract variable names from lines starting with '## - ' prefix."""
    variable_names = set()
    for line in content.splitlines():
        if line.startswith('## - '):
            variable_name = line[5:].strip()
            variable_names.add(variable_name)
    return variable_names

def process_yaml_file(file_path):
    """Process a YAML file and extract variables."""
    try:
        # First read the file as text to find variables in comments or invalid YAML sections
        with open(file_path, 'r', encoding='utf-8') as f:
            raw_content = f.read()
            variables = extract_variables(raw_content)
            variables_in_group = extract_variable_names(raw_content)

        # Then parse as YAML to get the structure (optional, for future use)
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                yaml_content = yaml.safe_load(f)
            except yaml.YAMLError:
                print(f"Warning: Could not parse {file_path} as valid YAML")
                yaml_content = None

        return variables, variables_in_group
    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")
        return set(), set()

def find_yaml_files(directory):
    """Find all YAML files in the given directory and subdirectories."""
    yaml_files = []
    for ext in ['.yml', '.yaml']:
        yaml_files.extend(Path(directory).rglob(f'*{ext}'))
    return yaml_files

def main():
    # Use the current working directory
    pipelines_dir = os.getcwd()

    # Find all YAML files
    yaml_files = find_yaml_files(pipelines_dir)

    # Process each file
    all_variables = {}
    all_variables_in_group = {}

    for file_path in yaml_files:
        variables, variables_in_group = process_yaml_file(file_path)
        if variables:
            all_variables[str(file_path)] = variables
            all_variables_in_group[str(file_path)] = variables_in_group

    # Print results
    print("\nVariables found in pipeline files123:")
    print("==================================")

    for file_path, variables in all_variables.items():
        print(f"\n{os.path.relpath(file_path, pipelines_dir)}:")
        for var in sorted(variables):
            print(f"  - {var}" + ("\033[92m (by variable group)\033[0m" if var in all_variables_in_group[file_path] else ""))

if __name__ == "__main__":
    main()
