# ADR-0013: Explore Partial Automation of Feedback Collection (Aspirational)

Date: 2026-03-20
Status: Proposed
HITL Issue: [#21](https://github.com/pslits/copilot-session-feedback/issues/21)
Decider: @pslits
Risk Tier: low

---

## Context

The book's Ch. 11 (Advanced Adaptation: Building Agents That Learn) covers automated feedback
collection — not just human-mediated capture. The framework's current feedback path is 100%
human-initiated: a developer manually runs `/compact` or reviews a session to extract findings.

Partial automation is possible within the existing VS Code-native constraint:
- The Stop hook could auto-scan the session transcript for tool-call correction patterns
  (user immediately follows a tool call with an edit — a common signal of agent error).
- The PostCompact hook could compare which rules were active before compaction against which
  corrections appeared in the session, tagging likely drift candidates.
- The PreCompact hook could export a "rules-in-effect" snapshot that is later compared to the
  post-session correction log.

None of these require external infrastructure. However, they represent Level 4–5 maturity work
and should be deferred until the current manual loop is validated and stable. This ADR documents
the aspiration for the adoption roadmap's Ongoing phase.

**Cloud-agent extension (concrete scenario — ADR-0016):** When an issue is assigned to the
GitHub Copilot coding agent, all work runs in a GitHub-hosted cloud environment and no local
hooks fire. ADR-0016 documents a hybrid path: a manual runbook step for immediate use and a
deferred GitHub Actions harvest workflow that appends a minimal row to
`sessions/metrics/sessions.jsonl` on each cloud Copilot PR merge. The data-residency policy
for that workflow is covered by ADR-0017.

---

## Decision

> **We decide to document automated feedback collection as an aspirational capability in the
> adoption roadmap's Ongoing phase, with a prerequisite of at least 8 weeks of stable manual
> loop operation before any automation is introduced.**

No implementation work is approved at this time. This ADR is a planning record that:
1. Names the automation options that are within the VS Code-native constraint.
2. Sets a stability prerequisite to prevent premature automation.
3. Links the aspiration to Ch. 11 of the book for future reference.

---

## Consequences

### Positive
- The aspirational roadmap is visible; contributors know where the flywheel evolution leads.
- The stability prerequisite prevents automation being introduced before the manual loop is
  mature enough to generate reliable training signal.

### Negative / Risks
- None. This ADR approves only documentation, not implementation.

### Neutral
- When the prerequisite is met, a new ADR will be required to approve the specific automation
  approach.

---

## Follow-up Actions

| Action | Owner | Due Date | Status |
|---|---|---|---|
| Add automated feedback collection entry to adoption roadmap Ongoing phase | @pslits | 2026-04-03 | Open |
| Note stability prerequisite (8 weeks manual loop) in the entry | @pslits | 2026-04-03 | Open |

---

## Outcome (complete after execution)

_To be filled after the change is made._
