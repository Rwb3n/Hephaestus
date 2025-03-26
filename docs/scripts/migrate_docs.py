#!/usr/bin/env python
"""
Documentation Migration Script for Hephaestus

This script helps with migrating existing documentation files to the new
MkDocs structure by copying files to their appropriate locations and
updating internal links.
"""

import os
import re
import shutil
from pathlib import Path

# Base paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
DOCS_DIR = PROJECT_ROOT / "docs"
SCRIPTS_DIR = DOCS_DIR / "scripts"
TEMPLATES_DIR = DOCS_DIR / "templates"

# Target structure paths
ASSETS_DIR = DOCS_DIR / "assets"
IMAGES_DIR = ASSETS_DIR / "images"
GUIDES_DIR = DOCS_DIR / "guides"
COMPONENTS_DIR = DOCS_DIR / "components"
CORE_COMPONENTS_DIR = COMPONENTS_DIR / "core"
ENGINE_COMPONENTS_DIR = COMPONENTS_DIR / "engine"
SCORING_COMPONENTS_DIR = COMPONENTS_DIR / "scoring"
PROPOSALS_DIR = DOCS_DIR / "proposals"
CONCEPTS_DIR = DOCS_DIR / "concepts"
REFERENCE_DIR = DOCS_DIR / "reference"
STATUS_DIR = DOCS_DIR / "status"

# Mapping of old locations to new locations
FILE_MAPPING = {
    # Core docs
    "project_status.md": ("status/project_status.md", True),
    "roadmap.md": ("status/roadmap.md", True),
    "CHANGELOG.md": ("status/changelog.md", True),
    "phase_progress.md": ("status/phase_progress.md", True),
    "test_debug_protocol.md": ("guides/test_debug_protocol.md", True),
    "architecture.md": ("concepts/architecture.md", True),
    
    # Guides
    "guides/migration_guide.md": ("guides/migration_guide.md", True),
    "guides/consolidation_status.md": ("guides/consolidation_status.md", True),
    "guides/documentation_progress.md": ("guides/documentation_progress.md", True),
    
    # Proposals
    "proposals/consolidation_proposal.md": ("proposals/consolidation_proposal.md", True),
    "proposals/testing_framework_proposal.md": ("proposals/testing_framework_proposal.md", True),
    "proposals/20250329_documentation_enhancement.md": ("proposals/20250329_documentation_enhancement.md", True),
}

# Pattern to find markdown links
LINK_PATTERN = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')


def migrate_file(source_path, target_path, update_links=False):
    """
    Migrate a file from source_path to target_path, optionally updating links.
    
    Args:
        source_path: The source file path
        target_path: The destination file path
        update_links: Whether to update internal links
    """
    source_full = DOCS_DIR / source_path
    target_full = DOCS_DIR / target_path
    
    if not source_full.exists():
        print(f"Warning: Source file not found: {source_full}")
        return False
    
    # Create target directory if it doesn't exist
    target_full.parent.mkdir(parents=True, exist_ok=True)
    
    if update_links:
        # Read content and update links
        with open(source_full, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Function to update links
        def update_link(match):
            link_text = match.group(1)
            link_target = match.group(2)
            
            # Don't update external links or anchors
            if link_target.startswith('http') or link_target.startswith('#'):
                return match.group(0)
                
            # Try to find the new path
            if link_target in FILE_MAPPING:
                new_target, _ = FILE_MAPPING[link_target]
                # Calculate relative path
                rel_path = os.path.relpath(
                    str(DOCS_DIR / new_target), 
                    str(target_full.parent)
                )
                # Normalize path separators for URLs
                rel_path = rel_path.replace('\\', '/')
                return f'[{link_text}]({rel_path})'
                
            return match.group(0)
            
        updated_content = LINK_PATTERN.sub(update_link, content)
        
        # Write updated content
        with open(target_full, 'w', encoding='utf-8') as f:
            f.write(updated_content)
            
        print(f"Migrated and updated links: {source_path} -> {target_path}")
    else:
        # Simple copy
        shutil.copy2(source_full, target_full)
        print(f"Migrated: {source_path} -> {target_path}")
        
    return True


def create_index_files():
    """Create basic index.md files for component directories."""
    directories = [
        (COMPONENTS_DIR, "Components"),
        (CORE_COMPONENTS_DIR, "Core Components"),
        (ENGINE_COMPONENTS_DIR, "Engine Components"),
        (SCORING_COMPONENTS_DIR, "Scoring Components"),
        (PROPOSALS_DIR, "Proposals"),
        (CONCEPTS_DIR, "Concepts"),
        (REFERENCE_DIR, "Reference"),
        (STATUS_DIR, "Project Status")
    ]
    
    for directory, title in directories:
        index_path = directory / "index.md"
        if not index_path.exists():
            with open(index_path, 'w', encoding='utf-8') as f:
                f.write(f"# {title}\n\n")
                f.write(f"This section contains documentation for the {title.lower()} of the Hephaestus project.\n\n")
                
                # For component directories, add a list of expected components
                if directory == CORE_COMPONENTS_DIR:
                    f.write("## Core Components\n\n")
                    f.write("- [Node](node.md)\n")
                    f.write("- [Flow](flow.md)\n")
                    f.write("- [Registry](registry.md)\n")
                elif directory == ENGINE_COMPONENTS_DIR:
                    f.write("## Engine Components\n\n")
                    f.write("- [Flow Builder](flow_builder.md)\n")
                    f.write("- [Mutation Engine](mutation_engine.md)\n")
                    f.write("- [Forge Loop](forge_loop.md)\n")
                elif directory == SCORING_COMPONENTS_DIR:
                    f.write("## Scoring Components\n\n")
                    f.write("- [Scorer](scorer.md)\n")
                    f.write("- [Best of N Builder](best_of_n.md)\n")
                    f.write("- [Test Harness](test_harness.md)\n")
                elif directory == PROPOSALS_DIR:
                    f.write("## Current Proposals\n\n")
                    f.write("- [Consolidation Proposal](consolidation_proposal.md)\n")
                    f.write("- [Testing Framework Proposal](testing_framework_proposal.md)\n")
                    f.write("- [Documentation Enhancement](20250329_documentation_enhancement.md)\n")
                
            print(f"Created index file: {index_path}")


def main():
    """Main function to migrate documentation files."""
    print("Starting documentation migration...")
    
    # Migrate files
    success_count = 0
    failure_count = 0
    
    for source_path, (target_path, update_links) in FILE_MAPPING.items():
        if migrate_file(source_path, target_path, update_links):
            success_count += 1
        else:
            failure_count += 1
    
    # Create index files
    create_index_files()
    
    print(f"\nMigration completed!")
    print(f"Successfully migrated: {success_count} files")
    print(f"Failed to migrate: {failure_count} files")
    print(f"\nNext steps:")
    print(f"1. Review migrated files")
    print(f"2. Update mkdocs.yml navigation to include new files")
    print(f"3. Check for any broken links")
    print(f"4. Run 'mkdocs serve' to preview the documentation")


if __name__ == "__main__":
    main() 