# ADR-0005: Define Fallback Strategy for RPI Chain Agent Failure

Date: 2026-03-20
Status: Accepted
HITL Issue: [#13](https://github.com/pslits/copilot-session-feedback/issues/13)
Decider: @pslits
Risk Tier: medium

---

## Context

The book's Ch. 5 (Multi-Agent Coordination Patterns) emphasises that the Hierarchical Orchestrator
is a single point of failure, and that orchestrator resilience must be explicitly designed. The same
applies to pipeline topologies: if a mid-chain agent fails to produce the required handoff artefact,
the downstream agents have no input and the pipeline stalls silently.

The framework's design document acknowledges this in the Multi-Agent risk row ("context loss at
handoff") but the only mitigation listed is "keep agent scopes narrow." No concrete fallback is
defined for what happens when `@planner` fails to produce a phased plan, or when `@researcher`
produces no codebase findings.

The current situation means a developer gets no actionable guidance when the RPI chain breaks
mid-execution — they must debug ad hoc rather than following a documented recovery path.

---

## Decision

> **We decide to define and document a concrete fallback procedure for each RPI chain failure mode,
> and to add the fallback logic to both the design document and the individual agent files.**

Proposed fallbacks:
1. **`@researcher` produces no findings:** Fall back to manual lens analysis using
   the four-lenses instruction directly, skipping `@researcher`.
2. **`@planner` produces no phased plan:** Fall back to direct `/implement` execution using the
   researcher output as the specification, accepting reduced structure.
3. **`@implementer` stalls mid-plan:** Re-invoke `@implementer` with the partial plan and the
   step number to resume from.

Each fallback is a human-actioned recovery, not an automated one, consistent with the system's
HITL design.

---

## Consequences

### Positive
- Developers have a recovery path for each failure mode without ad-hoc debugging.
- Aligns the framework with Ch. 5's resilience recommendations.
- The fallback paths keep the pipeline useful even when individual agents underperform.

### Negative / Risks
- The documented fallbacks may encourage skipping agents ("I'll just fall back to manual").
  Mitigation: frame fallbacks as last resort, not workflow shortcuts.

### Neutral
- Fallback paths are manually actioned; no automation required.

---

## Follow-up Actions

| Action | Owner | Due Date | Status |
|---|---|---|---|
| Add fallback table to design document (Multi-Agent risks row) | @pslits | 2026-04-03 | Done |
| Add fallback recovery section to @researcher agent file | @pslits | 2026-04-03 | Done |
| Add fallback recovery section to @planner agent file | @pslits | 2026-04-03 | Done |
| Add fallback recovery section to @implementer agent file | @pslits | 2026-04-03 | Done |

---

## Outcome (complete after execution)

All four follow-up actions completed. A fallback table was added to the design document's
Risks and Mitigations section under a new "RPI Chain Fallback Procedures" subsection. Each of
the three RPI agent files (`researcher.agent.md`, `planner.agent.md`, `implementer.agent.md`)
now contains a "Fallback Recovery" section documenting the failure mode, symptom, and concrete
human-actioned recovery steps. Fallbacks are framed as last-resort procedures, consistent with
the HITL design and Ch. 5 resilience guidance.
