---
description: Select and map the right agentic design patterns for a described system, drawing from both Gulli and Arsanjani/Bustos.
agent: planner
tools:
  - read/readFile
argument-hint: "system to design (e.g., autonomous document summarisation pipeline with human review)"
---

Select and compose agentic design patterns for the system described in the request.

Read [.github/skills/agentic-patterns/SKILL.md](../skills/agentic-patterns/SKILL.md) and [.github/skills/agentic-patterns/references/patterns-catalogue.md](../skills/agentic-patterns/references/patterns-catalogue.md) before proceeding. These are mandatory — do not answer from memory.

The catalogue covers two source books:
- **Gulli** — 21 patterns (Parts 1–4): Prompt Chaining, Routing, Parallelization, Reflection, Tool Use, Planning, Multi-Agent, Memory Management, Learning, MCP, Goal Setting, Exception Handling, HITL, RAG, A2A, Resource-Aware, Reasoning, Guardrails, Evaluation, Prioritization, Exploration
- **Arsanjani/Bustos** — 20 architectural patterns (Part 5): Agentic Stack, GenAI Maturity Model, Hierarchical Orchestrator, Agent Router, Blackboard, Instruction Fidelity Auditing, Decision Audit Trail, Parallel Execution Consensus, Circuit Breaker, Secure Agent, Agent Calls Human, Human Delegates to Agent, Collaborative Co-piloting, Single Agent Baseline, ReAct Agent, Memory-Augmented Agent, Tool and Agent Registry, Lifecycle Callbacks/AgentOps, Self-Improvement Flywheel, R⁵ Model

## Instructions

Follow the procedure in the skill file exactly for this system:

`${input:system description (goal, inputs, outputs, and any constraints)}`

1. Extract goal, inputs, outputs, and constraints from the description above.
2. Identify applicable patterns across **all five tiers** (Gulli Core, Gulli Advanced, Gulli Production, Gulli Enterprise, Arsanjani/Bustos Architectural) using the catalogue.
3. Select the minimum set of patterns needed — each must have a specific justification.
4. Design the composition: entry point, data flow, gates.
5. Identify risks and mitigations for each selected pattern.
6. Recommend next steps.

## Constraints

- Never recommend a pattern without a specific justification tied to the description above.
- Check all five tiers before finalising the selection (Gulli Core, Advanced, Production, Enterprise + Arsanjani/Bustos Architectural).
- When two patterns conflict, explain the trade-off.
- Do not invent patterns not in the catalogue.
- Do not write code or create agent files.

## Output Format

### System Summary
[One paragraph restating goal, inputs, outputs, constraints]

### Recommended Patterns
| # | Pattern | Tier | Justification |
|---|---------|------|---------------|
| 1 | | | |

### Composition Design
[Numbered flow or Mermaid diagram]

### Risks and Mitigations
| Pattern | Risk | Mitigation |
|---------|------|------------|
| | | |

### Next Steps
- To build the agent chain: use `@pattern-designer` for an interactive design session
- To scaffold agents from this design: use `@writing-agents`
- To create prompt files: use `@writing-prompts`
