# Hephaestus Test and Debug Protocol

## Overview

This document outlines the testing and debugging protocols for the Hephaestus project. A robust testing strategy is essential for ensuring the system functions reliably, especially given its self-evolving nature. These protocols serve as guidelines for developers and contributors to maintain code quality and facilitate troubleshooting.

## Testing Philosophy

Hephaestus' testing philosophy aligns with its architectural principles:

1. **Recursive Validation** — Components that generate code must also validate code.
2. **Controlled Entropy** — Tests must allow for variation while ensuring core functionality.
3. **Evolutionary Stability** — Tests should favor incremental improvements over radical changes.

## Test Types

### 1. Unit Tests

Unit tests focus on individual components in isolation:

- **Node Tests**: Verify that each Node follows the `prep → exec → post` pattern correctly
- **Utility Tests**: Test helper functions and utility modules
- **Service Tests**: Validate the LLM service integration

Unit tests should use mocks for external dependencies (especially LLM services).

### 2. Integration Tests

Integration tests verify the interaction between components:

- **Node Chains**: Test sequences of Nodes working together
- **Flow Tests**: Verify that Flows orchestrate Nodes correctly
- **Service Integration**: Test the interaction between components and services

### 3. System Tests

System tests validate the complete Hephaestus engine:

- **End-to-End Tests**: Run full build cycles
- **Regression Tests**: Ensure new changes don't break existing functionality
- **Performance Tests**: Measure execution time and resource usage

### 4. Evolutionary Tests

Specific to Hephaestus' self-improving nature:

- **Lineage Tests**: Verify that the ancestry system functions correctly
- **Mutation Tests**: Ensure the MutationEngine creates valid variations
- **Selection Tests**: Validate that BestOfNBuilder correctly selects the best variants

## Testing Framework

### Setup

1. Use pytest as the primary testing framework
2. Organize tests to mirror the project structure
3. Leverage fixtures for common setup and teardown

```bash
tests/
├── __init__.py
├── test_engine/
│   ├── test_flow_builder.py
│   ├── test_best_of_n.py
│   └── test_forge_loop.py
├── test_nodes/
│   ├── test_base_node.py
│   └── test_flow.py
├── test_scoring/
│   └── test_scoring.py
├── test_services/
│   └── test_llm_service.py
└── conftest.py  # Shared fixtures and configuration
```

### Test Fixtures

Create fixtures for common scenarios:

```python
@pytest.fixture
def sample_registry():
    """Create a sample registry for testing."""
    return Registry(in_memory=True)

@pytest.fixture
def mock_llm_service():
    """Create a mock LLM service that returns predefined responses."""
    return MockLLMService(responses={
        "code_generation": "def hello_world():\n    print('Hello, world!')",
        "scoring": "0.85",
        "mutation": "Build a Node that processes JSON data"
    })

@pytest.fixture
def sample_shared_state():
    """Create a sample shared state for testing."""
    return {
        "build_task": "Build a Node that validates user input",
        "directive": {
            "description": "Input validation node",
            "constraints": ["Handle empty input", "Validate email format"]
        },
        "registry": {
            "builds": [],
            "lineage": {},
            "last_build_id": 0
        }
    }
```

## Debugging Protocols

### Logging Strategy

Implement comprehensive logging throughout the system:

1. **Component-Specific Loggers**: Each component should have its own logger
2. **Log Levels**: Use appropriate log levels (DEBUG, INFO, WARNING, ERROR)
3. **Context Information**: Include relevant context in log messages
4. **Traceable Execution**: Log entry and exit of key methods

```python
# Example logging setup
import logging

def setup_logging(log_level=logging.INFO):
    """Configure logging for the application."""
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("hephaestus.log"),
            logging.StreamHandler()
        ]
    )
    
    # Reduce verbosity of third-party libraries
    logging.getLogger("openai").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
```

### Debug Tools

Develop specialized debug tools for the Hephaestus system:

1. **State Inspector**: Tool to examine the shared state at any point
2. **Lineage Visualizer**: Visualize build ancestry
3. **Execution Tracer**: Track the flow of execution through components

