# Suppose we have a Node wrapper class or a Flow with 'FlowBuilderNode' inside.
builder = FlowBuilderNode()

# Mock shared data
shared = {
    "build_task": "Implement a Node that scrapes website titles and logs them",
    "directive": {
        "goal": "Expand system capability",
        "constraints": {
            "max_lines_per_file": 200,
            "immutable_core_modules": ["/heph/boot/"],
            "require_registry_logging": True
        },
        "reward_criteria": ["scope_increase", "reusability"]
    }
}

# Simulate run
inputs = builder.prep(shared)
code_output = builder.exec(inputs)
result = builder.post(shared, inputs, code_output)

print("Flow result action:", result)
print("Feedback:", shared["feedback"])


## Sample Output ##
```
2025-03-25 17:12:01 [INFO] [Build 1] PASSED line-limit test: heph/builds/build_1.py
Flow result action: default
Feedback: {
  'build_id': 1,
  'passed_line_test': True,
  'remarks': 'Build file is within line limit.'
}
```