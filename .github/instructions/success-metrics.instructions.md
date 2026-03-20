---
name: success-metrics
description: Success metrics and anti-metrics for the Copilot feedback system. Apply when reviewing session quality, answering "Is the system improving?", or tracking feedback-loop health in session files.
applyTo: "sessions/**"
---

# Success Metrics — Copilot Feedback System

Rule: Evaluate feedback-system health using the five metrics below. Do not track
vanity metrics. Report at least one metric value when asked "Is the system improving?"
Reason: Qualitative statements about improvement are not actionable — these five
metrics provide objective, trend-based answers using data collected automatically
or with a single manual tally.

## Five Metrics

| Metric | Collection method | Healthy target | Anti-metric (do not track) |
|--------|-------------------|----------------|---------------------------|
| Corrections per session | Manual tally at session end | Trending ↓ over 4 weeks | Rule count (more rules ≠ better) |
| Time to first correct output | Manual: note when agent first gets it right | Trending ↓ | Session duration |
| Feedback debt backlog | Auto: count open items in `sessions/feedback-debt.md` | ≤ 5 open items | Items added per session |
| Stale rule count | Auto: `/audit` output | 0 stale rules | Total rule count |
| Hook failure rate | Auto: `sessions/metrics/sessions.jsonl` | 0 failures per week | Hook count |

Rule: When the feedback-debt backlog reaches 5 open items, address the highest-priority
(P0) item before adding new observations.
Reason: An unbounded backlog signals the flywheel has stalled — the observation buffer
is filling faster than it is being actioned.

Rule: Report "corrections per session" as the primary improvement signal. Use the
remaining four metrics as diagnostic signals only.
Reason: Corrections per session is the only metric that directly measures whether the
agent is learning from the feedback loop. All other metrics are leading or lagging
indicators.

## Collection Notes

- **SessionEnd hook** auto-collects timestamps into `sessions/metrics/sessions.jsonl`.
  This file may not exist until Feature #6 (SessionEnd hook) is implemented.
- **Corrections per session** is the single manual tally — no form, no dashboard.
  Note the count at session end; one number per session.
- **Stale rule count** is auto-calculated by running `/audit` monthly.
  Skip if `copilot-instructions.md` has fewer than 15 rules.
