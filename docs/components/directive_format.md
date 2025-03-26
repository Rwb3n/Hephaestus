---
title: Directive Format
description: Specification for the structured format used to instruct Hephaestus
---

# Directive Format

## Overview

The Directive Format is the standardized specification for communicating intent and requirements to Hephaestus. Directives serve as the primary interface for users to express what they want the system to accomplish, providing clear, structured instructions that can be parsed and executed by the various components.

By adhering to a consistent format, directives ensure that user requirements are correctly interpreted and implemented throughout the Hephaestus pipeline.

## Format Specification

### Basic Structure

Directives follow a YAML-based structure with specific sections:

```yaml
directive:
  type: [directive_type]
  name: [unique_identifier]
  description: [human-readable_description]
  
  # Specific directive content follows based on type
  content:
    # Type-specific fields
    
  constraints:
    # Optional constraints on implementation
    
  metadata:
    # Optional additional information
```

### Directive Types

Hephaestus supports several directive types:

1. **`feature`**: Request to add new functionality
2. **`fix`**: Request to correct a bug or issue
3. **`refactor`**: Request to improve existing code without changing functionality
4. **`optimize`**: Request to improve performance
5. **`test`**: Request to add or improve tests

### Type-Specific Content

Each directive type has specific content fields:

#### Feature Directive

```yaml
directive:
  type: feature
  name: "add-user-authentication"
  description: "Implement user authentication using JWT"
  
  content:
    requirements:
      - "Users should be able to register with email and password"
      - "System should issue JWT tokens upon successful login"
      - "Protected routes should verify token validity"
    
    acceptance_criteria:
      - "Registration endpoint returns 201 on success"
      - "Login endpoint returns valid JWT token"
      - "Protected routes return 401 for invalid tokens"
    
    interfaces:
      - name: "register"
        input: "email, password"
        output: "user_id, status"
      
      - name: "login"
        input: "email, password"
        output: "token, expiry"
  
  constraints:
    language: "python"
    libraries: ["flask", "pyjwt"]
    max_complexity: "medium"
```

#### Fix Directive

```yaml
directive:
  type: fix
  name: "fix-login-timeout"
  description: "Fix timeout issue in login process"
  
  content:
    issue_description: "Login requests timeout after 5 seconds during peak usage"
    observed_behavior: "Users receive 504 Gateway Timeout errors"
    expected_behavior: "Login should complete within 10 seconds even under load"
    reproduction_steps:
      - "Send 100 concurrent login requests"
      - "Observe timeouts in server logs"
    
    affected_components:
      - "auth_service.py"
      - "db_connector.py"
  
  constraints:
    maintain_compatibility: true
    max_response_time: "10s"
```

#### Refactor Directive

```yaml
directive:
  type: refactor
  name: "refactor-data-access"
  description: "Refactor data access layer to use repository pattern"
  
  content:
    motivation: "Current direct database access is scattered across codebase"
    target_components:
      - "user_service.py"
      - "order_service.py"
    
    design_pattern: "repository"
    expected_benefits:
      - "Improved testability"
      - "Better separation of concerns"
      - "Reduced duplication"
  
  constraints:
    maintain_functionality: true
    test_coverage: "90%"
```

## Constraints

Constraints define boundaries and requirements for the implementation:

| Constraint | Description | Example Values |
|------------|-------------|---------------|
| `language` | Programming language | `"python"`, `"javascript"` |
| `libraries` | Permitted libraries | `["react", "redux"]` |
| `max_complexity` | Complexity limit | `"low"`, `"medium"`, `"high"` |
| `test_coverage` | Required test coverage | `"80%"` |
| `performance` | Performance requirements | `"response_time < 200ms"` |
| `compatibility` | Compatibility requirements | `"browser: IE11+"` |
| `security` | Security requirements | `"input_validation: strict"` |

## Metadata

Metadata provides additional context:

```yaml
metadata:
  priority: "high"
  requestor: "product_team"
  deadline: "2023-12-31"
  related_directives: ["feature-user-roles"]
  tags: ["auth", "security"]
```

## Integration with Hephaestus

Directives are processed through the Hephaestus pipeline:

1. **Input Processing**: Directives are validated for correct format
2. **Goal Mapping**: The Goal Proposer maps directives to implementation goals
3. **Mutation Guidance**: The Mutation Engine uses directives to guide code generation
4. **Test Criteria**: The Test Harness uses directives to validate implementations
5. **Scoring Input**: The Scoring System uses directives to evaluate quality

## Usage Examples

### Command Line

```bash
hephaestus --directive path/to/directive.yaml
```

### Programmatic

```python
from hephaestus import Engine

engine = Engine()
with open('directive.yaml', 'r') as file:
    directive_content = file.read()
    
result = engine.process_directive(directive_content)
```

## Directive Validation

Hephaestus validates directives against a schema to ensure correctness:

```bash
hephaestus validate --directive path/to/directive.yaml
```

## Best Practices

When writing directives:

1. **Be specific** about requirements and expectations
2. **Include acceptance criteria** to clarify success conditions
3. **Specify constraints** to guide implementation boundaries
4. **Provide context** through detailed descriptions
5. **Use consistent terminology** across related directives
6. **Prioritize requirements** to focus implementation efforts
7. **Reference existing components** for integration points

## Common Errors

| Error | Description | Resolution |
|-------|-------------|------------|
| `Invalid directive type` | Unrecognized directive type | Use one of the supported types |
| `Missing required field` | Required field not provided | Add the missing field |
| `Constraint violation` | Implementation constraint issue | Adjust constraints or implementation |
| `Conflicting requirements` | Requirements conflict | Resolve the conflict in requirements |

## Future Enhancements

Planned enhancements to the Directive Format include:

1. **Visual Directive Builder**: GUI for creating directives
2. **Directive Templates**: Pre-configured templates for common tasks
3. **Natural Language Processing**: Generating directives from natural language
4. **Directive Versioning**: Tracking changes to directives over time
5. **Cross-Directive Dependencies**: Explicitly modeling dependencies 