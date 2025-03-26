---
title: Running Tests
description: A comprehensive guide to running and interpreting tests in Hephaestus
---

# Running Tests in Hephaestus

This guide explains how to run tests for the Hephaestus project, interpret test results, and troubleshoot common testing issues.

## Prerequisites

Before running tests, ensure you have:

1. A working Hephaestus installation (see [Installation Guide](../index.md))
2. Python 3.8+ with pip installed
3. Required dependencies installed:
   ```bash
   pip install -r requirements-dev.txt
   ```

## Test Types

Hephaestus includes several types of tests:

| Test Type | Description | Directory | Run Command |
|-----------|-------------|-----------|------------|
| Unit Tests | Verify individual components in isolation | `tests/unit/` | `pytest tests/unit/` |
| Integration Tests | Test interactions between components | `tests/integration/` | `pytest tests/integration/` |
| End-to-End Tests | Test complete system workflows | `tests/e2e/` | `pytest tests/e2e/` |
| Performance Tests | Benchmark system performance | `tests/performance/` | `pytest tests/performance/` |

## Running Tests

### Running All Tests

To run all tests:

```bash
pytest
```

### Running Specific Test Types

To run a specific type of test:

```bash
# Run unit tests only
pytest tests/unit/

# Run integration tests only
pytest tests/integration/

# Run end-to-end tests only
pytest tests/e2e/

# Run performance tests only
pytest tests/performance/
```

### Running Specific Test Files

To run tests from a specific file:

```bash
pytest tests/unit/test_mutation_engine.py
```

### Running Individual Tests

To run a specific test:

```bash
pytest tests/unit/test_mutation_engine.py::test_code_generation
```

## Test Options

Hephaestus tests support various pytest options:

| Option | Description | Example |
|--------|-------------|---------|
| `-v` | Verbose output | `pytest -v` |
| `-s` | Show print output | `pytest -s` |
| `-k` | Run tests matching expression | `pytest -k "mutation"` |
| `--tb=short` | Short traceback format | `pytest --tb=short` |
| `--cov=hephaestus` | Generate coverage report | `pytest --cov=hephaestus` |
| `--html=report.html` | Generate HTML report | `pytest --html=report.html` |

## Test Configuration

### pytest.ini

The `pytest.ini` file contains global test configuration:

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_functions = test_*
markers =
    unit: mark a test as a unit test
    integration: mark a test as an integration test
    e2e: mark a test as an end-to-end test
    performance: mark a test as a performance test
    slow: mark test as slow (skipped by default)
```

### conftest.py

The `conftest.py` file contains shared test fixtures and helper functions. Global fixtures include:

- `config`: Default configuration for testing
- `temp_registry`: Temporary registry for testing
- `test_harness`: Pre-configured test harness
- `mutation_engine`: Isolated mutation engine

## Test Fixtures

Use fixtures to set up test environments:

```python
# Example test using fixtures
def test_mutation_with_directive(temp_registry, test_harness):
    # Test code using fixtures
    assert test_harness.verify(temp_registry.get_latest())
```

## Writing Tests

When writing new tests:

1. Place them in the appropriate directory based on type
2. Use descriptive test names that explain what's being tested
3. Follow the AAA pattern: Arrange, Act, Assert
4. Use appropriate markers
5. Leverage existing fixtures when possible

Example:

```python
import pytest
from hephaestus.mutation import MutationEngine

@pytest.mark.unit
def test_mutation_engine_generates_valid_code():
    # Arrange
    engine = MutationEngine()
    directive = {
        "type": "feature",
        "description": "Add user authentication",
        "constraints": {"language": "python"}
    }
    
    # Act
    code = engine.generate(directive)
    
    # Assert
    assert code is not None
    assert "def authenticate_user" in code
```

## Interpreting Test Results

Test results include:

- **Pass**: Test succeeded (`.`)
- **Fail**: Test failed (`F`)
- **Error**: Exception occurred during test (`E`)
- **Skip**: Test was skipped (`s`)
- **xFail**: Expected failure (`x`)
- **xPass**: Unexpected pass (`X`)

Example output:

```
collected 145 items

