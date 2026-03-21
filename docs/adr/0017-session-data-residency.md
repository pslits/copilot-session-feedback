# ADR-0017: Session Data-Residency Policy

Date: 2026-03-21
Status: Accepted
HITL Issue: [#27](https://github.com/pslits/copilot-session-feedback/issues/27)
Decider: @pslits
Risk Tier: low

---

## Context

The `sessions/` directory is fully gitignored by design — session transcripts may contain
sensitive conversation content and are treated as local-only artefacts. However, any GitHub
Actions workflow that attempts to persist cloud Copilot session data must write to the
repository to be useful (see ADR-0013).

Before building such a workflow, a deliberate policy decision is needed: what subset of
session data (if any) is low-sensitivity enough to commit?

The candidate files are:

| File | Content | Sensitivity |
|---|---|---|
| `sessions/metrics/sessions.jsonl` | Structured metadata only: `session_id`, timestamps, `turn_count`, `duration_seconds` | Low — no conversation content |
| `sessions/<id>/transcript.json` | Full conversation transcript | High — may contain sensitive context |
| `sessions/<id>/metadata.json` | Session metadata including context snippets | Medium–High |

The metrics JSONL file is the observability pipeline output for Feature #6 (SessionEnd hook).
It contains no conversation content and is the minimum viable data set for trend analysis
(corrections per session, duration, turn count).

---

## Decision

> **We decide to expose `sessions/metrics/sessions.jsonl` to version control by adding
> targeted `.gitignore` exceptions, and to keep all other session artefacts
> (transcripts, per-session metadata) fully gitignored.**

The `.gitignore` rules added are:

```
sessions/*
!sessions/metrics/
sessions/metrics/*
!sessions/metrics/sessions.jsonl
```

Using `sessions/*` (wildcard) instead of `sessions` (directory) is required because git
does not apply negation exceptions to files inside a fully-ignored directory. The wildcard
ignores the _contents_ of `sessions/` while keeping the directory itself traversable, which
allows the two `!` negation lines to take effect.

All other files under `sessions/` remain gitignored. This is the narrowest possible
exception that enables automated harvest while protecting conversation content.

---

## Consequences

### Positive
- A GitHub Actions workflow can append minimal rows to `sessions/metrics/sessions.jsonl`
  and commit them without risk of exposing sensitive conversation content.
- The metrics file enables the trend analysis (corrections per session trending down) that
  the Validate stage of the feedback flywheel depends on (see Feature #6 spec).
- The policy decision is explicit and documented; future contributors know exactly what is
  tracked and why.

### Negative / Risks
- Any future addition of sensitive fields to `sessions/metrics/sessions.jsonl` would
  silently become tracked. The schema must be kept strictly to the five fields defined in
  Feature #6: `session_id`, `start_ts`, `end_ts`, `duration_seconds`, `turn_count`.
- If a broader exception is accidentally added to `.gitignore` (e.g. `!sessions/`), full
  transcripts could be committed. The targeted exception pattern guards against this.

### Neutral
- `sessions/metrics/` directory and `sessions.jsonl` do not need to be pre-created in
  the repository; the SessionEnd hook creates them on first run.

---

## What Is Committed vs. What Stays Local

| Artefact | Location | Committed? | Reason |
|---|---|---|---|
| Session metrics JSONL | `sessions/metrics/sessions.jsonl` | ✅ Yes | Structured metadata only; no conversation content |
| Full session transcripts | `sessions/<id>/transcript.json` | ❌ No | May contain sensitive conversation context |
| Per-session metadata | `sessions/<id>/metadata.json` | ❌ No | May contain sensitive context snippets |
| Current trace ID | `sessions/.current_trace_id` | ❌ No | Ephemeral; no value in version control |
| Session plans | `sessions/plans/` | ❌ No | Local planning artefacts |

---

## Schema Reference

The committed `sessions/metrics/sessions.jsonl` file contains one JSON object per line.
Each object has the following fields (and no others):

| Field | Type | Description |
|---|---|---|
| `session_id` | string | Unique identifier for the session (trace ID or generated UUID) |
| `start_ts` | string (ISO 8601) | Session start timestamp |
| `end_ts` | string (ISO 8601) | Session end timestamp |
| `duration_seconds` | number | Elapsed seconds from start to end |
| `turn_count` | number | Number of turns in the session (optional; 0 if not provided) |

No conversation content, file paths, or user-identifiable information is stored in this file.

---

## Rollback Strategy

Revert the `.gitignore` change. Any rows committed to `sessions/metrics/sessions.jsonl`
by GHA workflows would need manual removal or a follow-up commit to truncate.
Risk is low — the file contains no sensitive data.

---

## Follow-up Actions

| Action | Owner | Due Date | Status |
|---|---|---|---|
| Build GHA workflow to append rows to `sessions/metrics/sessions.jsonl` | @pslits | 2026-04-10 | Open |
| Add schema validation to SessionEnd hook (reject unknown fields) | @pslits | 2026-04-10 | Open |

---

## Outcome (complete after execution)

_To be filled after the change is made._
