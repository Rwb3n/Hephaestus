# Hephaestus: Roadmap

**Note: This roadmap is now maintained in the comprehensive [Project Status Document](project_status.md) which includes detailed implementation plans, timeline estimates, and integration with the consolidation phases. Please refer to that document for the most current and detailed roadmap.**

## v0.1.1 Goals (Core Improvements)
- [x] Implement LLM service integration
  - [x] Create a base LLM service class with common interface
  - [x] Add OpenAI API integration
  - [ ] Add Anthropic API integration
  - [x] Implement prompt templates for different tasks
- [x] Add basic test suite
  - [x] Unit tests for core components
  - [ ] Integration tests for full pipeline
- [ ] Improve FlowBuilder functionality
  - [x] Add LLM integration
  - [ ] Add file saving capabilities
  - [ ] Implement file location management
  - [ ] Add imports extraction and management

## v0.2.0 Goals (Enhanced Capabilities)
- [ ] Build specialized Node types
  - [ ] API call nodes
  - [ ] File handling nodes
  - [ ] Natural language processing nodes
- [ ] Implement Registry visualization
  - [ ] Add lineage graph generation
  - [ ] Create simple web dashboard
  - [ ] Add build comparison tools
- [ ] Add intelligent code splitting for large files
  - [ ] Implement file decomposition
  - [ ] Add cross-file reference tracking
  - [ ] Create mechanisms to stitch components together

## v0.3.0 Goals (Advanced Features)
- [ ] Formalize `Custodian` for stagnation detection and directive arbitration
- [ ] Implement `Visualizer` module for lineage mapping (Mermaid or SVG)
- [ ] Build `Memory` agent on top of FAISS (schema: directive → node → score vector)
- [ ] Launch `emergency_stop.flag` polling in `forge_loop.py`
- [ ] Add LLM-powered code review and improvement

## v0.4.0 Goals (Production Readiness)
- [ ] Sandbox execution with timeout and subprocess guards
- [ ] Integrate human-in-the-loop override path
- [ ] Allow directive queueing and scheduling with entropy weighting
- [ ] Implement distributed execution mode
- [ ] Add comprehensive documentation generation
- [ ] Create benchmarking and performance tracking

## Long-term Vision
- [ ] Self-improvement of the core Hephaestus engine itself
- [ ] Multi-agent cooperative code generation
- [ ] Dynamic adaptation to programming paradigms and languages
- [ ] Human preference learning from feedback
- [ ] Specialized domain expertise development
