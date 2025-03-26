---
title: Getting Started with Hephaestus
description: A step-by-step guide to installing, configuring, and running your first Hephaestus workflow
---

# Getting Started with Hephaestus

This guide will walk you through the process of setting up Hephaestus and running your first code generation and improvement workflow.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.9+**: Hephaestus requires Python 3.9 or newer
- **pip**: For package installation
- **Git**: For version control and cloning the repository
- **Virtual environment tool**: Either venv, conda, or another virtual environment manager

## Installation

### Option 1: Install from PyPI (Recommended)

```bash
# Create a virtual environment
python -m venv hephaestus-env
source hephaestus-env/bin/activate  # On Windows: hephaestus-env\Scripts\activate

# Install Hephaestus
pip install hephaestus
```

### Option 2: Install from Source

```bash
# Clone the repository
git clone https://github.com/username/hephaestus.git
cd hephaestus

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .
```

## Quick Start

Let's create a simple workflow to verify your installation is working correctly.

### 1. Create a Project Directory

```bash
mkdir hephaestus-demo
cd hephaestus-demo
```

### 2. Create a Basic Configuration File

Create a file named `config.yaml` with the following content:

```yaml
# Hephaestus configuration
project_name: "Demo Project"
output_dir: "./output"

# Component configuration
components:
  goal_proposer:
    enabled: true
    max_goals: 3
  
  mutation_engine:
    enabled: true
    mutation_strategies:
      - additive
      - refactoring
  
  test_harness:
    enabled: true
    timeout: 30  # seconds
  
  scoring:
    enabled: true
    metrics:
      - functionality
      - code_quality
      - performance

# Execution configuration
execution:
  mode: "direct"  # Options: direct, containerized, distributed
  resource_limits:
    memory_mb: 512
    cpu_time_seconds: 60
```

### 3. Create a Simple Directive

Create a file named `directive.yaml` that describes what you want to build:

```yaml
# Directive file
type: "function"
name: "calculate_factorial"
description: "Implement a function to calculate the factorial of a number"
requirements:
  - "The function should take a non-negative integer as input"
  - "The function should return the factorial of the input number"
  - "The function should handle edge cases (0, 1, negative numbers)"
  - "The function should be optimized for performance"
constraints:
  - "Use only the standard library"
  - "Include proper error handling"
  - "Add comprehensive docstrings"
```

### 4. Run Hephaestus

Now you can run Hephaestus with your configuration and directive:

```bash
hephaestus run --config config.yaml --directive directive.yaml
```

This will start the Hephaestus workflow, which will:
1. Process your directive
2. Generate code to implement the required functionality
3. Test the generated code
4. Score the implementation
5. Store the results in the output directory

## Understanding the Output

After running Hephaestus, check the `output` directory for the generated code and related artifacts:

```
output/
├── code/
│   └── calculate_factorial.py  # Generated function implementation
├── tests/
│   └── test_calculate_factorial.py  # Generated tests
├── reports/
│   ├── test_report.json       # Test results
│   └── scoring_report.json    # Scoring details
└── metadata.json              # Run metadata and provenance
```

The generated code should include a working implementation of the factorial function with proper documentation and error handling.

## Next Steps

Now that you've successfully run your first Hephaestus workflow, here are some next steps to explore:

### Learn About Components

Explore the core components that power Hephaestus:
- [Goal Proposer](../components/goal_proposer.md): Analyzes requirements and proposes development goals
- [Mutation Engine](../components/mutation.md): Generates code transformations to implement goals
- [Test Harness](../components/test_harness.md): Evaluates code against requirements and tests
- [Scoring System](../components/scoring.md): Assesses implementation quality

### Explore Advanced Features

- [Creating Custom Components](creating-components.md): Extend Hephaestus with your own components
- [Configuration Reference](../reference/configuration.md): Learn about all available configuration options
- [Directive Format](../components/directive_format.md): Learn how to write effective directives
- [Forge Loop](../components/forge_loop.md): Understand the iterative improvement process

### Try a Multi-Stage Workflow

For a more comprehensive example, try the [Multi-Stage Workflow Tutorial](multi-stage-workflow.md) that demonstrates how to build a more complex application with multiple components.

## Troubleshooting

If you encounter issues during installation or execution:

1. Verify your Python version: `python --version`
2. Check your dependencies: `pip list`
3. Look for error messages in the console output
4. Check the logs in the `output/logs` directory
5. Refer to the [Troubleshooting Guide](./troubleshooting.md)

If you need further assistance, please [open an issue](https://github.com/username/hephaestus/issues) on our GitHub repository. 