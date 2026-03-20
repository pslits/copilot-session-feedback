# ADR-0007: Specify Hook Script Timeout and Soft-Fail Strategy

Date: 2026-03-20
Status: Proposed
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

> **We decide to specify a maximum execution time of 2000ms per hook script (hard limit), enforce
> timeouts on all external calls within scripts, and document the soft-fail behaviour for each
> hook when the timeout is exceeded.**

Specific decisions:
- All hook scripts must complete within 2000ms (measured from hook invocation to exit).
- `curl` calls must use `--max-time 3 --connect-timeout 2`.
- `git` operations that may block (e.g., waiting for remote) must be replaced with local-only
  equivalents or wrapped with `timeout 2`.
- Timeout expiry = exit code 2 (soft block) — the agent is informed but not hard-blocked.
- This strategy is documented in hooks.instructions.md and in the Exception Handling catalogue entry.

---

## Consequences

### Positive
- Eliminates the hang risk from external calls in hooks.
- Aligns the framework with Ch. 7 fault tolerance recommendations.
- Provides a concrete, testable performance contract for all hook scripts.

### Negative / Risks
- 2000ms may be too tight on slow machines or for complex git operations. The threshold should
  be validated in practice and adjusted. Starting value is a proposal, not a hard requirement.
- Adding timeouts to shell scripts increases complexity slightly.

### Neutral
- The 2000ms budget applies to the entire script, not per-call. Multi-call scripts must budget
  accordingly.

---

## Follow-up Actions

| Action | Owner | Due Date | Status |
|---|---|---|---|
| Add timeout budget section to hooks.instructions.md | @pslits | 2026-04-03 | Open |
| Add --max-time flags to Notification hook curl template | @pslits | 2026-04-03 | Open |
| Wrap Stop hook git operation with timeout guard | @pslits | 2026-04-03 | Open |
| Update Exception Handling catalogue entry with timeout strategy | @pslits | 2026-04-03 | Open |

---

## Outcome (complete after execution)

_To be filled after the change is made._
