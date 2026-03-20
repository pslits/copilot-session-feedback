# ADR-0011: Introduce Trace ID Threading Across Lifecycle Hook Events

Date: 2026-03-20
Status: Proposed
HITL Issue: [#19](https://github.com/pslits/copilot-session-feedback/issues/19)
Decider: @pslits
Risk Tier: high

---

## Context

The book's Ch. 10 (System-Level Patterns for Production Readiness) identifies the trace ID as the
fundamental unit of observability in Lifecycle Callbacks / AgentOps: a single identifier that
links every lifecycle event (SessionStart → PreToolUse → PostToolUse → ... → SessionEnd) into a
reconstructable session trace.

The framework's `sessions.jsonl` logs timestamps and session IDs but there is no evidence that the
same trace ID is present in all hook events for a given session. Without it:
- It is impossible to reconstruct "exactly what happened in session X" from the JSONL alone.
- The Stop hook archives transcripts to a session directory but hook event records at non-Stop
  events have no reference to the session they belong to.
- Debugging "why did hook Y fire in session Z" requires manual timestamp correlation, which is
  fragile.

This is the highest-priority gap from the book review because it is a functional observability
gap, not a framing issue. The Lifecycle Callbacks pattern is only partially implemented without
cross-event trace correlation.

Risk is classified **high** because adding a trace ID to all hooks requires coordinated changes
across multiple hook scripts and the sessions.jsonl schema — a wider blast radius than any other
gap fix.

---

## Decision

> **We decide to introduce a session-scoped trace ID (UUID v4, generated at SessionStart) that is
> written to a temporary session state file and read by all subsequent hooks in the same session,
> and to extend the sessions.jsonl schema to include the trace_id field in every event record.**

Implementation approach:
1. SessionStart hook: generate `trace_id=$(uuidgen)`, write to `.session_trace` temp file.
2. All other hooks that log to sessions.jsonl: read trace_id from `.session_trace` before writing.
3. Stop hook: include trace_id in the archive directory name or metadata.json.
4. SessionEnd hook: delete `.session_trace` and write final record with trace_id to sessions.jsonl.
5. Document the `.session_trace` file lifecycle and the trace_id field in hooks.instructions.md.

Fallback if `.session_trace` is missing: use `"trace_id": "unknown-<timestamp>"` to prevent parse
failures while making the gap visible.

---

## Consequences

### Positive
- Full session reconstruction from sessions.jsonl becomes possible.
- Debugging multi-hook failures is reduced from manual timestamp correlation to trace_id lookup.
- Completes the Lifecycle Callbacks / AgentOps pattern implementation.
- Aligns the framework with Ch. 10's observability requirements.

### Negative / Risks
- Requires coordinated changes to all hook scripts that write to sessions.jsonl.
- The `.session_trace` temp file is a new external dependency for hook scripts; if SessionStart
  hook fails, downstream hooks will fall back to "unknown" — acceptable but visible.
- `uuidgen` may not be available on all platforms. Fallback: use `python -c "import uuid; print(uuid.uuid4())"`.

### Neutral
- The trace_id is a v4 UUID; it is not cryptographically signed and provides no security guarantees.
  It is an observability tool only.

---

## Follow-up Actions

| Action | Owner | Due Date | Status |
|---|---|---|---|
| Update SessionStart hook to generate and write trace_id | @pslits | 2026-04-03 | Open |
| Update all hooks that write to sessions.jsonl to include trace_id | @pslits | 2026-04-03 | Open |
| Update sessions.jsonl schema documentation | @pslits | 2026-04-03 | Open |
| Update hooks.instructions.md with trace_id lifecycle | @pslits | 2026-04-03 | Open |
| Add uuidgen fallback for cross-platform compatibility | @pslits | 2026-04-03 | Open |
| Test full session trace reconstruction from sessions.jsonl | @pslits | 2026-04-10 | Open |

---

## Outcome (complete after execution)

_To be filled after the change is made._
