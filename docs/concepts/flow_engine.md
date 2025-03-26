# Flow Engine

The Flow Engine is a core concept in the Hephaestus system, providing the foundation for building complex, multi-step processes.

## Overview

The Flow Engine in Hephaestus is based on the Node/Flow pattern from PocketFlow. It allows for the construction of complex, directed flows of computation by connecting nodes together into a graph.

## Key Concepts

### Nodes

Nodes are the fundamental building blocks of the Flow Engine. Each Node represents a discrete unit of work with three main phases:

1. **Preparation (prep)**: Reads from shared context and prepares data for execution
2. **Execution (exec)**: Performs the main computation or action
3. **Post-processing (post)**: Writes results back to shared context and determines the next action

Nodes are designed to be composable, reusable, and focused on a single responsibility.

### Flows

Flows are collections of Nodes connected in a directed graph. A Flow orchestrates the execution of Nodes in a specific order, with branches and decision points determined by the Actions returned from each Node's post-processing phase.

Flows manage a shared context that all Nodes can access, allowing for data to be passed between Nodes throughout the execution process.

### Actions

Actions are the connective tissue between Nodes in a Flow. When a Node completes its execution, it returns an Action that determines which Node should execute next.

This action-based routing allows for dynamic, conditional execution paths based on the results of each Node's work.

### Shared Context

The shared context is a dictionary-like object that all Nodes in a Flow can access. It serves as a shared memory space for the Flow, allowing Nodes to communicate with each other.

Nodes can read from and write to the shared context, enabling complex data pipelines where each Node builds upon the work of previous Nodes.

## Flow Engine in Practice

In Hephaestus, the Flow Engine is used extensively:

- **FlowBuilderNode**: Uses the Flow Engine to orchestrate the code generation process
- **MutationEngine**: Uses Flows to apply variations to task descriptions
- **BestOfNBuilder**: Uses Flows to generate multiple code variants and select the best one
- **ForgeLoop**: Uses a high-level Flow to orchestrate the entire build-test-score cycle

## Benefits of the Flow Engine

- **Modularity**: Each Node has a single responsibility, making the system easier to extend and maintain
- **Testability**: Nodes can be tested in isolation, improving test coverage and reliability
- **Flexibility**: Flows can be reconfigured and extended with minimal changes to existing code
- **Visibility**: The explicit flow structure makes it easier to understand the system's behavior

## Example: Simple Flow

```python
from hephaestus.core import Node, Flow

class ReadInput(Node):
    def prep(self, shared):
        return shared.get("input", "")
        
    def exec(self, input_data):
        return input_data.upper()
        
    def post(self, shared, prep_res, exec_res):
        shared["processed_input"] = exec_res
        return "process"

class ProcessData(Node):
    def prep(self, shared):
        return shared.get("processed_input", "")
        
    def exec(self, processed_input):
        return f"Processed: {processed_input}"
        
    def post(self, shared, prep_res, exec_res):
        shared["result"] = exec_res
        return "complete"

# Connect nodes
read_node = ReadInput()
process_node = ProcessData()

# Define transitions
read_node - "process" >> process_node

# Create flow
flow = Flow(start=read_node)

# Run the flow
shared = {"input": "hello world"}
flow.run(shared)

print(shared["result"])  # Outputs: "Processed: HELLO WORLD"
``` 