# API Reference

This page provides a reference for the core classes and functions in the Hephaestus system.

> Note: This is a preliminary API reference. As the system evolves, this documentation will be automatically generated from docstrings.

## Core Components

### Node

The fundamental building block for all operations in Hephaestus.

```python
class Node:
    def __init__(self, max_retries=1, wait=0)
    
    def prep(self, shared)
    
    def exec(self, prep_res)
    
    def exec_fallback(self, prep_res, exc)
    
    def post(self, shared, prep_res, exec_res)
    
    def run(self, shared)
```

#### Parameters
- `max_retries` (int): Maximum number of retries for the exec function. Default is 1 (no retries).
- `wait` (int): Wait time in seconds before retrying. Default is 0.

#### Methods
- `prep(shared)`: Preparation phase. Reads from shared context and returns data for execution.
- `exec(prep_res)`: Execution phase. Performs the actual computation using the prepared data.
- `exec_fallback(prep_res, exc)`: Called when exec fails after all retries. By default, re-raises the exception.
- `post(shared, prep_res, exec_res)`: Post-processing phase. Writes results to shared context and returns an action.
- `run(shared)`: Executes the full node lifecycle (prep->exec->post).

### BatchNode

A specialized node for processing multiple items in parallel.

```python
class BatchNode(Node):
    def prep(self, shared)
    
    def exec(self, item)
    
    def post(self, shared, prep_res, exec_res_list)
```

#### Methods
- `prep(shared)`: Returns an iterable of items to process.
- `exec(item)`: Called once for each item returned by prep.
- `post(shared, prep_res, exec_res_list)`: Receives a list of all exec results.

### Flow

A directed graph of nodes that orchestrates the execution flow.

```python
class Flow(Node):
    def __init__(self, start=None)
    
    def add_node(self, node)
    
    def add_edge(self, source, target, action="default")
    
    def run(self, shared)
    
    def set_params(self, params)
```

#### Parameters
- `start` (Node): The starting node of the flow.

#### Methods
- `add_node(node)`: Adds a node to the flow.
- `add_edge(source, target, action="default")`: Adds an edge between nodes for a specific action.
- `run(shared)`: Executes the flow, starting from the start node.
- `set_params(params)`: Sets parameters for the flow and all its nodes.

## Code Generation Components

### FlowBuilderNode

A specialized node for generating code using language models.

```python
class FlowBuilderNode(Node):
    def __init__(self, llm_provider, max_retries=3)
    
    def prep(self, shared)
    
    def exec(self, directive)
    
    def post(self, shared, prep_res, exec_res)
```

#### Parameters
- `llm_provider`: The language model provider to use.
- `max_retries` (int): Maximum number of retries for the LLM call. Default is 3.

### BestOfNBuilder

Generates multiple variants of a component and selects the best one.

```python
class BestOfNBuilder(Flow):
    def __init__(self, generator_node, scorer_node, n=3)
```

#### Parameters
- `generator_node`: The node responsible for generating code.
- `scorer_node`: The node responsible for scoring generated code.
- `n` (int): Number of variants to generate. Default is 3.

## Testing Components

### TestHarnessNode

Executes tests against generated components.

```python
class TestHarnessNode(Node):
    def __init__(self, test_runner, timeout=10)
    
    def prep(self, shared)
    
    def exec(self, code_and_tests)
    
    def post(self, shared, prep_res, exec_res)
```

#### Parameters
- `test_runner`: The test execution engine to use.
- `timeout` (int): Maximum test execution time in seconds. Default is 10.

## Scoring Components

### ScorerNode

Base class for all scorer nodes.

```python
class ScorerNode(Node):
    def __init__(self, score_range=(0.0, 1.0))
    
    def normalize_score(self, score)
```

#### Parameters
- `score_range` (tuple): The range for normalized scores. Default is (0.0, 1.0).

#### Methods
- `normalize_score(score)`: Normalizes a score to the specified range.

### FunctionalityScorer

Evaluates if code meets functional requirements.

```python
class FunctionalityScorer(ScorerNode):
    def __init__(self, test_harness)
```

#### Parameters
- `test_harness`: The test harness to use for evaluation.

### QualityScorer

Evaluates code quality, style, and best practices.

```python
class QualityScorer(ScorerNode):
    def __init__(self, llm_provider)
```

#### Parameters
- `llm_provider`: The language model provider to use for evaluation.

## Registry Components

### RegistryNode

Manages the component registry.

```python
class RegistryNode(Node):
    def __init__(self, registry_path="./registry")
    
    def register_component(self, component_id, code, metadata)
    
    def get_component(self, component_id)
    
    def list_components(self, filter_func=None)
```

#### Parameters
- `registry_path` (str): Path to the registry directory. Default is "./registry".

#### Methods
- `register_component(component_id, code, metadata)`: Registers a new component.
- `get_component(component_id)`: Retrieves a component by ID.
- `list_components(filter_func=None)`: Lists components, optionally filtered.

## Improvement Components

### MutationEngine

Creates improved variants of existing components.

```python
class MutationEngine(Flow):
    def __init__(self, llm_provider, mutation_strategies=None)
```

#### Parameters
- `llm_provider`: The language model provider to use.
- `mutation_strategies`: List of mutation strategies to apply. If None, uses default strategies.

### ForgeLoop

Orchestrates the continuous improvement cycle.

```python
class ForgeLoop(Flow):
    def __init__(self, registry_node, mutation_engine, test_harness, scorers)
```

#### Parameters
- `registry_node`: The registry node to use.
- `mutation_engine`: The mutation engine to use.
- `test_harness`: The test harness to use.
- `scorers`: A list of scorer nodes to use. 