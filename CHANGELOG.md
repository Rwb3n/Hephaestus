# Changelog

All notable changes to Hephaestus will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive system consolidation proposal
- LLM service integration with OpenAI API
- Template system for prompt management using Jinja2
- Enhanced FlowBuilderNode with LLM integration
- Testing framework for LLM services and FlowBuilderNode
- Analysis document for BestOfNBuilder and FlowBuilderNode integration
- Consolidated BestOfNBuilder implementation in scoring/best_of_n.py
- Compatibility layers for deprecated implementations
- Import management hooks for tracking deprecated imports
- Core directory for foundational system components
- Test script for verifying imports after directory restructuring
- Comprehensive project status document with detailed roadmap
- Integration plan for consolidation phases with version roadmap
- Timeline for first full project test run (scheduled for April 15, 2025)
- Phase 3 Testing Framework Enhancement proposal with detailed implementation plan
- Reorganized scoring module with Scorer and TestHarness in dedicated submodules
- Consolidated phase progress documentation (phase_progress.md)
- Documentation Enhancement Proposal with comprehensive improvement plan
- Standardized documentation templates (component, guide, proposal, FAQ)
- MkDocs framework evaluation and implementation plan
- Documentation style guide with formatting standards
- Documentation contribution guidelines
- Implementation timeline for documentation enhancement initiative
- Documentation automation scripts for setup, migration, and component documentation generation
- Cross-platform helper scripts for running documentation tools
- Documentation scripts README with comprehensive usage instructions

### Changed
- Updated FlowBuilderNode to use the LLM service for code generation
- Improved code organization with services package
- Enhanced error handling and logging throughout the system
- Consolidated BestOfNBuilder implementations with backward compatibility
- Marked deprecated implementations with clear warnings
- Reorganized core infrastructure (Node, Flow, Registry) to core/ directory
- Added compatibility stubs with deprecation warnings for backward compatibility
- Enhanced roadmap with detailed implementation goals for each version
- Integrated existing roadmap.md with expanded project_status.md
- Moved TestHarness to scoring/test_harness/ module with backward compatibility
- Moved Scorer to scoring/scorer/ module with backward compatibility
- Consolidated phase2_summary.md and phase2_progress.md into phase_progress.md

### Fixed
- Integration between BestOfNBuilder and FlowBuilderNode
- Error handling in BestOfNBuilder for variant generation
- Import paths for core components

### Deprecated
- engine/best_of_n.py implementation (use scoring/best_of_n.py instead)
- Importing BestOfNBuilder from scoring.scoring module
- Imports from nodes.base_node and nodes.flow (use core.base_node and core.flow instead)
- Imports from registry.registry (use core.registry instead)
- Standalone roadmap.md (now integrated into project_status.md)

### Planned
- First full project test run (April 15, 2025)
- Completion of directory structure reorganization (April 1, 2025)
- Enhanced testing framework implementation (April 5-25, 2025)
- Documentation updates (May 1-15, 2025)
- Version 0.1.1 release (May 1, 2025)

## [0.1.0] - 2024-03-26

### Added
- Core Node/Flow infrastructure based on the PocketFlow pattern
- Registry system for storing build artifacts and tracking lineage
- TestHarness for validating generated code
- Scoring system with multiple evaluation criteria
- GoalProposer for generating build tasks
- MutationEngine for introducing variation into tasks
- FlowBuilder for code generation from task descriptions
- ForgeLoop for orchestrating the complete build cycle
- Main entry point (run.py) with CLI arguments
- Environment variable support via .env files
- Emergency stop mechanism
- Basic logging throughout the system
- Configuration system with CLI args and environment variables

### Changed
- Refactored existing components to follow the Node pattern

### Technical Debt
- Need to implement actual LLM service integration
- Need comprehensive test suite
- Need actual code saving functionality in FlowBuilder

## [Template for Future Entries]

## [x.y.z] - YYYY-MM-DD

### Added
- New feature A
- New feature B

### Changed
- Changed behavior of X
- Updated component Y

### Fixed
- Fixed bug in component Z
- Fixed issue with feature W

### Removed
- Deprecated feature V
- Removed unused code U

### Security
- Fixed security vulnerability in dependency D 