tests/unit/test_goal_proposer.py .......                             [  4%]
tests/unit/test_mutation_engine.py .....FF...                        [ 11%]
tests/unit/test_registry.py .................                        [ 22%]
tests/unit/test_scoring.py ............                              [ 30%]
tests/unit/test_test_harness.py ..................                   [ 42%]
tests/integration/test_goal_mutation.py ...........                  [ 50%]
tests/integration/test_mutation_testing.py ..........               [ 57%]
tests/integration/test_scoring_feedback.py .........                [ 63%]
tests/integration/test_forge_loop.py ..............                 [ 73%]
tests/e2e/test_code_generation.py .........                         [ 80%]
tests/e2e/test_improvement_cycle.py ............                    [ 88%]
tests/performance/test_mutation_performance.py .....                [ 91%]
tests/performance/test_registry_performance.py .....               [ 95%]
tests/performance/test_forge_performance.py .....                  [100%]

FAILURES
========
...
```

## Code Coverage

Generate a coverage report:

```bash
pytest --cov=hephaestus --cov-report=html
```

This creates a detailed HTML report in the `htmlcov/` directory, showing which lines of code are covered by tests.

## Continuous Integration

Hephaestus uses GitHub Actions for CI testing. Each pull request automatically runs:

1. Unit tests
2. Integration tests
3. Code coverage analysis
4. Linting checks

See `.github/workflows/test.yml` for configuration details.

## Common Testing Issues

### Tests Taking Too Long

For slow tests:

1. Mark them with `@pytest.mark.slow`
2. Skip them in normal runs: `pytest -k "not slow"`
3. Run them explicitly when needed: `pytest -m slow`

### Resource-Intensive Tests

For resource-intensive tests:

1. Use the `@pytest.mark.resource_intensive` marker
2. Implement cleanup in fixtures using `yield` and `finally`
3. Use `pytest.xfail` for tests that may fail due to resource constraints

### Flaky Tests

For tests that occasionally fail:

1. Identify the cause (race conditions, timing issues, external dependencies)
2. Add appropriate retries or stabilizing code
3. If necessary, mark as `@pytest.mark.flaky(reruns=3)`

## Debugging Tests

When tests fail:

1. Use `-v` for verbose output
2. Add `--pdb` to drop into debugger on failure
3. Add print statements with `-s` option
4. Inspect test logs in the `.test_logs/` directory
5. Use the `PYTEST_DEBUG=1` environment variable for extra debug info

## Mock Objects

Use mocks to isolate components:

```python
from unittest.mock import Mock, patch

def test_forge_loop_with_mock_mutation():
    with patch('hephaestus.mutation.MutationEngine') as mock_engine:
        mock_engine.return_value.generate.return_value = "mock code"
        # Test code using mock_engine
```

## Test Data

Test data files are stored in `tests/data/`. Access them using the `load_test_data` helper:

```python
from tests.helpers import load_test_data

def test_with_sample_directive():
    directive = load_test_data("directives/sample_feature.yaml")
    # Test using directive
```

## Advanced Testing

### Parametrized Tests

For testing multiple cases:

```python
@pytest.mark.parametrize("input_data,expected", [
    ({"type": "feature"}, True),
    ({"type": "invalid"}, False),
    ({}, False),
])
def test_directive_validation(input_data, expected):
    assert validate_directive(input_data) == expected
```

### Property-Based Testing

For more comprehensive test coverage:

```python
import hypothesis
from hypothesis import strategies as st

@hypothesis.given(st.dictionaries(
    keys=st.text(),
    values=st.one_of(st.text(), st.integers())
))
def test_registry_stores_arbitrary_metadata(metadata):
    registry = Registry()
    registry.store("test_id", "test_code", metadata)
    retrieved = registry.get_metadata("test_id")
    assert retrieved == metadata
```

## Test Harness Component

The Hephaestus Test Harness component provides additional testing capabilities:

```python
from hephaestus.test_harness import TestHarness

harness = TestHarness()
result = harness.run_tests("test_implementation", test_suite="authentication")
```

See the [Test Harness documentation](../components/test_harness.md) for more details.

## Conclusion

Thorough testing is essential for maintaining Hephaestus's reliability and quality. By following these testing practices, you'll help ensure that the system functions correctly and continues to improve. 