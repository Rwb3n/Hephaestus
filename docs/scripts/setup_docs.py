#!/usr/bin/env python
"""
Documentation Setup Script for Hephaestus

This script automates the setup process for the MkDocs documentation environment
by creating the necessary directory structure, copying template files, and
setting up the initial configuration.
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

# Base paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
DOCS_DIR = PROJECT_ROOT / "docs"
SCRIPTS_DIR = DOCS_DIR / "scripts"
TEMPLATES_DIR = DOCS_DIR / "templates"
RESEARCH_DIR = DOCS_DIR / "research"

# Documentation structure paths
ASSETS_DIR = DOCS_DIR / "assets"
IMAGES_DIR = ASSETS_DIR / "images"
CSS_DIR = ASSETS_DIR / "css"
GUIDES_DIR = DOCS_DIR / "guides"
COMPONENTS_DIR = DOCS_DIR / "components"
CORE_COMPONENTS_DIR = COMPONENTS_DIR / "core"
ENGINE_COMPONENTS_DIR = COMPONENTS_DIR / "engine"
SCORING_COMPONENTS_DIR = COMPONENTS_DIR / "scoring"
PROPOSALS_DIR = DOCS_DIR / "proposals"
CONCEPTS_DIR = DOCS_DIR / "concepts"
REFERENCE_DIR = DOCS_DIR / "reference"
STATUS_DIR = DOCS_DIR / "status"
PROGRESS_DIR = DOCS_DIR / "progress"

# Files
CONFIG_EXAMPLE = RESEARCH_DIR / "mkdocs_config_example.yml"
REQUIREMENTS = RESEARCH_DIR / "documentation_requirements.txt"
CUSTOM_CSS = CSS_DIR / "custom.css"
INDEX_MD = DOCS_DIR / "index.md"


def create_directories():
    """Create the necessary directory structure for documentation."""
    print("Creating directory structure...")
    
    directories = [
        ASSETS_DIR, IMAGES_DIR, CSS_DIR, 
        GUIDES_DIR, COMPONENTS_DIR, CORE_COMPONENTS_DIR, 
        ENGINE_COMPONENTS_DIR, SCORING_COMPONENTS_DIR,
        PROPOSALS_DIR, CONCEPTS_DIR, REFERENCE_DIR,
        STATUS_DIR, PROGRESS_DIR
    ]
    
    for directory in directories:
        if not directory.exists():
            directory.mkdir(parents=True)
            print(f"Created directory: {directory}")
        else:
            print(f"Directory already exists: {directory}")


def copy_config_file():
    """Copy the MkDocs configuration file to the project root."""
    print("Setting up MkDocs configuration...")
    
    if CONFIG_EXAMPLE.exists():
        mkdocs_config = PROJECT_ROOT / "mkdocs.yml"
        shutil.copy(CONFIG_EXAMPLE, mkdocs_config)
        print(f"Copied configuration file to {mkdocs_config}")
    else:
        print(f"Warning: Configuration example not found at {CONFIG_EXAMPLE}")


def create_custom_css():
    """Create a custom CSS file for styling the documentation."""
    print("Creating custom CSS file...")
    
    css_content = """
:root {
  --md-primary-fg-color: #3949ab;
  --md-primary-fg-color--light: #757de8;
  --md-primary-fg-color--dark: #002984;
  --md-accent-fg-color: #757de8;
}

.md-header__title {
  font-weight: bold;
}

.md-content {
  max-width: 1200px;
  margin: 0 auto;
}

code {
  font-size: 0.9em;
}

.md-typeset table:not([class]) {
  font-size: 0.7rem;
}
"""
    
    with open(CUSTOM_CSS, "w") as f:
        f.write(css_content)
    print(f"Created custom CSS file at {CUSTOM_CSS}")


def create_requirements_file():
    """Create a requirements file for documentation dependencies in the project root."""
    print("Setting up requirements file...")
    
    if REQUIREMENTS.exists():
        docs_requirements = PROJECT_ROOT / "docs-requirements.txt"
        shutil.copy(REQUIREMENTS, docs_requirements)
        print(f"Copied requirements file to {docs_requirements}")
    else:
        print(f"Warning: Requirements file not found at {REQUIREMENTS}")


def create_index_page():
    """Create an initial index.md file if it doesn't exist."""
    print("Setting up index page...")
    
    if not INDEX_MD.exists():
        index_content = """# Hephaestus Documentation

Welcome to the Hephaestus documentation. Hephaestus is a self-improving code generation system designed to propose, build, test, score, and improve its own components through an evolutionary process.

## Getting Started

- [Installation Guide](guides/installation.md)
- [Quick Start Guide](guides/getting_started.md)
- [Architecture Overview](concepts/architecture.md)

## Key Components

- [Core Components](components/core/index.md)
- [Engine Components](components/engine/index.md)
- [Scoring Components](components/scoring/index.md)

## Project Information

- [Project Status](status/project_status.md)
- [Roadmap](status/roadmap.md)
- [Changelog](status/changelog.md)
"""
        with open(INDEX_MD, "w") as f:
            f.write(index_content)
        print(f"Created index page at {INDEX_MD}")
    else:
        print(f"Index page already exists at {INDEX_MD}")


def install_dependencies():
    """Install MkDocs and required plugins."""
    try:
        print("Installing documentation dependencies...")
        docs_requirements = PROJECT_ROOT / "docs-requirements.txt"
        
        if not docs_requirements.exists():
            print(f"Error: Requirements file not found at {docs_requirements}")
            return False
        
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", str(docs_requirements)],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("Successfully installed documentation dependencies")
            return True
        else:
            print(f"Error installing dependencies: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"Exception during dependency installation: {e}")
        return False


def test_mkdocs_build():
    """Test building the documentation with MkDocs."""
    try:
        print("Testing MkDocs build...")
        
        result = subprocess.run(
            ["mkdocs", "build", "--clean"],
            cwd=str(PROJECT_ROOT),
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("MkDocs build successful!")
            site_dir = PROJECT_ROOT / "site"
            print(f"Documentation site generated in {site_dir}")
            return True
        else:
            print(f"Error building documentation: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"Exception during MkDocs build: {e}")
        return False


def main():
    """Main function to run all setup tasks."""
    print("Starting documentation setup...")
    
    # Create necessary directories
    create_directories()
    
    # Copy configuration file
    copy_config_file()
    
    # Create custom CSS
    create_custom_css()
    
    # Create requirements file
    create_requirements_file()
    
    # Create index page
    create_index_page()
    
    # Ask to install dependencies
    install_deps = input("Do you want to install documentation dependencies? (y/n): ").lower()
    if install_deps == 'y':
        success = install_dependencies()
        if success:
            # Test MkDocs build
            build_docs = input("Do you want to test the documentation build? (y/n): ").lower()
            if build_docs == 'y':
                test_mkdocs_build()
    
    print("\nDocumentation setup completed!")
    print("Next steps:")
    print("1. Review the mkdocs.yml configuration file")
    print("2. Run 'mkdocs serve' to preview the documentation")
    print("3. Start migrating existing documentation")
    print("4. Update navigation structure in mkdocs.yml")


if __name__ == "__main__":
    main() 