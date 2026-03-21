# ADR-0001: Level 5 Autonomous Maturity — Add Aspirational Placeholder to Adoption Roadmap

Date: 2026-03-20
Status: Accepted
HITL Issue: [#9](https://github.com/pslits/copilot-session-feedback/issues/9)
Decider: @pslits
Risk Tier: low

---

## Context

The adoption roadmap in [adoption-roadmap.instructions.md](../../.github/instructions/adoption-roadmap.instructions.md)
covers Levels 2–4 of the GenAI Maturity Model. The book's Ch. 1 defines Level 5 as "Autonomous:
self-improving, self-healing systems with minimal human oversight." The framework's Self-Improvement
Flywheel is the mechanism that could eventually reach Level 5 — where hook scripts auto-detect
recurring patterns and propose new rules without manual initiation.

Currently, there is no reference to Level 5 anywhere in the framework. This creates a blind spot:
a developer following the roadmap has no signal that the flywheel could be automated further, and no
documented criteria for when to consider that step.

The risk of adding a placeholder is minimal — it is a documentation-only change with no code or
behaviour impact.

---

## Decision

> **We decide to add a Level 5 "Aspirational" phase entry to the adoption roadmap describing the
> conditions under which automated pattern detection could replace manual session analysis.**

The entry should be clearly marked as aspirational/out-of-scope for the current VS Code-native
constraint, while describing the capability threshold that would justify exploring it.

---

## Consequences

### Positive
- The roadmap is complete against the book's five-level maturity model.
- Developers have a clear horizon to plan toward, rather than an abrupt "Ongoing" endpoint.
- Prevents premature automation by naming the preconditions explicitly.

### Negative / Risks
- None anticipated. Documentation-only change.

### Neutral
- The Level 5 placeholder may surface questions about tool/plugin requirements outside VS Code.

---

## Follow-up Actions

| Action | Owner | Due Date | Status |
|---|---|---|---|
| Add Level 5 entry to adoption-roadmap.instructions.md | @pslits | 2026-04-03 | Done |
| Reference ADR-0001 in the roadmap file | @pslits | 2026-04-03 | Done |

---

## Outcome (complete after execution)

Added an aspirational Level 5 — Autonomous row to the Adoption Phases table in
`adoption-roadmap.instructions.md`, clearly marked as out of scope for the current
VS Code-native constraint. A friction checkpoint for the Ongoing → Level 5 transition
was added to the Friction Checkpoints table. A reference to this ADR was added at the
end of the Planning Rules section.
