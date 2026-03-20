# ADR-0012: Document Registry Introduction Threshold

Date: 2026-03-20
Status: Proposed
HITL Issue: [#20](https://github.com/pslits/copilot-session-feedback/issues/20)
Decider: @pslits
Risk Tier: low

---

## Context

The book's Ch. 10 defines the Tool and Agent Registry pattern — a centralised catalogue of
available agents and tools with schemas, versioning, and health status. The framework correctly
excludes this as premature for a 3-agent, single-developer system. However, the catalogue entry
does not document when the registry should be introduced.

As the framework grows (more skills, more agents, team adoption), the absence of a documented
threshold means the registry will either:
(a) Never be introduced because no one knows when the trigger condition is met, or
(b) Introduced too early, adding governance overhead before there is complexity to govern.

Both outcomes are suboptimal. A simple size-based threshold prevents both failure modes.

---

## Decision

> **We decide to add an explicit introduction threshold to the Tool and Agent Registry catalogue
> entry: "Introduce when the system reaches 5+ active agents OR 10+ active skills, whichever
> comes first."**

This threshold is based on the book's Single Agent Baseline guidance: start simple, add
orchestration only when justified by observable complexity. 5 agents / 10 skills represents the
point at which discovery and governance overhead exceeds the cost of a registry.

---

## Consequences

### Positive
- The registry introduction decision is criteria-based rather than arbitrary.
- Prevents premature governance overhead.
- Provides an observable trigger for when to revisit this decision.

### Negative / Risks
- The threshold (5/10) is a heuristic, not a validated number. It should be treated as a
  starting point for a future ADR when the threshold is approached.

### Neutral
- The threshold docs remain dormant until the system hits 4 agents or 9 skills.

---

## Follow-up Actions

| Action | Owner | Due Date | Status |
|---|---|---|---|
| Add introduction threshold to Tool and Agent Registry entry | @pslits | 2026-04-03 | Open |

---

## Outcome (complete after execution)

_To be filled after the change is made._
