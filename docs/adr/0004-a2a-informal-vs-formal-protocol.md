# ADR-0004: Document VS Code Handoffs as Informal A2A

Date: 2026-03-20
Status: Proposed
HITL Issue: [#12](https://github.com/pslits/copilot-session-feedback/issues/12)
Decider: @pslits
Risk Tier: low

---

## Context

The book's Ch. 4 and Ch. 5 treat Agent-to-Agent (A2A) communication as a formal protocol layer
with message envelopes (sender, receiver, intent, payload, trace ID). The framework's Gulli #15
(Inter-Agent Communication) is catalogued under Enterprise patterns and correctly excluded from
the current single-developer context.

However, the VS Code handoff mechanism used between `@researcher`, `@planner`, and `@implementer`
IS informal A2A — agents pass accumulated context forward without a formal envelope. The catalogue
currently does not acknowledge this distinction. A reader comparing the framework to the book's A2A
definition may conclude the framework has no A2A at all, missing the implicit informal A2A that the
RPI chain relies upon.

---

## Decision

> **We decide to add a clarifying note to the Agentic Stack catalogue entry and the A2A (Gulli #15)
> entry stating that VS Code agent handoffs constitute informal A2A — context forwarding without a
> formal protocol envelope — and documenting when a formal A2A layer would be warranted.**

The note will state: "The VS Code handoff mechanism is informal A2A: accumulated context is passed
forward at the UI layer without a structured message envelope. Formal A2A (with trace IDs, sender/
receiver fields, and idempotency) is warranted when agents operate across process boundaries or
network hops — not applicable in this single-process VS Code context."

---

## Consequences

### Positive
- The framework's relationship to Ch. 4/5 A2A definitions is explicit.
- Prevents confusion when comparing this framework to enterprise-grade A2A implementations.
- Documents the upgrade path to formal A2A if the system scales.

### Negative / Risks
- None. Documentation-only change.

### Neutral
- May prompt a future ADR when the framework is extended to multi-machine or team use.

---

## Follow-up Actions

| Action | Owner | Due Date | Status |
|---|---|---|---|
| Update Agentic Stack entry in patterns-catalogue.md | @pslits | 2026-04-03 | Open |
| Update A2A (Gulli #15) entry with informal A2A note | @pslits | 2026-04-03 | Open |

---

## Outcome (complete after execution)

_To be filled after the change is made._
