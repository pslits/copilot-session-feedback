# ADR-0003: Define Formal Input/Output Schemas for RPI Agent Chain

Date: 2026-03-20
Status: Proposed
HITL Issue: [#11](https://github.com/pslits/copilot-session-feedback/issues/11)
Decider: @pslits
Risk Tier: medium

---

## Context

The book's Ch. 4 (Agentic AI Architecture: Components and Interactions) stresses that agent
contracts — defined input/output schemas — are non-negotiable for reliable multi-agent systems.
Context loss at handoffs is the primary failure mode cited.

The framework's three agents (`@researcher`, `@planner`, `@implementer`) currently have no formal
contract table. Their agent files define roles and procedures but do not specify:
- What exact artefacts each accepts as input
- What exact artefacts each must produce before handing off
- How handoff failure (missing output) is detected

Without schemas, context loss at the `@researcher → @planner` handoff (summarisation too aggressive,
losing file:line references) is the documented but unmitigated highest-probability failure mode.

---

## Decision

> **We decide to add a formal contract section to each of the three RPI agent files, specifying
> required input artefacts, required output artefacts, and the failure signal for an incomplete
> handoff.**

The contract table format will follow the book's Ch. 4 component interaction model:

| Item | Format | Required |
|---|---|---|
| Input: session summary | Markdown with lens classifications | Yes |
| Output: findings table | File:line references for each finding | Yes |

---

## Consequences

### Positive
- Handoff failures are detectable (missing required output → visible gap).
- The `@researcher` output template can enforce file:line citation as a contract obligation.
- Aligns the framework with Ch. 4 of the book.

### Negative / Risks
- Adding schema validation to agent files increases their length; must stay within token budget.
- If the schema is too prescriptive, the agent becomes brittle to natural variation in session
  content.

### Neutral
- The contract table may need to evolve as the agents mature; version it alongside the ADR.

---

## Follow-up Actions

| Action | Owner | Due Date | Status |
|---|---|---|---|
| Add contract section to @researcher agent file | @pslits | 2026-04-03 | Open |
| Add contract section to @planner agent file | @pslits | 2026-04-03 | Open |
| Add contract section to @implementer agent file | @pslits | 2026-04-03 | Open |
| Cross-reference ADR-0003 in each agent file | @pslits | 2026-04-03 | Open |

---

## Outcome (complete after execution)

_To be filled after the change is made._
