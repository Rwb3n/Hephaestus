---
title: Troubleshooting Guide
description: Comprehensive solutions for common issues when working with Hephaestus
---

# Troubleshooting Guide

This guide provides solutions for common issues you might encounter when working with Hephaestus.

## Table of Contents

- [Installation Issues](#installation-issues)
- [Configuration Issues](#configuration-issues)
- [API Connection Issues](#api-connection-issues)
- [Execution Issues](#execution-issues)
- [Directive Issues](#directive-issues)
- [Code Generation Issues](#code-generation-issues)
- [Performance Issues](#performance-issues)
- [Component Registry Issues](#component-registry-issues)
- [Debugging Tips](#debugging-tips)
- [Getting Help](#getting-help)
- [Common Error Messages](#common-error-messages)

## Installation Issues

### Package Dependencies

**Issue**: Missing or incompatible dependencies during installation.

**Solution**:
- Ensure you're using Python 3.9 or newer
- Try installing with the `--upgrade` flag: `pip install --upgrade hephaestus`
- If installing from source, use `pip install -e ".[dev]"` to include development dependencies

### Virtual Environment Problems

**Issue**: Conflicts with existing packages in your environment.

**Solution**:
- Create a fresh virtual environment: `python -m venv hephaestus-env`
- Activate the environment before installing: 
  ```bash
  # Windows
  hephaestus-env\Scripts\activate
  
  # Linux/Mac
  source hephaestus-env/bin/activate
  ```
- Install Hephaestus in the clean environment

### Missing System Dependencies

**Symptoms**: Installation fails with cryptic errors about missing libraries.

**Solution**:

For Linux:
```bash
sudo apt-get update
sudo apt-get install python3-dev build-essential
```

For Mac:
```bash
brew install python
xcode-select --install
```

For Windows, ensure you have the [Visual C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/) installed.

## Configuration Issues

### Invalid Configuration

**Issue**: Errors about invalid configuration format or missing required fields.

**Solution**:
- Verify your YAML syntax is correct
- Check for proper indentation
- Ensure all required fields are present
- Use a YAML validator to check your configuration files

### Component Configuration

**Issue**: Components not behaving as expected due to configuration issues.

**Solution**:
- Make sure all components you're using are set to `enabled: true`
- Check component-specific configuration parameters
- Look for typos in component names or parameter names
- Set `log_level: "debug"` for more detailed logs

## API Connection Issues

### API Key Not Found

**Symptoms**: The system fails with an error message about missing API keys:
```
Error: OpenAI API key not found
```

**Solution**:
1. Ensure you have set the appropriate environment variable:
   ```bash
   # For Windows PowerShell
   $env:OPENAI_API_KEY = "your-api-key"
   
   # For Linux/Mac
   export OPENAI_API_KEY="your-api-key"
   ```
2. Verify your configuration file has the correct reference to the environment variable
3. Restart your terminal or application after setting the environment variable

### API Rate Limit Exceeded

**Symptoms**: Operations fail with rate limit errors:
```
Error: Rate limit exceeded, please try again later
```

**Solution**:
1. Check your API usage dashboard for limits
2. Add a retry mechanism with exponential backoff in the configuration:
   ```yaml
   llm:
     retry_attempts: 5
     retry_delay: 2  # seconds, doubles each retry
   ```
3. Consider implementing a queue system for large batches of requests

## Execution Issues

### Memory Errors

**Issue**: Out of memory errors during execution.

**Solution**:
- Increase memory limits in configuration: `memory_mb: 1024`
- Reduce the complexity of your directive or split it into smaller parts
- Ensure you don't have other memory-intensive applications running
- Enable memory-efficient processing:
  ```yaml
  system:
    memory_efficient: true
  ```

### Timeout Errors

**Issue**: Execution exceeds the configured timeout.

**Solution**:
- Increase the timeout in your configuration: `timeout: 60`
- Simplify your directive to reduce computation time
- Check if your system is under heavy load

### Permission Errors

**Issue**: Permission denied errors when accessing files or resources.

**Solution**:
- Check file permissions for input/output directories
- Run with appropriate privileges for the needed resources
- Use relative paths within your project directory

## Directive Issues

### Directive Parsing Errors

**Issue**: Errors about invalid directive format.

**Solution**:
- Verify your YAML syntax
- Ensure all required fields are present (type, name, description, requirements)
- Check for proper indentation and formatting
- Refer to the [Directive Format](../components/directive_format.md) documentation

### Unclear Directives

**Issue**: Poor quality or unexpected code generated due to ambiguous directives.

**Solution**:
- Make your requirements more specific and detailed
- Add constraints to guide the implementation
- Provide examples of expected behavior
- Use more precise language and avoid ambiguity

## Code Generation Issues

### Low-Quality Code

**Issue**: Generated code doesn't meet expectations or has issues.

**Solution**:
- Review and refine your directive to be more specific
- Increase the number of improvement iterations: `max_iterations: 5`
- Add more detailed constraints and requirements
- Enable additional quality metrics in the scoring configuration
- Enable more detailed prompting:
  ```yaml
  generation:
    detailed_instructions: true
    examples_count: 3
  ```

### Test Failures

**Issue**: Generated code fails tests.

**Solution**:
- Check the test failure messages in the logs
- Review your directive requirements for clarity
- Increase the number of improvement iterations
- Examine test cases to ensure they accurately reflect requirements
- Increase the sample size for generation:
  ```yaml
  generation:
    best_of_n: 5  # Try more variants
  ```

## Performance Issues

### Slow Execution

**Issue**: Hephaestus runs very slowly.

**Solution**:
- Reduce `max_iterations` for quicker runs during development
- Simplify directives for testing
- Disable components you don't need for specific runs
- Check system resources (CPU, memory) during execution
- Adjust parallel processing settings:
  ```yaml
  system:
    max_workers: 4  # Increase if you have more cores
  ```

### High Resource Usage

**Issue**: Hephaestus consumes excessive system resources.

**Solution**:
- Configure stricter resource limits
- Run fewer parallel iterations if using batch mode
- Close other resource-intensive applications
- Enable caching:
  ```yaml
  system:
    enable_cache: true
    cache_dir: "./cache"
  ```

## Component Registry Issues

### Component Registry Corruption

**Symptoms**: Missing components, unexpected errors when accessing the registry.

**Solution**:
1. Check for filesystem issues or permission problems
2. Try loading a registry backup:
   ```bash
   python -m hephaestus --restore-registry backup-20250329
   ```
3. If corruption persists, rebuild the affected components:
   ```bash
   python -m hephaestus --rebuild-component component_id
   ```

## Debugging Tips

### Enabling Debug Logs

For more detailed information, set the log level to debug in your configuration:

```yaml
log_level: "debug"
```

### Using Verbose Mode

Run Hephaestus with the verbose flag for more detailed console output:

```bash
hephaestus run --config config.yaml --directive directive.yaml --verbose
```

### Examining Log Files

Check the log files in the output directory for detailed execution information:

```
output/
└── logs/
    ├── hephaestus.log        # Main log file
    ├── components/           # Component-specific logs
    └── execution/            # Execution-related logs
```

### Step-by-Step Execution

For complex issues, try running components individually to isolate problems:

```bash
hephaestus goal-proposer --directive directive.yaml --output goal.json
hephaestus mutation --goal goal.json --output code.py
```

### Isolating Components

To test individual components in isolation:

```bash
python -m hephaestus.debug --test-node RegistryNode
```

## Getting Help

If you're still experiencing issues:

1. Search the [GitHub issues](https://github.com/username/hephaestus/issues) for similar problems
2. Check the [FAQ](../about/faq.md) for additional information
3. Use the `--diagnostic` flag to generate a diagnostic report:
   ```bash
   python -m hephaestus --diagnostic > diagnostic.txt
   ```
4. Open a new issue with:
   - A detailed description of the problem
   - Steps to reproduce
   - Relevant configuration files
   - Log outputs
   - Your system information (OS, Python version, etc.)

## Common Error Messages

### "Component X failed with error Y"

Check the component-specific configuration and ensure it has all required parameters.

### "No valid implementation found after N iterations"

The system couldn't generate a satisfactory implementation within the configured number of iterations. Try:
- Increasing `max_iterations`
- Simplifying the directive
- Providing more specific requirements

### "Resource limit exceeded"

The execution exceeded the configured resource limits. Increase the relevant limit or optimize your directive.

### "Invalid directive schema"

Your directive doesn't match the expected format. Check the [Directive Format](../components/directive_format.md) documentation.

### "No compatible executor found"

The system couldn't find an appropriate execution environment. Check your execution configuration and installed dependencies. 