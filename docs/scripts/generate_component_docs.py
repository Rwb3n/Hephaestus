#!/usr/bin/env python
"""
Component Documentation Generator for Hephaestus

This script analyzes Python source files to generate component documentation
using the standardized template format.
"""

import os
import re
import ast
import inspect
import importlib.util
import datetime
from pathlib import Path

# Base paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
DOCS_DIR = PROJECT_ROOT / "docs"
SCRIPTS_DIR = DOCS_DIR / "scripts"
TEMPLATES_DIR = DOCS_DIR / "templates"
COMPONENTS_DIR = DOCS_DIR / "components"

# Template file
COMPONENT_TEMPLATE = TEMPLATES_DIR / "component_template.md"

# Regex pattern for extracting class docstrings
CLASS_DOCSTRING_PATTERN = re.compile(r'class\s+(\w+).*?:(?:\s*"""(.*?)""")?', re.DOTALL)
METHOD_DOCSTRING_PATTERN = re.compile(r'def\s+(\w+).*?:(?:\s*"""(.*?)""")?', re.DOTALL)


def extract_class_info(file_path):
    """
    Extract class information from a Python file.
    
    Args:
        file_path: Path to the Python file
        
    Returns:
        A list of dictionaries with class information
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            source = f.read()
        
        # Parse the source code
        tree = ast.parse(source)
        
        classes = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                class_info = {
                    'name': node.name,
                    'docstring': ast.get_docstring(node) or '',
                    'methods': [],
                    'base_classes': [base.id if isinstance(base, ast.Name) else None for base in node.bases]
                }
                
                # Extract methods
                for method in [n for n in node.body if isinstance(n, ast.FunctionDef)]:
                    method_info = {
                        'name': method.name,
                        'docstring': ast.get_docstring(method) or '',
                        'args': [arg.arg for arg in method.args.args if arg.arg != 'self'],
                        'is_private': method.name.startswith('_')
                    }
                    class_info['methods'].append(method_info)
                
                classes.append(class_info)
        
        return classes
    
    except Exception as e:
        print(f"Error extracting class info from {file_path}: {str(e)}")
        return []


def generate_component_doc(component_path, output_dir, component_type=None):
    """
    Generate documentation for a component.
    
    Args:
        component_path: Path to the component Python file
        output_dir: Directory to write the documentation
        component_type: Type of component (core, engine, scoring, etc.)
    """
    # Extract class information
    classes = extract_class_info(component_path)
    if not classes:
        print(f"No classes found in {component_path}")
        return False
    
    # Use the first class as the main component
    main_class = classes[0]
    
    # Determine component status
    status = "Stable"  # Default
    if "BestOfNBuilder" in main_class['name']:
        status = "Consolidated"
    elif "FlowBuilder" in main_class['name']:
        status = "Enhanced"
    
    # Load template
    try:
        with open(COMPONENT_TEMPLATE, 'r', encoding='utf-8') as f:
            template = f.read()
    except FileNotFoundError:
        print(f"Template file not found: {COMPONENT_TEMPLATE}")
        return False
    
    # Get relative path from project root
    rel_path = component_path.relative_to(PROJECT_ROOT)
    
    # Prepare class interface
    interface_code = f"```python\nclass {main_class['name']}"
    if main_class['base_classes']:
        base_classes = [base for base in main_class['base_classes'] if base]
        if base_classes:
            interface_code += f"({', '.join(base_classes)})"
    interface_code += ":\n"
    
    # Add constructor and methods
    for method in main_class['methods']:
        if method['is_private']:
            continue
        args_str = ', '.join(['self'] + method['args'])
        interface_code += f"    def {method['name']}({args_str}):\n"
        if method['docstring']:
            # Extract first line of docstring
            doc_summary = method['docstring'].strip().split('\n')[0]
            interface_code += f"        \"{doc_summary}\"\n"
        else:
            interface_code += "        pass\n"
    
    interface_code += "```"
    
    # Prepare usage examples
    basic_example = f"""```python
from hephaestus import {main_class['name']}

component = {main_class['name']}()
# Basic usage example
result = component.method1(input_data)
```"""
    
    advanced_example = f"""```python
from hephaestus import {main_class['name']}
from hephaestus import AnotherComponent

# Advanced usage
component = {main_class['name']}(config={"param": "value"})
other = AnotherComponent()

# Integration example
result = component.process(other.prepare(data))
```"""
    
    # Create documentation content
    today = datetime.date.today().strftime("%Y-%m-%d")
    doc_content = template.replace("Component Name", main_class['name'])
    doc_content = doc_content.replace("**Version**: 0.1.1", "**Version**: 0.1.1")
    doc_content = doc_content.replace("**Status**: Stable | Enhanced | Consolidated | In Progress | Planned", f"**Status**: {status}")
    doc_content = doc_content.replace("**Last Updated**: YYYY-MM-DD", f"**Last Updated**: {today}")
    doc_content = doc_content.replace("`path/to/component.py`", f"`{rel_path}`")
    
    # Replace overview and purpose with docstring if available
    if main_class['docstring']:
        docstring_parts = main_class['docstring'].strip().split('\n\n', 1)
        overview = docstring_parts[0]
        purpose = docstring_parts[1] if len(docstring_parts) > 1 else ""
        
        doc_content = re.sub(r'## Overview\n\nBrief description.*?\n\n## Purpose\n\nClear statement.*?\n\n',
                            f"## Overview\n\n{overview}\n\n## Purpose\n\n{purpose}\n\n", 
                            doc_content, 
                            flags=re.DOTALL)
    
    # Replace interface and usage examples
    doc_content = doc_content.replace("```python\n# Core class/function signature\nclass ComponentName:\n    def __init__(self, param1, param2=None):\n        \"\"\"Constructor documentation\"\"\"\n        pass\n        \n    def method1(self, input):\n        \"\"\"Method documentation\"\"\"\n        return output\n```", interface_code)
    doc_content = doc_content.replace("```python\n# Simple example of how to use the component\nfrom module import ComponentName\n\ncomponent = ComponentName(param1=\"value\")\nresult = component.method1(\"input\")\nprint(result)\n```", basic_example)
    doc_content = doc_content.replace("```python\n# More complex example showing integration with other components\nfrom module import ComponentName\nfrom other_module import OtherComponent\n\ncomponent = ComponentName(param1=\"value\")\nother = OtherComponent()\n\n# Show how they work together\ncomponent.method1(other.process(\"input\"))\n```", advanced_example)
    
    # Write output file
    output_filename = f"{main_class['name'].lower()}.md"
    output_path = output_dir / output_filename
    
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(doc_content)
        print(f"Generated documentation for {main_class['name']} at {output_path}")
        return True
    except Exception as e:
        print(f"Error writing documentation file: {str(e)}")
        return False


def main():
    """Main function to generate component documentation."""
    print("Starting component documentation generation...")
    
    # Map of component types to directories
    component_dirs = {
        'core': COMPONENTS_DIR / "core",
        'engine': COMPONENTS_DIR / "engine",
        'scoring': COMPONENTS_DIR / "scoring"
    }
    
    # Source code locations to scan
    source_dirs = {
        'core': PROJECT_ROOT / "core",
        'engine': PROJECT_ROOT / "engine",
        'scoring': PROJECT_ROOT / "scoring"
    }
    
    # Ensure output directories exist
    for dir_path in component_dirs.values():
        dir_path.mkdir(parents=True, exist_ok=True)
    
    # Track success and failure
    success_count = 0
    failure_count = 0
    
    # Process components
    for component_type, source_dir in source_dirs.items():
        if not source_dir.exists():
            print(f"Source directory not found: {source_dir}")
            continue
            
        output_dir = component_dirs[component_type]
        
        # Find Python files
        python_files = list(source_dir.glob("**/*.py"))
        for py_file in python_files:
            # Skip __init__.py and similar files
            if py_file.name.startswith("__") or py_file.name.endswith("_test.py"):
                continue
                
            print(f"Processing {py_file}...")
            success = generate_component_doc(py_file, output_dir, component_type)
            if success:
                success_count += 1
            else:
                failure_count += 1
    
    print(f"\nComponent documentation generation completed!")
    print(f"Successfully generated: {success_count} files")
    print(f"Failed to generate: {failure_count} files")
    print(f"\nNext steps:")
    print(f"1. Review generated documentation files")
    print(f"2. Update any missing information")
    print(f"3. Add the component pages to the mkdocs.yml navigation")


if __name__ == "__main__":
    main() 