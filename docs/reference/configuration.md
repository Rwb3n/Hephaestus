# Configuration Reference

This page provides detailed information about configuring the Hephaestus system.

## Configuration File

Hephaestus uses a YAML configuration file that can be specified with the `--config` flag:

```bash
python -m hephaestus --config config.yaml
```

If not specified, Hephaestus looks for configuration in these locations (in order):
1. `./hephaestus.yaml` (current directory)
2. `~/.hephaestus/config.yaml` (user home directory)
3. Default configuration (built-in)

## Core Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `log_level` | string | `"INFO"` | Logging level (`DEBUG`, `INFO`, `WARNING`, `ERROR`) |
| `registry_path` | string | `"./registry"` | Directory path for component registry |
| `max_workers` | integer | `4` | Maximum number of parallel workers |
| `cache_dir` | string | `"~/.hephaestus/cache"` | Directory for caching |

## LLM Configuration

```yaml
llm:
  provider: "openai"  # "openai", "anthropic", "local"
  model: "gpt-4"      # Model to use
  temperature: 0.7    # Creativity level (0.0-1.0)
  max_tokens: 2000    # Maximum response tokens
  timeout: 30         # Request timeout in seconds
  retry_attempts: 3   # Number of retry attempts
  
  # Provider-specific settings
  openai:
    api_key: "${OPENAI_API_KEY}"  # Environment variable reference
    
  anthropic:
    api_key: "${ANTHROPIC_API_KEY}"
    
  local:
    endpoint: "http://localhost:8000/v1"
    model_path: "./models/llama-7b"
```

## Code Generation Settings

```yaml
generation:
  best_of_n: 3          # Number of variants to generate
  timeout: 120          # Generation timeout in seconds
  max_line_length: 88   # Maximum line length
  pydocstyle: true      # Enforce docstring style
  enforce_typing: true  # Enforce type hints
```

## Testing Configuration

```yaml
testing:
  test_timeout: 10        # Maximum test execution time (seconds)
  coverage_threshold: 80  # Minimum test coverage percentage
  max_test_cases: 10      # Maximum number of test cases to generate
  test_frameworks:        # Test frameworks to use
    - pytest
```

## Scoring Configuration

```yaml
scoring:
  weights:
    functionality: 0.5    # Weight for functionality score
    quality: 0.3          # Weight for code quality score
    performance: 0.2      # Weight for performance score
  
  quality:
    max_complexity: 10    # Maximum cyclomatic complexity
    
  performance:
    benchmark_iterations: 5  # Number of benchmark iterations
```

## Forge Loop Configuration

```yaml
forge:
  enabled: true           # Enable the forge loop
  interval: 3600          # Run interval in seconds (0 for continuous)
  max_mutations: 5        # Maximum mutations per component
  selection_strategy: "random"  # Component selection strategy
```

## Environment Variables

Hephaestus supports environment variables for sensitive configuration or deployment-specific settings. In the configuration file, use `${ENV_VAR_NAME}` syntax to reference an environment variable.

Required environment variables:
- `OPENAI_API_KEY` (if using OpenAI)
- `ANTHROPIC_API_KEY` (if using Anthropic)

Optional environment variables:
- `HEPHAESTUS_LOG_LEVEL`
- `HEPHAESTUS_REGISTRY_PATH`
- `HEPHAESTUS_CACHE_DIR`

## Example Configuration

```yaml
log_level: "INFO"
registry_path: "./registry"
max_workers: 4

llm:
  provider: "openai"
  model: "gpt-4"
  temperature: 0.7
  max_tokens: 2000
  openai:
    api_key: "${OPENAI_API_KEY}"

generation:
  best_of_n: 3
  timeout: 120
  max_line_length: 88
  enforce_typing: true

testing:
  test_timeout: 10
  coverage_threshold: 80
  test_frameworks:
    - pytest

scoring:
  weights:
    functionality: 0.5
    quality: 0.3
    performance: 0.2

forge:
  enabled: true
  interval: 3600
  max_mutations: 5
  selection_strategy: "random"
``` 