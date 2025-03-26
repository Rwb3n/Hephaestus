# Documentation Scripts

This directory contains scripts for automating the documentation process for the Hephaestus project.

## Available Scripts

- **setup_docs.py**: Sets up the documentation structure and initial configuration
- **migrate_docs.py**: Migrates existing documentation files to the new structure
- **generate_component_docs.py**: Generates component documentation from source code
- **build_docs.bat**: Windows batch script for running documentation tools
- **build_docs.sh**: Unix shell script for running documentation tools

## Running the Scripts

### Using the Helper Scripts

The easiest way to run the documentation tools is to use the helper scripts:

#### Windows
```
cd D:\PROJECTS\hephaestus
docs\scripts\build_docs.bat
```

#### Unix-based Systems (Linux, macOS)
```bash
cd /path/to/hephaestus
chmod +x docs/scripts/build_docs.sh
./docs/scripts/build_docs.sh
```

These scripts provide a menu-based interface for running the various documentation tools.

### Running Individual Scripts

You can also run the Python scripts directly:

```bash
# Set up documentation structure
python docs/scripts/setup_docs.py

# Migrate existing documentation
python docs/scripts/migrate_docs.py

# Generate component documentation
python docs/scripts/generate_component_docs.py
```

## Documentation Pipeline

The complete documentation pipeline consists of the following steps:

1. **Setup**: Creates the necessary directory structure and configuration files
2. **Migration**: Moves existing documentation files to the new structure
3. **Generation**: Creates component documentation from source code
4. **Build**: Builds the documentation site using MkDocs

This pipeline is automated by the helper scripts (option 6).

## MkDocs Commands

After setting up the documentation, you can use the following MkDocs commands:

```bash
# Start a development server for preview
mkdocs serve

# Build the documentation site
mkdocs build

# Get help
mkdocs --help
```

## Requirements

The documentation system requires the following dependencies:

- Python 3.8+
- MkDocs and plugins (installed by setup_docs.py)

See the `docs/research/documentation_requirements.txt` file for a complete list of dependencies.

## Troubleshooting

If you encounter issues running the scripts:

1. Ensure you have Python 3.8+ installed and available in your PATH
2. Verify that you've installed the required dependencies
3. Check that you're running the scripts from the project root directory
4. Look for error messages in the script output 