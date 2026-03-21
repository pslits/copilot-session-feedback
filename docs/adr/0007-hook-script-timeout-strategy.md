# ADR-0007: Specify Hook Script Timeout and Soft-Fail Strategy

Date: 2026-03-20
Status: Accepted
HITL Issue: [#15](https://github.com/pslits/copilot-session-feedback/issues/15)
Decider: @pslits
Risk Tier: medium

---

## Context

The framework makes external calls from hook scripts: git operations (Stop hook), shell formatters
(PostToolUse), and optionally curl (Notification hook). These are real failure surfaces. The book's
Ch. 7 (Robustness and Fault Tolerance) notes that Circuit Breaker logic applies even without named
external services — any external call that can hang or fail silently needs a timeout contract.

Currently:
- No maximum execution time is specified for any hook script.
- A hanging `git` or `curl` call would block the VS Code agent indefinitely.
- The hooks.instructions.md documents exit codes (0/2/other) but has no wall-clock budget.
- The Notification hook's `curl` failure mode is completely undocumented.

This is the framework's primary production reliability gap: a slow network or locked git index
could hang the Stop hook and block session end.

---

## Decision

> **We decide to specify a maximum execution time of 5000ms per hook script (hard limit), enforce
> timeouts on all external calls within scripts, and document the soft-fail behaviour for each
> hook when the timeout is exceeded.**

The initial proposal was 2000ms. After reviewing all six hook scripts, 2000ms was found to be
too tight: `post-tool-use.py` already uses `subprocess.run(..., timeout=5)` for shell formatter
invocations, which can legitimately run up to 5000ms. All other hooks complete in under 100ms.
The budget was raised to 5000ms to reflect the honest maximum derived from the actual scripts
(see HITL comment thread on issue #15, Option 2).

Specific decisions:
- All hook scripts must complete within 5000ms (measured from hook invocation to exit).
- Network calls must use an explicit timeout ≤ 5000ms total. The Notification hook uses
  `urllib.request.urlopen(..., timeout=2)` — this remains unchanged and well within budget.
- Subprocess formatter calls (PostToolUse hook) use `subprocess.run(..., timeout=5)`, which
  aligns exactly with the 5000ms outer budget.
- `git` operations in hook scripts must be local-only (no remote calls). The Stop hook performs
  only local filesystem operations (file copy + metadata write) and requires no git guard.
- Timeout expiry = exit code 2 (soft block) — the agent is informed but not hard-blocked.
- This strategy is documented in hooks.instructions.md and in the Exception Handling catalogue
  entry.

---

## Consequences

### Positive
- Eliminates the hang risk from external calls in hooks.
- Aligns the framework with Ch. 7 fault tolerance recommendations.
- Provides a concrete, testable performance contract for all hook scripts.

### Negative / Risks
- 5000ms may still be too tight on very slow machines or under heavy I/O load for formatter
  invocations. The threshold should be validated in practice and adjusted if needed.
- Adding explicit timeout contracts to scripts slightly increases cognitive overhead.

### Neutral
- The 5000ms budget applies to the entire script, not per-call. Multi-call scripts must budget
  accordingly.
- The budget was raised from the initial 2000ms proposal after reviewing that the PostToolUse
  formatter subprocess already uses a 5s timeout internally.

---

## Follow-up Actions

| Action | Owner | Due Date | Status |
|---|---|---|---|
| Add timeout budget section to hooks.instructions.md | @pslits | 2026-04-03 | Done |
| Add timeout documentation to Notification hook | @pslits | 2026-04-03 | Done — hook uses `urllib` with `timeout=2`; no curl involved |
| Confirm Stop hook has no blocking git/remote calls | @pslits | 2026-04-03 | Done — Stop hook is local FS only |
| Update Exception Handling catalogue entry with timeout strategy | @pslits | 2026-04-03 | Done |

---

## Outcome (complete after execution)

**Implemented 2026-03-21.**

- `hooks.instructions.md` updated with a "Timeout Budget" section specifying the 5000ms per-script
  budget and soft-fail (exit 2) behaviour.
- ADR status changed from Proposed → Accepted with the 5000ms budget documented.
- Exception Handling catalogue entry updated to reference the hook timeout strategy.
- All six hook scripts were reviewed; no code changes were required:
  - `post-tool-use.py` already uses `subprocess.run(..., timeout=5)` — aligns with the 5000ms budget.
  - `notification.py` already uses `urllib.request.urlopen(..., timeout=2)` — within budget.
  - All remaining hooks (`stop.py`, `session-end.py`, `pre-tool-use.py`, `post-compact.py`,
    `pre-compact.py`, `session-start.py`) are local FS only and complete in under 50ms.
