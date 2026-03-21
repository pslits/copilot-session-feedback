# ADR-0008: Re-classify Collaborative Co-piloting as Primary Interaction Mode

Date: 2026-03-20
Status: Accepted
HITL Issue: [#16](https://github.com/pslits/copilot-session-feedback/issues/16)
Decider: @pslits
Risk Tier: low

---

## Context

The design document's pattern rejection table labels Collaborative Co-piloting (A&B, Tier 5) as
"general model, not a design choice." This is a significant under-classification. The book's Ch. 8
describes Collaborative Co-piloting as the mode where human and agent work simultaneously with the
human retaining final authority — which is exactly the primary interaction mode of this system.

The entire feedback loop exists *because* the developer is co-piloting with Copilot every day.
The friction, corrections, and vocabulary gaps that feed the flywheel are all artefacts of the
co-piloting experience. Misclassifying this as "not a design choice" makes the trigger context
for the whole system invisible in the design document.

Correcting this also sharpens the framing: the feedback loop is not a general improvement system —
it is a co-piloting quality improvement system specifically. The success metrics and the human gates
all derive from co-piloting context.

---

## Decision

> **We decide to re-classify Collaborative Co-piloting from "rejected (general model)" to
> "foundational context" in the design document, and to add a brief description of it as the
> trigger interaction mode that justifies the entire feedback loop.**

The pattern itself does not need to be added to the "Recommended Patterns" table — it is the
environment, not a component of the pipeline. A dedicated paragraph in the System Summary section
of the design document is the appropriate location.

---

## Consequences

### Positive
- The design rationale for the feedback loop is explicit and traceable to the book.
- Future contributors immediately understand the interaction context without having to infer it.
- Correct classification removes a potential point of confusion when reviewing the rejection table.

### Negative / Risks
- None. Documentation-only change.

### Neutral
- The framing change may prompt a discussion about whether the system is applicable to non-
  co-piloting agent modes (autonomous agents). That is a valid future question.

---

## Follow-up Actions

| Action | Owner | Due Date | Status |
|---|---|---|---|
| Update System Summary in design document | @pslits | 2026-04-03 | Done |
| Update rejection table entry for Collaborative Co-piloting | @pslits | 2026-04-03 | Done |

---

## Outcome (complete after execution)

Both changes have been applied to `docs/design/copilot-feedback-system-pattern-design.md`:

1. A **Primary Interaction Mode** paragraph was added to the System Summary, naming Collaborative
   Co-piloting as the foundational context and clarifying that the feedback loop is a co-piloting
   quality improvement system specifically.

2. The Tier 5 rejection table entry was updated from _"general model, not a design choice"_ to
   _"foundational context — the interaction mode the feedback loop serves; not a pipeline component"_.
