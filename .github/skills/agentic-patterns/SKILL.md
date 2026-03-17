---
name: agentic-patterns
description: "Applies agentic design patterns from two authoritative sources — Gulli's 21-pattern framework (evoiz/Agentic-Design-Patterns) and Arsanjani/Bustos's architectural pattern library (PacktPublishing/Agentic-Architectural-Patterns-for-Building-Multi-Agent-Systems, 2026) — to help design, evaluate, or improve AI agent systems. Gulli covers: Prompt Chaining, Routing, Parallelization, Reflection, Tool Use, Planning, Multi-Agent, Memory Management, Learning, MCP, Goal Setting, Exception Handling, Human-in-the-Loop, RAG, A2A, Resource-Aware, Reasoning, Guardrails, Evaluation, Prioritization, Exploration. Arsanjani/Bustos adds: Agentic Stack (3 layers), GenAI Maturity Model, Hierarchical Orchestrator, Agent Router, Blackboard, Instruction Fidelity Auditing, Decision Audit Trail, Parallel Execution Consensus, Circuit Breaker, Secure Agent, Agent Calls Human, Human Delegates to Agent, Collaborative Co-piloting, Single Agent Baseline, ReAct Agent, Memory-Augmented Agent, Tool and Agent Registry, Lifecycle Callbacks / AgentOps, Self-Improvement Flywheel, R⁵ Model. Use when: selecting patterns for a new agent system, evaluating an existing architecture, combining patterns, explaining what a pattern does, designing an agent chain, assessing enterprise maturity, or adding observability. Triggers on: 'design pattern', 'agentic pattern', 'agent architecture', 'which pattern', 'pattern for', 'orchestrator', 'hierarchical agent', 'circuit breaker', 'agent router', 'instruction fidelity', 'agentops', 'lifecycle callbacks', 'maturity model', 'R5 model', 'ReAct', 'agentic stack', 'A2A pattern', 'fault tolerance', 'explainability pattern', 'compliance pattern', 'reflection pattern', 'planning pattern', 'routing pattern', 'multi-agent', 'RAG pattern', 'HITL pattern', 'tool use pattern', 'guardrails pattern', 'memory pattern'. Do not use for: writing code that implements a pattern, creating agent files (use writing-agents skill), or creating prompt files (use writing-prompts skill)."
metadata:
  version: "1.0.0"
  author: "Paul Slits"
---

# Agentic Patterns

Select, combine, and apply patterns from the *Agentic Design Patterns* framework (Gulli, 2024) to design or improve AI agent systems.

## Reference

Consult [references/patterns-catalogue.md](references/patterns-catalogue.md) for the full catalogue of patterns from both sources:
- **Parts 1–4** — 21 patterns from Gulli (*Agentic Design Patterns*)
- **Part 5** — 20 architectural patterns from Arsanjani & Bustos (*Agentic Architectural Patterns for Building Multi-Agent Systems*, Packt 2026) — including the Agentic Stack, GenAI Maturity Model, Hierarchical Orchestrator, coordination, explainability, robustness, human-agent, agent-level, system-level, and adaptation patterns

## Procedure

### 1. Understand the System Being Designed

Read the user's description. Extract:
- The **goal** (what the system must accomplish)
- The **inputs** (what arrives and from whom)
- The **outputs** (what is produced and for whom)
- The **constraints** (latency, cost, safety, human oversight requirements)

If any of these are missing or ambiguous, ask before proceeding.

### 2. Identify Applicable Patterns

Using [references/patterns-catalogue.md](references/patterns-catalogue.md), match the system's needs to patterns. Check all four tiers:

- **Tier 1 – Core (Gulli):** Does the task have serial stages? Multiple input types? Independent sub-tasks? Need for self-correction? External tools? Long-horizon planning? Multiple expert roles?
- **Tier 2 – Advanced (Gulli):** Does the agent need persistent memory? Stale or insufficient knowledge base? Explicit goal tracking?
- **Tier 3 – Production (Gulli):** Could failures cascade? Are actions high-stakes or irreversible? Is domain knowledge external?
- **Tier 4 – Enterprise (Gulli):** Are multiple agents distributed across services? Must cost or latency be bounded? Is the system user-facing or regulated?
- **Tier 5 – Architectural (Arsanjani/Bustos):** Does the design need a maturity assessment? Does it require hierarchical orchestration, intent-based routing, or a shared-state blackboard? Must the system be explainable or auditable? Are there fault tolerance requirements beyond retry logic? Does the human-agent interaction need a formalised mode? Does the agent need an explicit internal architecture (ReAct, R⁵)? Is production observability (AgentOps, Lifecycle Callbacks) or capability governance (Tool Registry) required?

### 3. Select and Justify Patterns

For each recommended pattern:
1. State the **pattern name and tier**
2. Give a **one-sentence justification** referencing the system's specific requirement
3. Note any **key consideration** from the catalogue that applies
4. Flag **conflicts or tensions** between selected patterns (e.g., Parallelization vs. Resource-Aware Optimization)

Limit selection to the minimum set required. Do not recommend patterns that have no specific justification.

### 4. Design the Composition

If multiple patterns are selected, design how they combine:
- Define the **entry point** (which pattern handles the first interaction)
- Map **data flow** between patterns (what each passes to the next)
- Identify **gates** where human review or quality checks are inserted
- Note which patterns run in parallel vs. in sequence

Produce a simple numbered flow or Mermaid diagram if the composition has more than 3 patterns.

### 5. Identify Risks and Mitigations

For each selected pattern, call out its primary risk (from the catalogue's "Key consideration") and recommend a concrete mitigation in the context of this system.

### 6. Recommend Next Steps

Based on the design, recommend which VS Code artefact to build next:
- Prototype the agent chain → use `@writing-agents`
- Create a reusable prompt for a specific step → use `@writing-prompts`
- Codify this pattern knowledge → use `@writing-skills`
- Implement code → use the default coding agent

## Output Format

Present findings in this structure:

### System Summary
One paragraph restating the system's goal, inputs, outputs, and constraints as understood.

### Recommended Patterns

| # | Pattern | Tier | Justification |
|---|---------|------|---------------|
| 1 | Name | Core / Advanced / Production / Enterprise | Why this system needs it |

### Composition Design
Numbered flow or Mermaid diagram showing how patterns chain together.

### Risks and Mitigations

| Pattern | Risk | Mitigation |
|---------|------|------------|
| Name | Key consideration from catalogue | Concrete action for this system |

### Next Steps
Bulleted list of recommended artefacts or implementation actions.

## Rules

- Never recommend a pattern without a specific justification tied to the system's stated requirements.
- Always check all four tiers before concluding the selection is complete.
- When two patterns conflict, explain the trade-off rather than silently picking one.
- Do not invent patterns not in the catalogue; if the user's need is not covered, say so explicitly.
- Do not implement code. Design only.
