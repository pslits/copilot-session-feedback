# ADR-0016: Cloud Copilot Session Harvest Strategy

Date: 2026-03-21
Status: Accepted
HITL Issue: [#26](https://github.com/pslits/copilot-session-feedback/issues/26)
Decider: @pslits
Risk Tier: low

---

## Context

The existing feedback loop relies on VS Code-native hooks (`stop.py`, `session-end.py`) that
fire only during local developer sessions. When an issue is assigned to the GitHub Copilot
coding agent, work executes in a GitHub-hosted cloud environment — no local hooks fire, no
transcript is written to `sessions/`, and no entry appears in
`sessions/metrics/sessions.jsonl`.

The PR created by Copilot contains an activity/session log, but there is no defined path to
ingest that log into the local feedback structure. This leaves cloud-agent sessions invisible
to the feedback loop and breaks the continuity of the improvement flywheel.

ADR-0013 documents automated feedback collection as aspirational (VS Code-native only); this
gap extends that aspiration to cover the cloud-agent execution path.

A prerequisite constraint exists: `sessions/` is fully gitignored by design. Any automated
workflow writing cloud session data must respect the data-residency policy defined in
ADR-0017, which limits committed artefacts to `sessions/metrics/sessions.jsonl` only
(structured metadata; no conversation content).

---

## Decision

> **We decide to adopt a hybrid approach: formalise a manual runbook step immediately, and
> defer the automated GitHub Actions harvest workflow until the data-residency policy
> (ADR-0017) is implemented and the manual path has confirmed a stable schema.**

Options evaluated:

| Option | Description | Verdict |
|---|---|---|
| 1 — Do nothing | Cloud sessions remain invisible | Rejected — instruction drift is never captured |
| 2 — Manual runbook | Developer copies corrections from the PR log into `sessions/` by hand | Accepted for immediate implementation |
| 3 — GHA workflow | Workflow appends a structured row to `sessions/metrics/sessions.jsonl` on PR merge | Deferred — blocked on ADR-0017 |
| 4 — Hybrid (selected) | Manual runbook now; automate once schema is stable | Accepted |

The manual path (Option 2) is unblocked today: a developer can run a documented checklist
locally after a cloud Copilot PR is merged, writing files to their own `sessions/`
directory under the existing gitignore rules. The runbook section added by this ADR
formalises that checklist.

The automated path (Option 3) is deferred until:
1. ADR-0017 `.gitignore` exceptions are merged and the schema is stable.
2. At least one manual harvest cycle has confirmed the entry format.

---

## Consequences

### Positive
- Cloud Copilot sessions are no longer invisible to the feedback loop once the manual
  checklist is followed.
- The manual step costs roughly 5 minutes per merged PR and requires no infrastructure.
- The runbook section doubles as the specification for the future automated harvest workflow.

### Negative / Risks
- Manual harvest depends on developer discipline; sessions will still be missed if the
  checklist is not followed after each cloud Copilot PR merge.
- The automated path is deferred, so trend analysis in `sessions/metrics/sessions.jsonl`
  will not include cloud-agent sessions until Option 3 is built.

### Neutral
- The `sessions/` gitignore rules are unchanged by this ADR (ADR-0017 owns that change).
- The per-session directory structure written by the manual checklist mirrors what the future
  automated workflow will produce.

---

## Follow-up Actions

| Action | Owner | Due Date | Status |
|---|---|---|---|
| Add "Harvesting Cloud Copilot Session Logs" section to `docs/hitl/runbook.md` | @pslits | 2026-04-10 | Done |
| Build GHA harvest workflow once ADR-0017 schema is stable | @pslits | 2026-05-01 | Open |
| Add note to ADR-0013 referencing cloud-agent path as concrete extension scenario | @pslits | 2026-04-10 | Done |

---

## Outcome (complete after execution)

_To be filled after the change is made._
