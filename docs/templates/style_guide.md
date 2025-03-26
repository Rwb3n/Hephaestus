# Documentation Style Guide

**Version**: 0.1.0  
**Last Updated**: YYYY-MM-DD  

## Overview

This style guide provides standards and best practices for writing documentation for the Hephaestus project. Following these guidelines ensures that our documentation remains consistent, clear, and professional across all areas of the project.

## General Principles

### Clarity First

- Write for clarity and understanding, not to impress.
- Use simple language and avoid unnecessary jargon.
- If a technical term is unavoidable, define it on first use.
- Break complex ideas into smaller, digestible chunks.

### Know Your Audience

- Consider the technical level of your intended readers.
- For general documentation, assume the reader is a developer with basic familiarity with Python.
- For advanced topics, clearly label them as such.
- For user guides, assume minimal technical knowledge.

### Be Consistent

- Use consistent terminology throughout the documentation.
- Follow the formatting guidelines in this document.
- Maintain the same level of detail across similar sections.

## Language and Grammar

### Voice and Tense

- Use active voice instead of passive voice.
  - Good: "The function returns a value."
  - Avoid: "A value is returned by the function."

- Use present tense in most cases.
  - Good: "The system displays an error message."
  - Avoid: "The system will display an error message."

- Use second person ("you") when addressing the reader.
  - Good: "You can configure the system using..."
  - Avoid: "One can configure the system using..."

### Capitalization

- Use sentence case for headings and titles.
  - Good: "How to install the package"
  - Avoid: "How To Install The Package"

- Capitalize proper nouns, including product names.
  - Example: "Hephaestus provides a flexible framework..."

- Follow standard capitalization for technical terms.
  - Example: "Python", "JavaScript", "API", "HTTP"

### Punctuation

- Use serial commas (Oxford commas).
  - Example: "The system supports Python, JavaScript, and Ruby."

- Use single spaces after periods.

- Use em dashes (—) without spaces for interruptions in thought.
  - Example: "The system—when properly configured—can process thousands of requests."

- Use code formatting for file paths, code elements, and commands.
  - Example: `config.yaml`, `hephaestus.utils.scoring`, `pip install`

## Formatting

### Markdown

All documentation should be written in Markdown, following these guidelines:

#### Headers

- Use ATX-style headers (with `#` symbols).
- Include a space after the `#` symbols.
- Maintain a hierarchical structure (don't skip levels).

```markdown
# Top-level header (h1)
## Second-level header (h2)
### Third-level header (h3)
```

#### Lists

- Use hyphens (`-`) for unordered lists.
- Use numbers for ordered lists.
- Indent nested lists with four spaces.
- Include a space after the list marker.

```markdown
- First item
- Second item
    - Nested item
    - Another nested item
- Third item

1. First step
2. Second step
3. Third step
```

#### Code

- Use backticks (`` ` ``) for inline code.
- Use triple backticks with a language identifier for code blocks.

```markdown
Use the `configure()` method to set up the component.

```python
from hephaestus import Component

component = Component()
component.configure(param="value")
```
```

#### Links

- Use descriptive link text that explains where the link leads.
- Use relative links for internal documentation.

```markdown
See the [installation guide](../guides/installation.md) for more details.
```

#### Images

- Include alt text for all images.
- Keep image file sizes reasonable (< 1MB).
- Use descriptive filenames for images.

```markdown
![Diagram of component architecture](../assets/images/component_architecture.png)
```

#### Tables

- Use tables for structured data.
- Include a header row.
- Align columns as needed for readability.

```markdown
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| name | string | Yes | The component name |
| config | object | No | Configuration options |
```

#### Admonitions

Use admonitions for callouts, warnings, and notes:

```markdown
!!! note
    This is an important note.

!!! warning
    This is a warning message.

!!! tip
    This is a helpful tip.
```

## Documentation Types

### API Reference

- Include all parameters, return values, and exceptions.
- Provide examples for common use cases.
- Document both successful and error scenarios.
- Use consistent terminology across the API.

### Guides

- Begin with a clear statement of what the guide covers.
- List prerequisites at the beginning.
- Break down complex procedures into numbered steps.
- Include expected outcomes for each major step.
- Conclude with next steps or related guides.

### Concepts

- Begin with a simple definition of the concept.
- Explain why the concept is important.
- Use analogies to relate complex ideas to familiar concepts.
- Include diagrams for visual explanation where appropriate.
- Reference related concepts.

### FAQ

- Use question-answer format.
- Group related questions together.
- Keep answers concise but complete.
- Include code examples where helpful.
- Link to more detailed documentation.

## Code Examples

### Best Practices

- Ensure code examples are correct and functional.
- Include comments to explain complex or non-obvious parts.
- Follow the project's coding style guide.
- Use realistic variable names and values.
- Demonstrate best practices, not just functional code.

### Python Examples

- Include imports at the beginning.
- Follow PEP 8 guidelines.
- Use 4 spaces for indentation.
- Include type hints where appropriate.
- Document inputs and outputs clearly.

```python
from hephaestus import Component
from typing import Dict, Any

def configure_component(name: str, options: Dict[str, Any]) -> Component:
    """
    Configure a component with the given options.
    
    Args:
        name: The component name
        options: Configuration options
        
    Returns:
        A configured component instance
    """
    component = Component(name)
    component.configure(options)
    return component
```

## Inclusive Language

- Use gender-neutral language.
  - Good: "The user can configure their settings."
  - Avoid: "The user can configure his settings."

- Avoid terminology that might be considered exclusionary.
  - Good: "Primary/secondary" or "main/replica"
  - Avoid: "Master/slave"

- Be mindful of cultural differences and avoid idioms that may not translate well.

## Review Checklist

Before submitting documentation, check the following:

- [ ] Content is technically accurate
- [ ] Content follows the style guidelines
- [ ] All links work correctly
- [ ] Code examples run without errors
- [ ] Images display correctly
- [ ] No spelling or grammatical errors
- [ ] No broken references or formatting
- [ ] Documentation builds without errors

## Resources

- [Google Developer Documentation Style Guide](https://developers.google.com/style)
- [Microsoft Writing Style Guide](https://docs.microsoft.com/en-us/style-guide/welcome/)
- [Markdown Guide](https://www.markdownguide.org/) 