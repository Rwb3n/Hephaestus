# Hephaestus Migration Guide

This guide provides instructions for migrating to the consolidated implementation of Hephaestus components. It addresses breaking changes, deprecated features, and recommended migration paths.

## BestOfNBuilder Migration

The `BestOfNBuilder` implementation has been consolidated to improve consistency and maintainability. The original implementation in `engine/best_of_n.py` is now deprecated, and a new implementation in `scoring/best_of_n.py` should be used.

### Import Changes

#### Before:
```python
from engine.best_of_n import BestOfNBuilder
```

#### After:
```python
from scoring.best_of_n import BestOfNBuilder
```

### Interface Changes

The new implementation follows the Node pattern more consistently:

#### Old Interface:
```python
builder = BestOfNBuilder(n=3)
inputs = builder.prep(shared)
candidates = builder.exec(inputs)
builder.post(shared, inputs, candidates)
```

#### New Interface:
```python
builder = BestOfNBuilder(
    n=3,
    mutation_engine=mutation_engine,  # Optional
    flow_builder=flow_builder,        # Optional 
    test_harness=test_harness         # Optional
)
action = builder.run(shared)  # Calls prep->exec->post internally
```

### Compatibility Layer

A compatibility layer is provided to ease the transition:

```python
# This will still work but will show a deprecation warning
from engine import BestOfNBuilder
```

## FlowBuilderNode Migration

The `FlowBuilderNode` implementation has been enhanced to integrate with the LLM service. The original implementation in `engine/flow_builder_node.py` is now deprecated, and the enhanced implementation in `engine/flow_builder.py` should be used.

### Import Changes

#### Before:
```python
from engine.flow_builder_node import FlowBuilderNode
```

#### After:
```python
from engine.flow_builder import FlowBuilderNode
```

### Interface Changes

The enhanced implementation provides additional capabilities:

#### New Features:
- Integration with the LLM service
- Template-based prompt generation
- Enhanced error handling and retries
- Support for saving generated code to disk

#### Example Usage:
```python
from engine.flow_builder import FlowBuilderNode
from services import OpenAIService

# Create the FlowBuilderNode with an LLM service
flow_builder = FlowBuilderNode(
    llm_service=OpenAIService()
)

# Run the flow builder
shared = {
    "build_task": "Create a data validation node",
    "directive": {"constraints": ["Handle null values"]},
    "save_path": "nodes/data_validator.py"  # Optional
}
action = flow_builder.run(shared)
```

## Deprecation Timeline

The following deprecation timeline has been established:

1. **Phase 1 (Current):** Deprecation warnings are displayed when using deprecated components.

2. **Phase 2 (2 weeks from now):** Additional log errors will be emitted, but the code will still function.

3. **Phase 3 (1 month from now):** Deprecated components will be removed from the codebase.

## Recommended Migration Steps

1. **Update Imports:** Replace imports to use the consolidated implementations.

2. **Update Code:** Use the new interfaces as described above.

3. **Run Tests:** Verify that your code works with the new implementations.

4. **Remove Warnings:** After successful migration, you can filter the deprecation warnings:

   ```python
   import warnings
   warnings.filterwarnings("ignore", category=DeprecationWarning)
   ```

## Getting Help

If you encounter issues during migration, please:

1. Check the updated documentation in the `docs/` directory.
2. Run the test scripts in `tests/` to verify your implementation.
3. Refer to the example implementations in `docs/examples/`.

## Reporting Issues

If you find bugs or issues with the consolidated implementation, please report them by opening an issue in the repository. 