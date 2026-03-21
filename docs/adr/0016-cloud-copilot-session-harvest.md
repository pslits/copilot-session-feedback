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

The PR created by Copilot contains an activity/session log, but there was no defined path to
ingest that log into the local feedback structure. This leaves cloud-agent sessions invisible
to the feedback loop and breaks the continuity of the improvement flywheel.

ADR-0013 documents automated feedback collection as aspirational (VS Code-native only); this
gap extends that aspiration to cover the cloud-agent execution path.

The prerequisite data-residency policy (ADR-0017) has now been implemented: `.gitignore`
exceptions expose `sessions/metrics/sessions.jsonl` to version control while keeping all
other session artefacts (transcripts, per-session metadata) gitignored. This unblocks the
automated harvest workflow.

---

## Decision

> **We decide to implement a GitHub Actions workflow (`copilot-session-harvest.yml`) that
> automatically appends a structured metrics row to `sessions/metrics/sessions.jsonl`
> whenever a `copilot/*` branch PR is merged.**

Options evaluated:

| Option | Description | Verdict |
|---|---|---|
| 1 — Do nothing | Cloud sessions remain invisible | Rejected — instruction drift is never captured |
| 2 — Manual runbook | Developer copies corrections from the PR log into `sessions/` by hand | Superseded — manual fallback only if workflow is disabled |
| 3 — GHA workflow (selected) | Workflow appends a metrics row to `sessions/metrics/sessions.jsonl` on PR merge | Accepted — ADR-0017 unblocks this path |
| 4 — Hybrid | Manual runbook now; automate once schema is stable | Superseded — ADR-0017 is implemented; schema is stable |

The workflow:
1. Triggers on `pull_request` closed events where `merged == true` and the head branch
   matches `copilot/*`.
2. Derives the session ID from the branch name (e.g. `copilot/issue-26` →
   `copilot-issue-26-<YYYYMMDD>`).
3. Appends one JSONL row to `sessions/metrics/sessions.jsonl` with fields matching the
   schema used by the VS Code `session-end.py` hook:
   `session_id`, `trace_id` (null for cloud runs), `start_ts`, `end_ts`,
   `duration_seconds`, `turn_count` (PR commit count as proxy).
4. Commits and pushes the updated file to the base branch using the
   `github-actions[bot]` identity.

---

## Consequences

### Positive
- Cloud Copilot sessions are automatically captured in `sessions/metrics/sessions.jsonl`
  without any manual intervention.
- The metrics row is schema-compatible with the VS Code `session-end.py` output, so
  trend analysis works across both local and cloud sessions.
- The workflow costs no infrastructure — it runs on GitHub-hosted runners using the
  existing `GITHUB_TOKEN`.

### Negative / Risks
- `turn_count` for cloud runs uses PR commit count as a proxy, which is a coarser
  signal than the VS Code hook's turn count. This is a known approximation.
- The workflow pushes directly to the base branch (`main`). If branch protection
  requires PRs for all pushes, the `GITHUB_TOKEN` push will fail. A bypass rule for
  `github-actions[bot]` would be needed.
- Full session transcripts (Copilot reasoning, tool calls) are not captured — only
  the structured metrics fields. This is by design (ADR-0017).

### Neutral
- The `.gitignore` exceptions required by this workflow were implemented in ADR-0017
  and are already merged.
- The per-session directory structure (`sessions/YYYY-MM-DD/<id>/`) is not written
  by this workflow; full transcript harvest remains out of scope.

---

## Follow-up Actions

| Action | Owner | Due Date | Status |
|---|---|---|---|
| Create `.github/workflows/copilot-session-harvest.yml` | @pslits | 2026-04-10 | Done |
| Add note to ADR-0013 referencing cloud-agent path as concrete extension scenario | @pslits | 2026-04-10 | Done |
| Add schema validation to SessionEnd hook (reject unknown fields) | @pslits | 2026-05-01 | Open |

---

## Outcome (complete after execution)

_To be filled after the change is made._