```python
class StateInspector:
    """Tool for inspecting the shared state."""
    
    @staticmethod
    def dump(shared, file_path=None):
        """Dump the shared state to a file or stdout."""
        import json
        import sys
        
        # Filter out large objects
        filtered_state = {k: v for k, v in shared.items() 
                         if k not in ["code"]}
        
        # Format as JSON
        formatted = json.dumps(filtered_state, indent=2)
        
        if file_path:
            with open(file_path, "w") as f:
                f.write(formatted)
        else:
            print(formatted, file=sys.stderr)
```

### Error Handling

Implement a consistent error handling strategy:

1. **Graceful Degradation**: Allow the system to continue when possible
2. **Detailed Error Information**: Capture context for debugging
3. **Recovery Mechanisms**: Implement retry logic for transient failures

```python
class HephaestusError(Exception):
    """Base class for Hephaestus-specific exceptions."""
    
    def __init__(self, message, context=None):
        super().__init__(message)
        self.context = context or {}
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.error(f"{message} (context: {context})")
```

## Testing the BestOfNBuilder Integration

### Unit Tests

```python
def test_best_of_n_builder_init():
    """Test BestOfNBuilder initialization."""
    builder = BestOfNBuilder(n=5)
    assert builder.n == 5
    assert builder.mutation_engine is not None
    assert builder.flow_builder is not None
    assert builder.test_harness is not None

def test_best_of_n_builder_prep(sample_shared_state):
    """Test BestOfNBuilder prep method."""
    builder = BestOfNBuilder()
    result = builder.prep(sample_shared_state)
    assert "build_task" in result
    assert "directive" in result
    assert "registry" in result

def test_best_of_n_builder_exec(sample_shared_state, mock_mutation_engine):
    """Test BestOfNBuilder exec method."""
    builder = BestOfNBuilder(n=3, mutation_engine=mock_mutation_engine)
    prep_res = builder.prep(sample_shared_state)
    variants = builder.exec(prep_res)
    assert len(variants) <= 3  # May be less if some fail
    
    # Check variant structure
    if variants:
        variant = variants[0]
        assert "build_task" in variant
        assert "directive" in variant
        assert "code" in variant
        assert "score" in variant

def test_best_of_n_builder_post(sample_shared_state):
    """Test BestOfNBuilder post method."""
    builder = BestOfNBuilder()
    variants = [
        {"score": 0.5, "code": "code1", "variant_idx": 0},
        {"score": 0.8, "code": "code2", "variant_idx": 1},
        {"score": 0.3, "code": "code3", "variant_idx": 2}
    ]
    
    shared = sample_shared_state.copy()
    action = builder.post(shared, None, variants)
    
    assert action == "success"
    assert shared["score"] == 0.8
    assert shared["code"] == "code2"
    assert shared["feedback"]["best_variant_idx"] == 1
```

### Integration Tests

```python
def test_best_of_n_with_flow_builder(sample_shared_state, mock_llm_service):
    """Test BestOfNBuilder with FlowBuilderNode."""
    # Set up components
    flow_builder = FlowBuilderNode(llm_service=mock_llm_service)
    mutation_engine = MutationEngine(llm_service=mock_llm_service)
    test_harness = TestHarness()
    
    # Create BestOfNBuilder with mocked components
    builder = BestOfNBuilder(
        n=2,
        mutation_engine=mutation_engine,
        flow_builder=flow_builder,
        test_harness=test_harness
    )
    
    # Run the full flow
    shared = sample_shared_state.copy()
    action = builder.run(shared)
    
    # Verify results
    assert action in ["success", "fail"]
    if action == "success":
        assert "code" in shared
        assert "score" in shared
        assert "feedback" in shared
        assert "variants" in shared
        assert len(shared["variants"]) <= 2
```

### System Tests

```python
def test_forge_loop_with_best_of_n(mock_components):
    """Test ForgeLoop with BestOfNBuilder integration."""
    # Set up mock components
    goal_proposer, best_builder, registry = mock_components
    
    # Create ForgeLoop with mocked components
    forge = ForgeLoop(
        goal_proposer=goal_proposer,
        best_builder=best_builder,
        registry=registry
    )
    
    # Run a complete cycle
    shared = {"registry": registry.get_data()}
    feedback = forge.step(shared)
    
    # Verify the cycle completed correctly
    assert "best_score" in feedback
    assert best_builder.run.called  # Verify best_builder was called
    assert registry.register_build.called  # Verify registry was updated
```

