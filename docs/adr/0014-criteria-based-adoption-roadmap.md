# ADR-0014: Convert Adoption Roadmap from Time-Based to Criteria-Based Phases

Date: 2026-03-20
Status: Proposed
HITL Issue: [#22](https://github.com/pslits/copilot-session-feedback/issues/22)
Decider: @pslits
Risk Tier: medium

---

## Context

The book's Ch. 12 (A Practical Roadmap: Implementing Agentic Patterns by Maturity Level) uses
observable capability thresholds per maturity level, not calendar time, to gate progression. The
framework's adoption roadmap in adoption-roadmap.instructions.md currently uses weeks ("Week 1",
"Week 2", "Week 4") as phase delimiters.

The problem with time-based phases:
- A developer who completes Week 1 in 3 days gains no signal to advance to Week 2.
- A developer who is blocked for 3 weeks on Week 1 has no criterion to recognise the blockage.
- Teams adopting the framework at different times cannot coordinate using calendar references.

Criteria-based phases (e.g., "advance to Phase 2 when: at least 2 sessions have produced rule
commits AND the `/verify` prompt passes without errors") are independently measurable by any
developer at any start date.

Time references can be kept as *guidance* ("typically 1–2 weeks") but must not be the gate.

---

## Decision

> **We decide to convert the adoption-roadmap.instructions.md phases from time-gated to
> criteria-gated, adding at least one observable success threshold per phase that must be met
> before proceeding to the next phase. Time estimates are retained as guidance in parentheses.**

Proposed phase thresholds (to be validated):
- **Phase 1 complete:** `/verify` prompt passes in a live session AND at least one rule has been
  committed from a session finding.
- **Phase 2 complete:** Stop hook is operational (exit 0 on session end) AND at least one hook
  event is logged to sessions.jsonl.
- **Phase 3 complete:** RPI chain has been used end-to-end at least once AND a planner-produced
  plan has been executed successfully by @implementer.
- **Ongoing threshold:** Corrections per session trending downward over 4 consecutive sessions.

---

## Consequences

### Positive
- Progression is independently verifiable by any developer.
- Blocked phases are detectable: if criteria are unmet after 3× the typical time estimate, it
  signals a setup problem.
- Aligns the roadmap with Ch. 12's maturity-level capability thresholds.
- Works for teams with different start dates.

### Negative / Risks
- Converting the existing roadmap requires rewriting the phase headers and adding criteria
  sections — moderate effort.
- The proposed thresholds are initial estimates; they may need adjustment based on real-world
  adoption experience. Version the criteria in the file.

### Neutral
- Time estimates remain as guidance; removing them entirely would lose useful planning context.

---

## Follow-up Actions

| Action | Owner | Due Date | Status |
|---|---|---|---|
| Rewrite adoption-roadmap.instructions.md phase gates to criteria-based | @pslits | 2026-04-10 | Open |
| Add time estimates as parenthetical guidance | @pslits | 2026-04-10 | Open |
| Validate proposed thresholds against actual adoption experience | @pslits | 2026-05-01 | Open |
| Cross-reference ADR-0014 in the roadmap file | @pslits | 2026-04-10 | Open |

---

## Outcome (complete after execution)

_To be filled after the change is made._
