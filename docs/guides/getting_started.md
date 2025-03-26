# Getting Started with Hephaestus

**Version**: 0.1.1  
**Last Updated**: March 29, 2025  
**Audience**: Developers  
**Difficulty**: Beginner  

## Overview

This guide will help you get started with the Hephaestus code generation system. It covers the basic setup, configuration, and usage of the system.

## Prerequisites

- Python 3.8+
- Git
- OpenAI API key (for LLM integration)
- Basic understanding of Python and AI concepts

## Step-by-Step Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-org/hephaestus.git
cd hephaestus
```

**Expected Outcome**: The Hephaestus codebase is downloaded to your local machine and you are in the project directory.

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

**Expected Outcome**: All required dependencies are installed in your Python environment.

### 3. Configure Environment

Create a `.env` file in the project root with your API keys:

```
OPENAI_API_KEY=your_api_key_here
```

**Expected Outcome**: Your environment is configured with the necessary API keys.

### 4. Run a Basic Build

```bash
python run.py --directive "Create a simple logging utility"
```

**Expected Outcome**: Hephaestus will generate, test, and score a logging utility implementation.

## Common Use Cases

### Use Case 1: Generate a Component

```python
from hephaestus.engine import FlowBuilder
from hephaestus.core import Node

# Create a flow builder
builder = FlowBuilder()

# Generate a component
result = builder.build("Create a component that validates email addresses")
print(result.code)
```

### Use Case 2: Evaluating Generated Code

```python
from hephaestus.scoring import Scorer

# Initialize the scorer
scorer = Scorer()

# Score some code
score = scorer.score(code, "Validate that the code correctly validates email addresses")
print(f"Code score: {score}")
```

## Troubleshooting

### Common Issue 1: API Key Issues

**Symptom**: Error message about invalid API key or authentication.

**Cause**: API key is incorrect or not properly set in the environment.

**Resolution**: Double-check your API key and ensure it's correctly set in the `.env` file.

### Common Issue 2: Dependency Errors

**Symptom**: Import errors when running the code.

**Cause**: Missing or incompatible dependencies.

**Resolution**: Ensure you've installed all dependencies with `pip install -r requirements.txt`.

## Best Practices

- Start with simple directives before trying complex ones
- Use specific and clear directives for better results
- Check the logs if something isn't working as expected
- Review generated code before using it in production

## Related Guides

- [Configuration Guide](configuration.md) - Detailed configuration options
- [Migration Guide](migration_guide.md) - How to migrate from older versions 