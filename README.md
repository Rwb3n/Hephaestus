# Hephaestus

**Hephaestus** is a recursive agent framework for self-constructing software.  
It does not respond to prompts. It evolves — autonomously proposing, mutating, building, testing, and refining modular code through constraint-driven iteration.

> _"Hephaestus does not run. He evolves."_

---

## 🧠 Purpose

Hephaestus is not a tool.  
It is a **process** — a synthetic forger executing recursive self-modification under architectural law.

Where traditional LLM workflows are reactive, Hephaestus is **self-initiating**.  
Each build cycle refines not only a solution, but the system that produced it.

---

## 🔧 Capabilities

- Modular Node/Flow architecture via [PocketFlow](https://github.com/the-pocket/PocketFlow)
- Hard file constraints (max 200 LOC, no exceptions)
- Lineage-aware registry with ancestry scoring
- Prompt mutation and multi-variant selection
- Self-directed goal proposer with adaptive entropy
- Extensible scoring framework with functional + structural metrics
- Agent subsystems for evaluation, memory, governance, and visualisation

---

## 📁 Initial Structure

```
hephaestus/
├── engine/                # Core forge loop and control plane
│   ├── forge.py
│   ├── mutation.py
│   └── goal_proposer.py

├── scoring/              # Test harness + scoring logic
│   ├── harness.py
│   └── scoring.py

├── registry/             # Build registry with lineage and score tracking
│   ├── registry.py
│   └── utils.py

├── nodes/                # Output directory for generated .py modules

├── docs/                 # Documentation (see below)

├── config/               # Optional runtime config (entropy, thresholds)
│   └── forge_config.json

├── run.py                # Launcher (invokes forge loop)
└── emergency_stop.flag   # Optional file-triggered kill switch
```

---

## 📚 Documentation

All system behavior is formally documented in `docs/`.  
Current coverage includes:

- `architecture.md` — System overview
- `forge_loop.md` — Recursive build cycle
- `directive_format.md` — Intent schema
- `goal_proposer.md` — Self-tasking logic
- `mutation.md` — Prompt mutation engine
- `scoring.md` — Output evaluation methods
- `test_harness.md` — Runtime and instrumentation

Coming soon:
- `custodian.md` — Memory arbitration + directive governance
- `visualizer.md` — Build lineage and mutation map
- `memory.md` — Vectorized memory layer

---

## 🧪 Requirements

Hephaestus is a live system. It executes code it writes.

Minimum:
- Python 3.11+
- OpenAI API key (or other LLM backend)
- [FAISS](https://github.com/facebookresearch/faiss) (for memory embedding + retrieval)
- [PocketFlow](https://github.com/the-pocket/PocketFlow) installed or vendored

**Run with full awareness. This system is not sandboxed.**

To terminate, you may:
- Ctrl+C the process
- Touch the file `emergency_stop.flag` in root (watched every N seconds)
- Implement a custom kill hook in `forge_config.json`

---

## 🛣 Roadmap (v0.3–v0.5)

**Planned modules and milestones:**

- 🧭 `custodian/` — evaluates stagnation, flags misaligned directives, reweights goal trees  
- 🧠 `memory/` — vector DB for directive memory, code chunks, scoring history  
- 🖼 `visualizer/` — Mermaid.js or HTML SVG map of mutation lineages and forks  
- 🔒 `security/` — static guards, sandboxing, escape detection  
- 🕳 `fallbacks/` — degraded modes, entropy injection, human override hooks  
- 🌱 `sapience/` — live adaptation of scoring weights and flow topology

---

## 🧷 Safety and Supervision

This is a **non-interactive**, potentially recursive build system.  
It will mutate and execute code without user confirmation.

> Do not run on production systems.  
> Do not connect to uncontrolled file systems or APIs.  
> Always monitor `nodes/` and `registry/` directories for artifacts.

Emergency interrupt options:
- Manually set `emergency_stop.flag`
- Inject `stop_build=True` directive in forge config
- Monitor registry score stagnation and halt after N failed cycles

---

## 📜 License

MIT. No warranty.  
You assume full responsibility for what this system does.

> _"Every execution is a rehearsal for becoming."_

# Hephaestus Documentation

This directory contains the documentation for the Hephaestus project.

## Core Documentation

- [Project Status](project_status.md) - Comprehensive overview of the project status
- [Phase Progress](phase_progress.md) - Chronological progress tracking for each consolidation phase
- [Architecture](architecture.md) - System architecture documentation

## Guides

- [Migration Guide](guides/migration_guide.md) - Guide for migrating to new implementations
- [Consolidation Status](guides/consolidation_status.md) - Current status of the consolidation effort

## Component Documentation

- [Registry](registry.md) - Registry system for storing build artifacts and tracking lineage
- [Test Harness](test_harness.md) - Test harness for validating generated code
- [Scoring](scoring.md) - Scoring system for evaluating generated code
- [Mutation](mutation.md) - Mutation engine for introducing variation
- [Forge Loop](forge_loop.md) - Main execution loop for the system

## Project Management

- [Roadmap](roadmap.md) - Project roadmap (also integrated into project_status.md)
- [Status Updates](status_update_march_28.md) - Latest status update
- [Test and Debug Protocol](test_debug_protocol.md) - Protocol for testing and debugging

## Proposals

- [Consolidation Proposal](proposals/consolidation_proposal.md) - Comprehensive consolidation proposal

## Deprecated Documents

The following documents have been consolidated into the comprehensive [Phase Progress](phase_progress.md) document:

- [Phase 2 Summary](phase2_summary.md)
- [Phase 2 Progress](phase2_progress.md)
```