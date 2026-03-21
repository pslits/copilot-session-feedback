# Feedback Debt

Observations from sessions that need to be promoted to a rule, prompt, agent, or hook.
Items are ordered by priority (P0 = highest). Mark items Done once promoted.

| ID | Priority | Status | Session / Source | Observation | Target surface | Notes |
|----|----------|--------|-----------------|-------------|----------------|-------|
| FD-001 | P1 | Open | ADR-0016 review | Self-learning loop is incomplete: `sessions.jsonl` captures timing and turn-count but not **corrections data** (lens, mistake, rule change) nor **rule attribution** (which `copilot-instructions.md` rule was added as a result). Without these two fields, "corrections per session" can only be tallied manually and recurrence cannot be detected automatically. | New ADR + `corrections.jsonl` schema | See ADR-0016 comment thread. Proposed next step: define a `corrections.jsonl` schema with `session_id`, `lens` (1–4), `description`, `rule_ref` fields and update the Stop hook to prompt for structured input rather than free-text. |