## Continuous Integration

### GitHub Actions Workflow

```yaml
name: Hephaestus CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-cov
    - name: Test with pytest
      run: |
        pytest --cov=./ --cov-report=xml
    - name: Upload coverage report
      uses: codecov/codecov-action@v1
```

## Debug Protocol for LLM-Based Components

Working with LLM-generated content requires special consideration:

1. **Input/Output Logging**: Log both prompts and responses
2. **Deterministic Testing**: Use fixed seeds or mock responses
3. **Output Validation**: Verify structure and content of generated code

```python
class LLMDebugWrapper:
    """
    Wrapper for LLM services that logs all prompts and responses.
    """
    
    def __init__(self, llm_service, log_dir="logs/llm"):
        self.llm_service = llm_service
        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)
        self.logger = logging.getLogger("LLMDebug")
    
    async def generate(self, prompt, **kwargs):
        """Generate text, logging prompt and response."""
        # Log prompt
        request_id = str(uuid.uuid4())[:8]
        prompt_path = f"{self.log_dir}/{request_id}_prompt.txt"
        
        with open(prompt_path, "w") as f:
            f.write(prompt)
        
        # Call the actual service
        self.logger.info(f"LLM request {request_id}: {prompt[:50]}...")
        response = await self.llm_service.generate(prompt, **kwargs)
        
        # Log response
        response_path = f"{self.log_dir}/{request_id}_response.txt"
        with open(response_path, "w") as f:
            f.write(response)
        
        self.logger.info(f"LLM response {request_id}: {response[:50]}...")
        return response
```

## Monitoring and Performance

Implement monitoring for long-running evolutionary processes:

1. **Metrics Collection**: Track key performance indicators
2. **Progress Reporting**: Monitor the status of ongoing builds
3. **Resource Usage**: Track memory and CPU usage

```python
class HephaestusMonitor:
    """
    Monitor for tracking Hephaestus performance metrics.
    """
    
    def __init__(self):
        self.metrics = {
            "cycles": 0,
            "builds": 0,
            "successful_builds": 0,
            "failed_builds": 0,
            "avg_score": 0,
            "cycle_times": [],
            "api_calls": 0,
            "llm_tokens": 0
        }
        
    def start_cycle(self):
        """Start timing a new cycle."""
        self.cycle_start = time.time()
        
    def end_cycle(self, results):
        """End cycle timing and update metrics."""
        cycle_time = time.time() - self.cycle_start
        self.metrics["cycles"] += 1
        self.metrics["cycle_times"].append(cycle_time)
        
        # Update other metrics based on results
        if results.get("status") == "success":
            self.metrics["successful_builds"] += 1
        else:
            self.metrics["failed_builds"] += 1
        
        self.metrics["builds"] += 1
        
        # Update average score
        current_avg = self.metrics["avg_score"]
        new_score = results.get("score", 0)
        self.metrics["avg_score"] = (current_avg * (self.metrics["builds"] - 1) + new_score) / self.metrics["builds"]
        
    def report(self):
        """Generate a performance report."""
        return {
            "total_cycles": self.metrics["cycles"],
            "success_rate": self.metrics["successful_builds"] / max(1, self.metrics["builds"]),
            "avg_cycle_time": sum(self.metrics["cycle_times"]) / max(1, len(self.metrics["cycle_times"])),
            "avg_score": self.metrics["avg_score"],
            "total_llm_tokens": self.metrics["llm_tokens"]
        }
```

## Conclusion

This test and debug protocol provides a comprehensive framework for ensuring the reliability and performance of the Hephaestus system. By following these guidelines, developers can maintain code quality while enabling the evolutionary nature of the project.

The protocols should be regularly reviewed and updated as the system evolves, ensuring they remain effective for catching issues and providing meaningful debug information. 