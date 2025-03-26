# MkDocs Implementation Plan

**Date**: March 29, 2025  
**Author**: Documentation Team  
**Status**: Draft  

## Overview

This document outlines the detailed implementation plan for setting up MkDocs as the documentation framework for the Hephaestus project. The plan includes installation, configuration, migration of existing documentation, and customization.

## Prerequisites

- Python 3.8+
- pip
- git

## Installation Steps

1. **Install MkDocs and Required Plugins**

```bash
# Create a virtual environment (optional but recommended)
python -m venv docs-env
source docs-env/bin/activate  # On Windows: docs-env\Scripts\activate

# Install MkDocs and Material theme
pip install mkdocs
pip install mkdocs-material

# Install additional plugins
pip install mkdocs-versioning-plugin
pip install mkdocs-minify-plugin
pip install mkdocs-git-revision-date-plugin
pip install mkdocstrings
pip install mkdocs-include-markdown-plugin
```

2. **Save Requirements to File**

```bash
pip freeze > docs/requirements-docs.txt
```

## Initial Setup

1. **Initialize MkDocs Project**

```bash
# Navigate to the project root
cd /path/to/hephaestus

# Initialize MkDocs (creates mkdocs.yml and docs directory)
mkdocs new .
```

2. **Create Basic Configuration**

Edit `mkdocs.yml` to include:

```yaml
site_name: Hephaestus Documentation
site_description: Documentation for the Hephaestus self-improving code generation system
site_author: Hephaestus Team
repo_url: https://github.com/organization/hephaestus

theme:
  name: material
  features:
    - navigation.tabs
    - navigation.sections
    - navigation.indexes
    - search.highlight
    - search.share
    - content.code.copy
  palette:
    - scheme: default
      primary: indigo
      accent: indigo
      toggle:
        icon: material/brightness-7
        name: Switch to dark mode
    - scheme: slate
      primary: indigo
      accent: indigo
      toggle:
        icon: material/brightness-4
        name: Switch to light mode

markdown_extensions:
  - admonition
  - attr_list
  - def_list
  - footnotes
  - meta
  - pymdownx.details
  - pymdownx.highlight
  - pymdownx.superfences
  - pymdownx.tabbed
  - pymdownx.tasklist
  - tables
  - toc:
      permalink: true

plugins:
  - search
  - git-revision-date
  - minify:
      minify_html: true
      minify_js: true
      minify_css: true
  - include-markdown
  - versioning:
      version_selection:
        - latest
        - 0.1.1
        - 0.1.0
        
extra:
  version:
    provider: mike
```

## Directory Structure

Create the following directory structure:

```
docs/
├── assets/
│   ├── images/
│   ├── css/
│   └── js/
├── guides/
│   ├── getting-started.md
│   ├── migration.md
│   └── consolidation.md
├── components/
│   ├── core/
│   │   ├── node.md
│   │   ├── flow.md
│   │   └── registry.md
│   ├── engine/
│   │   ├── forge-loop.md
│   │   ├── flow-builder.md
│   │   └── mutation-engine.md
│   └── scoring/
│       ├── scorer.md
│       ├── best-of-n.md
│       └── test-harness.md
├── proposals/
│   └── index.md
├── progress/
│   ├── phase1.md
│   ├── phase2.md
│   └── phase3.md
└── index.md
```

## Migration Strategy

1. **Copy Existing Documentation**

```bash
# Create necessary directories
mkdir -p docs/assets/images docs/guides docs/components/{core,engine,scoring} docs/proposals docs/progress

# Copy existing documentation (example commands)
cp docs/README.md docs/index.md
cp docs/guides/migration_guide.md docs/guides/migration.md
cp docs/guides/consolidation_status.md docs/guides/consolidation.md
cp docs/phase_progress.md docs/progress/index.md
cp docs/project_status.md docs/status.md
```

2. **Update Cross-References**

Update all internal links to use relative paths compatible with MkDocs:

- Example: Change `[Migration Guide](guides/migration_guide.md)` to `[Migration Guide](../guides/migration.md)`

3. **Create Navigation Structure**

Update `mkdocs.yml` to include:

```yaml
nav:
  - Home: index.md
  - Project Status: status.md
  - Guides:
    - Getting Started: guides/getting-started.md
    - Migration Guide: guides/migration.md
    - Consolidation Status: guides/consolidation.md
  - Components:
    - Core:
      - Overview: components/core/index.md
      - Node: components/core/node.md
      - Flow: components/core/flow.md
      - Registry: components/core/registry.md
    - Engine:
      - Overview: components/engine/index.md
      - Forge Loop: components/engine/forge-loop.md
      - Flow Builder: components/engine/flow-builder.md
      - Mutation Engine: components/engine/mutation-engine.md
    - Scoring:
      - Overview: components/scoring/index.md
      - Scorer: components/scoring/scorer.md
      - BestOfN Builder: components/scoring/best-of-n.md
      - Test Harness: components/scoring/test-harness.md
  - Progress:
    - Overview: progress/index.md
    - Phase 1: progress/phase1.md
    - Phase 2: progress/phase2.md
    - Phase 3: progress/phase3.md
  - Proposals:
    - Overview: proposals/index.md
```

## Customization

1. **Add Custom Styling**

Create `docs/assets/css/custom.css`:

```css
:root {
  --md-primary-fg-color: #3949ab;
  --md-primary-fg-color--light: #757de8;
  --md-primary-fg-color--dark: #002984;
  --md-accent-fg-color: #757de8;
}

.md-header__title {
  font-weight: bold;
}
```

Update `mkdocs.yml` to include custom CSS:

```yaml
extra_css:
  - assets/css/custom.css
```

2. **Add Project Logo**

```yaml
theme:
  logo: assets/images/logo.png
  favicon: assets/images/favicon.ico
```

## Building and Testing

1. **Local Development**

```bash
# Start local development server
mkdocs serve

# Access at http://127.0.0.1:8000/
```

2. **Building the Documentation**

```bash
# Build the documentation
mkdocs build

# Output will be in the 'site' directory
```

## Deployment

1. **GitHub Pages Setup**

```bash
# Deploy to GitHub Pages
mkdocs gh-deploy
```

2. **Version Management**

```bash
# Install mike for versioning
pip install mike

# Deploy versions
mike deploy 0.1.0
mike deploy 0.1.1
mike deploy latest

# Set latest as default
mike set-default latest
```

## Timeline

| Task | Estimated Time | Target Completion |
|------|----------------|-------------------|
| Installation and initial setup | 1 day | April 2, 2025 |
| Directory structure creation | 1 day | April 3, 2025 |
| Migration of existing documentation | 2 days | April 5, 2025 |
| Navigation and cross-reference updates | 2 days | April 7, 2025 |
| Theme customization | 1 day | April 8, 2025 |
| Testing and refinement | 2 days | April 10, 2025 |
| Initial deployment | 1 day | April 11, 2025 |

## Next Steps

After initial implementation:

1. Create documentation templates for different document types
2. Implement API documentation generation
3. Add versioning support
4. Develop contribution guidelines for documentation
5. Train team members on using and contributing to the documentation

## References

- [MkDocs Official Documentation](https://www.mkdocs.org/)
- [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)
- [MkDocs Versioning Plugin](https://github.com/zayd62/mkdocs-versioning-plugin)
- [mike - Versioning Tool](https://github.com/jimporter/mike) 