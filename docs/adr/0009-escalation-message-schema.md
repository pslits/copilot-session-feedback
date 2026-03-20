# ADR-0009: Define Escalation Message Schema for Soft-Block (Exit Code 2)

Date: 2026-03-20
Status: Proposed
HITL Issue: [#17](https://github.com/pslits/copilot-session-feedback/issues/17)
Decider: @pslits
Risk Tier: low

---

## Context

The book's Ch. 8 (Human-Agent Interaction Patterns) — specifically the "Agent Calls Human (HITL
Escalation)" pattern — stresses that the quality of the escalation message determines whether the
human can make a useful decision. Poor escalation messages (e.g., "blocked" with no context) lead
to human confusion rather than resolution.

The framework implements soft-block escalation via PreToolUse hook exit code 2: the agent's
intended action is paused and a message is shown to the developer. However, the security-patterns.json
file defines the blocked patterns but does not specify the format of the message shown when a block
triggers. Some current messages may be "Blocked: [pattern]" without a reason, an override path, or
a recommended alternative.

This means the developer is interrupted but not helped — they must infer why the block occurred and
how to proceed, adding friction and potentially causing them to disable the hook entirely.

---

## Decision

> **We decide to define and enforce a structured escalation message schema for all exit code 2
> responses from hook scripts, and to update the security-patterns.json template and hooks
> documentation accordingly.**

Schema (3 mandatory fields):

```
BLOCKED: <action attempted in one line>
REASON:  <why this action is protected — policy or risk>
NEXT:    <what the developer should do instead, or how to override>
```

All PreToolUse soft-blocks must use this schema. The schema is documented in hooks.instructions.md.

---

## Consequences

### Positive
- Developer has actionable context when blocked, reducing friction.
- Aligns with Ch. 8 escalation message quality requirements.
- Override path is explicit, reducing the temptation to disable the hook entirely.

### Negative / Risks
- Existing security-patterns.json entries need message field updates — small but real effort.
- If the message is too detailed, it may distract from the agent's primary task flow.

### Neutral
- The schema is line-oriented for easy parsing by both humans and future automation.

---

## Follow-up Actions

| Action | Owner | Due Date | Status |
|---|---|---|---|
| Define schema in hooks.instructions.md | @pslits | 2026-04-03 | Open |
| Update security-patterns.json entries to use schema | @pslits | 2026-04-03 | Open |
| Add schema example to PreToolUse hook template | @pslits | 2026-04-03 | Open |

---

## Outcome (complete after execution)

_To be filled after the change is made._
