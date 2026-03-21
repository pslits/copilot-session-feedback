# ADR-0010: Document Why Fixed Procedures Outperform ReAct in This Context

Date: 2026-03-20
Status: Accepted
HITL Issue: [#18](https://github.com/pslits/copilot-session-feedback/issues/18)
Decider: @pslits
Risk Tier: low

---

## Context

The patterns catalogue correctly excludes ReAct (Reason + Act) for the framework's agents, stating
"agents use fixed procedures." However, the rationale is missing from the entry and from the agent
files themselves.

The book's Ch. 9 provides the theoretical foundation for this tradeoff: ReAct agents are more
adaptive but less predictable. In a feedback loop system where reproducibility and auditability
are critical — each run must produce a comparable output so improvements can be measured against
a baseline — fixed procedures are demonstrably superior to ReAct's open-ended reasoning loops.

Without this explanation:
- Future contributors may add ReAct-style open-ended reasoning to agent prompts, not realising
  they are degrading the system's auditability.
- The framework appears to reject ReAct arbitrarily rather than for principled reasons.
- The tradeoff between adaptability and predictability is invisible.

---

## Decision

> **We decide to add a "Design Rationale" note to the ReAct Agent catalogue entry and to the
> agent files explaining why fixed-procedure agents are the correct choice in an auditable
> feedback loop system, referencing the predictability-vs-adaptability tradeoff from Ch. 9.**

The note will read: "Fixed procedures are preferred over ReAct in this system because the feedback
loop requires reproducible, auditable outputs that can be compared across sessions. ReAct's dynamic
reason-act loops introduce output variability that would make session-over-session improvement
measurement unreliable. Adaptability is achieved through the feedback loop itself (weekly rule
updates), not through per-invocation dynamic reasoning."

---

## Consequences

### Positive
- The rejection of ReAct is principled and traceable to Ch. 9.
- Future contributors are warned against introducing open-ended reasoning.
- Auditability as a first-class design goal is explicit.

### Negative / Risks
- None. Documentation-only change.

### Neutral
- Some tasks (e.g., complex codebase research) might genuinely benefit from ReAct. The note
  should acknowledge this nuance while defending the current choice.

---

## Follow-up Actions

| Action | Owner | Due Date | Status |
|---|---|---|---|
| Update ReAct Agent catalogue entry with design rationale | @pslits | 2026-04-03 | Done |
| Add design rationale comment to @researcher agent file | @pslits | 2026-04-03 | Done |

---

## Outcome (complete after execution)

Design rationale added to two locations:
- `patterns-catalogue.md` — ReAct Agent entry now includes a "Design Rationale" blockquote
  explaining the predictability-vs-adaptability tradeoff, the auditability requirement, and a
  note acknowledging the nuance for open-ended tasks.
- `researcher.agent.md` — system prompt now opens with a matching "Design Rationale" blockquote
  referencing this ADR.

Both changes are documentation-only; no agent behaviour was modified.
