# ADR-0006: Introduce "Instruction Drift" Terminology Across Framework

Date: 2026-03-20
Status: Accepted
HITL Issue: [#14](https://github.com/pslits/copilot-session-feedback/issues/14)
Decider: @pslits
Risk Tier: low

---

## Context

The book's Ch. 6 identifies "instruction drift" as the central explainability problem in agentic
systems: rules that were correct at time T become incorrect or misleading by time T+N as the
codebase, team, or tooling evolves. The `/audit` prompt exists precisely to detect and remediate
instruction drift — but neither the prompt nor the rule-writing instructions use this term.

Without the term, the system's explainability story is incomplete. A reviewer or auditor who has
read the book cannot map the `/audit` mechanism to the instruction drift problem it solves. The
rule-writing checklist asks "Is it still true?" but frames it as a general quality check, not as
drift detection.

Using the terminology also helps future contributors understand *why* the monthly audit cadence
exists: it is a scheduled drift-detection run, not general housekeeping.

---

## Decision

> **We decide to introduce the term "instruction drift" explicitly in rule-writing.instructions.md
> and in the /audit prompt description, naming the monthly cadence as a drift-detection cycle.**

The change is additive: existing content is preserved; the term and its definition from the book
(rules correct at T become incorrect by T+N due to codebase/team/tooling change) are inserted at
appropriate points.

---

## Consequences

### Positive
- Framework language aligns with Ch. 6 of the book.
- The purpose of the monthly audit is unambiguous.
- Future contributors recognise the concept immediately if they have read the book.

### Negative / Risks
- None. Documentation-only change.

### Neutral
- The term "instruction drift" may surface questions about automated drift detection — this is
  the aspirational Gap #13 and should be cross-referenced.

---

## Follow-up Actions

| Action | Owner | Due Date | Status |
|---|---|---|---|
| Add "instruction drift" definition to rule-writing.instructions.md | @pslits | 2026-04-03 | Done |
| Add "instruction drift" context to /audit prompt | @pslits | 2026-04-03 | Done |
| Cross-reference ADR-0006 in Instruction Fidelity Auditing catalogue entry | @pslits | 2026-04-03 | Open |

---

## Outcome (complete after execution)

The term "instruction drift" and its definition (rules correct at T become incorrect by T+N)
were inserted as a context paragraph at the top of `rule-writing.instructions.md` and as an
opening description in `audit.prompt.md`. The monthly cadence is now explicitly named a
drift-detection cycle in both artifacts. ADR status updated to Accepted.
