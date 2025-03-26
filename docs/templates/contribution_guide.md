# Documentation Contribution Guide

**Version**: 0.1.0  
**Last Updated**: YYYY-MM-DD  

## Overview

This guide outlines the process and standards for contributing to the Hephaestus project documentation. Following these guidelines ensures that our documentation remains consistent, high-quality, and useful to all users.

## Getting Started

### Setting Up Your Environment

1. Clone the repository:
   ```bash
   git clone https://github.com/your-org/hephaestus.git
   cd hephaestus
   ```

2. Install MkDocs and required plugins:
   ```bash
   pip install -r docs/requirements.txt
   ```

3. Preview the documentation locally:
   ```bash
   mkdocs serve
   ```
   This will start a local server at `http://127.0.0.1:8000/`.

## Documentation Structure

Our documentation is organized into the following categories:

- **Guides**: Step-by-step instructions for specific tasks
- **Concepts**: Explanations of core ideas and architecture
- **Reference**: Detailed API and component documentation
- **Tutorials**: End-to-end examples for learning
- **FAQs**: Frequently asked questions
- **Proposals**: Design and feature proposals

Each section has its own directory within the `docs/` folder.

## Creating New Documentation

### Using Templates

We provide templates for common documentation types. Copy the appropriate template as a starting point:

- [Component Template](../templates/component_template.md) - For documenting system components
- [Guide Template](../templates/guide_template.md) - For step-by-step instructions
- [FAQ Template](../templates/faq_template.md) - For frequently asked questions
- [Proposal Template](../templates/proposal_template.md) - For new proposals

### Naming Conventions

- **Filenames**: Use lowercase with underscores (e.g., `component_name.md`)
- **Proposals**: Use date-based prefixes (e.g., `20250329_feature_proposal.md`)
- **Images**: Store in `docs/assets/images/` with descriptive names

### Adding to Navigation

To add your document to the site navigation, edit the `mkdocs.yml` file in the root directory. Add your page under the appropriate section:

```yaml
nav:
  - Home: index.md
  - Guides:
    - Getting Started: guides/getting_started.md
    - Your New Guide: guides/your_new_guide.md
```

## Writing Style Guide

### Voice and Tone

- Use active voice rather than passive
- Write in present tense
- Be direct and concise
- Use second person ("you") when addressing the reader

### Formatting

- Use Markdown for all documentation
- Use ATX-style headers (`#`, `##`, `###`, etc.)
- Use code blocks with language specifiers for code examples
- Use lists for sequential steps or related items
- Use tables for structured data

### Code Examples

Code examples should:

- Be complete and runnable when possible
- Include comments to explain complex parts
- Use consistent indentation (4 spaces for Python)
- Follow the project's coding style guide

Example:
```python
# Import the component
from hephaestus import Component

# Initialize with configuration
component = Component(config={
    "parameter": "value"
})

# Process data
result = component.process()
```

### Images and Diagrams

- Use images sparingly and only when they add value
- Keep images under 1MB in size
- Provide alt text for accessibility
- Use diagrams for complex workflows or architectures

## Review Process

All documentation changes follow this process:

1. Create a branch for your changes
2. Make your documentation updates
3. Run `mkdocs build` to verify there are no errors
4. Submit a pull request
5. Address any feedback from reviewers
6. Once approved, your changes will be merged

## Best Practices

- Update related documents when making changes
- Check for broken links before submitting
- Keep examples up-to-date with the latest API
- Consider different expertise levels of readers
- Define technical terms on first use
- Use consistent terminology throughout

## Getting Help

If you have questions about contributing to documentation:

- Ask in the #documentation channel on Slack
- Post on the internal forums
- Contact the documentation team at docs@example.com

## References

- [MkDocs Documentation](https://www.mkdocs.org/)
- [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)
- [Markdown Guide](https://www.markdownguide.org/) 