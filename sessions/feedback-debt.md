# Feedback Debt Tracker

This tracker is the flywheel's intake queue — observations that have not yet been
promoted to rules or artifacts.

## Health Check

- Open items: 0 / 5 (target: ≤ 5)
- Oldest open item: N/A

## Open Items

| ID | Observation | Entry path | Sessions seen | Priority | Status | Linked artifact |
|----|-------------|------------|---------------|----------|--------|-----------------|

*(No open items.)*

## Closed Items (last 30 days)

| ID | Observation | Closed in session | Artifact created |
|----|-------------|-------------------|------------------|
| FD-001 | `sessions.jsonl` missing structured `corrections` array (lens, mistake, rule_change, rule_ref) | 2026-03-22 | `.github/hooks/_trace.py` (`read_corrections`, `reset_corrections`); `session-end.py` (`corrections` field); `stop.json` additionalContext updated; `tests/test_session_end.py` `TestSessionEndCorrections` |
| FD-002 | `sessions.jsonl` missing `rule_ref` field for knowledge provenance | 2026-03-22 | Same artifacts as FD-001 — `rule_ref` is a field inside each corrections array entry |
| FD-003 | No guardrail against direct push to `main` | 2026-03-22 | HITL issue #45 (branch-protection rule added to repo settings) |
| FD-004 | MCP git tools (`mcp_gitkraken_git_add_or_commit`, `mcp_gitkraken_git_push`) bypass the pre-tool-use security gate | 2026-03-22 | `pre-tool-use.py` (`MCP_GIT_TOOLS`, `check_mcp_git_operation()`); `security-patterns.json` (`blocked_mcp_tools`); `copilot-instructions.md` (Git Operations rules + PRIORITY comments); `tests/test_pre_tool_use.py` (`TestPreToolUseMcpGitBlock`) |

---

## Usage Guide

**Two valid entry paths for new items:**

1. **Direct report** — Add a row immediately when you observe a gap or friction point, even if it has only surfaced once. Set `Entry path` to `Direct report`. Do not assign a lens yet — that requires seeing the issue in at least two sessions.
2. **Lens analysis** — After running `/compact` and analysing findings through the four diagnostic lenses, assign the matching lens number (1–4) as the `Entry path` (e.g. `Lens 1 — Recurring Correction`). This path confirms the issue is recurring and promotion-ready.

**Adding an item:** Add a row to Open Items any session where a finding is not actioned
immediately. Use the next sequential numeric ID.

**Sessions seen:** Increment this count each time the issue recurs in a new session.
When `Sessions seen` reaches 2, this is a Lens 1 signal — promote to `copilot-instructions.md`.

**Closing an item:** Move the row to Closed Items when the corresponding rule or artifact
is committed. Fill in the session date and the artifact path.

**Backlog health rule:** If open items ≥ 5, address the highest-priority (P0) item before
adding new observations. Do not let the backlog grow unbounded.

**Priority guide:**
- P0 — blocks productive work; address this session
- P1 — recurring friction; address within 2 sessions
- P2 — quality improvement; address when capacity allows
- P3 — nice-to-have; defer until other items are closed
