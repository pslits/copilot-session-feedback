# Feedback Debt Tracker

This tracker is the flywheel's intake queue — observations that have not yet been
promoted to rules or artifacts.

## Health Check

- Open items: 1 / 5 (target: ≤ 5)
- Oldest open item: ADR-0016 review

## Open Items



| ID | Observation | Pattern triggered | Sessions seen | Priority | Status | Linked artifact |
|----|-------------|-------------------|---------------|----------|--------|-----------------|
| FD-001 | Self-learning loop is incomplete: `sessions.jsonl` captures timing and turn-count but not **corrections data** (lens, mistake, rule change) nor **rule attribution** (which `copilot-instructions.md` rule was added as a result). Without these two fields, "corrections per session" can only be tallied manually and recurrence cannot be detected automatically. | Lens 1 — Recurring Correction | 1 | P1 | Open | New ADR + `corrections.jsonl` schema; see ADR-0016. Proposed: define schema with `session_id`, `lens` (1–4), `description`, `rule_ref` and update Stop hook to prompt for structured input rather than free-text. |

## Closed Items (last 30 days)

| ID | Observation | Closed in session | Artifact created |
|----|-------------|-------------------|------------------|

---

## Usage Guide

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
