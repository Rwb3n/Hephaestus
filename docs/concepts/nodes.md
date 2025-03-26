# Nodes

Nodes are the fundamental building blocks of the Hephaestus system, providing atomic units of computation that can be composed into complex workflows.

## Overview

In Hephaestus, a Node represents a discrete unit of work with a clear input, process, and output pattern. Nodes are designed to be modular, reusable, and focused on a single responsibility, making the system easier to understand, test, and extend.

## Node Lifecycle

Each Node goes through a three-step lifecycle during execution:

1. **Preparation (prep)**: Reads data from the shared context and prepares it for execution
2. **Execution (exec)**: Performs the core computation or action using the prepared data
3. **Post-processing (post)**: Processes the results and writes them back to the shared context

This clear separation of concerns allows for proper error handling, efficient resource usage, and clear data flow.

## Node Structure

A typical Node implementation follows this pattern:

```python
from hephaestus.core import Node

class MyNode(Node):
    def prep(self, shared):
        # Read from shared context
        input_data = shared.get("some_key", default_value)
        # Return data needed for execution
        return input_data
    
    def exec(self, prep_res):
        # Process the data
        result = some_computation(prep_res)
        # Return the processed result
        return result
    
    def post(self, shared, prep_res, exec_res):
        # Store results in shared context
        shared["result_key"] = exec_res
        # Return an action (determines the next node to execute)
        return "next_action"
```

## Node Types

Hephaestus includes several specialized types of Nodes:

### Basic Node

The standard Node implementation with the three-phase lifecycle.

### BatchNode

A specialized Node that processes multiple items in a batch, allowing for efficient handling of collections.

```python
class MyBatchNode(BatchNode):
    def prep(self, shared):
        # Return a list of items to process
        return shared.get("items", [])
    
    def exec(self, item):
        # Process a single item (called once per item)
        return process(item)
    
    def post(self, shared, prep_res, exec_res_list):
        # Handle the list of results from all items
        shared["results"] = exec_res_list
        return "next"
```

### FlowBuilderNode

A specialized Node for generating code based on directives, leveraging language models.

### Specialized Component Nodes

- **ScorerNode**: Evaluates code quality and correctness
- **TestHarnessNode**: Runs tests against generated code
- **RegistryNode**: Manages code artifacts and lineage tracking

## Node Communication

Nodes communicate with each other through:

1. **Shared Context**: A dictionary-like object accessible by all Nodes in a Flow
2. **Actions**: Strings returned by `post()` that determine the next Node to execute

## Best Practices for Node Design

- **Single Responsibility**: Each Node should do one thing well
- **Clear Input/Output**: Define clear contracts for what the Node expects and provides
- **Error Handling**: Handle errors gracefully, with appropriate fallbacks
- **Testability**: Design Nodes to be easily testable in isolation
- **Documentation**: Document the purpose, inputs, outputs, and assumptions of each Node

## Examples

### Data Processing Node

```python
class DataProcessorNode(Node):
    def prep(self, shared):
        return shared.get("data", [])
    
    def exec(self, data):
        return [item * 2 for item in data]
    
    def post(self, shared, prep_res, exec_res):
        shared["processed_data"] = exec_res
        return "continue"
```

### LLM Integration Node

```python
class LLMNode(Node):
    def prep(self, shared):
        return shared.get("prompt", "")
    
    def exec(self, prompt):
        # Call LLM service
        return call_llm(prompt)
    
    def post(self, shared, prep_res, exec_res):
        shared["llm_response"] = exec_res
        return "process_response"
``` 