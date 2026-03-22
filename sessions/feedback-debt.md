# Feedback Debt Tracker

This tracker is the flywheel's intake queue — observations that have not yet been
promoted to rules or artifacts.

## Health Check

- Open items: 2 / 5 (target: ≤ 5)
- Oldest open item: ADR-0016 review

## Open Items

| ID | Observation | Entry path | Sessions seen | Priority | Status | Linked artifact |
|----|-------------|------------|---------------|----------|--------|-----------------|
| FD-001 | `sessions.jsonl` does not capture **corrections data** — the structured fields `lens` (1–4), `mistake`, and `rule_change` that would allow automatic recurrence detection. Without this field, "corrections per session" can only be tallied manually. | Direct report | 1 | P1 | Open | New schema: add `corrections` array to session record; update Stop hook to prompt for structured input rather than free-text. |
| FD-002 | `sessions.jsonl` does not capture **rule attribution** — which `copilot-instructions.md` rule was added or changed as a result of a session. Without `rule_ref`, it is impossible to trace knowledge provenance automatically. | Direct report | 1 | P2 | Open | Same schema work as FD-001; add `rule_ref` field alongside `corrections` array. |

## Closed Items (last 30 days)

| ID | Observation | Closed in session | Artifact created |
|----|-------------|-------------------|------------------|

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
