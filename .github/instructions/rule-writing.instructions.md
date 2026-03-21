---
name: Rule Writing Checklist
description: Apply a six-check rule quality checklist when writing or editing instruction rules.
applyTo: "**/*.instructions.md,**/copilot-instructions.md"
---

# Rule Writing Checklist

**Instruction drift** is the process by which rules that were correct at time T become
incorrect or misleading by time T+N as the codebase, team, or tooling evolves (Ch. 6).
This checklist is the first line of defence against drift: every rule admitted through
this gate should be verifiable, scoped, and auditable so that the monthly drift-detection
cycle (run via `/audit`) can flag stale rules before they mislead the agent.

Use this checklist before saving any new or updated instruction rule.

## Checklist

1. Write each rule in positive, directive language that states the target behaviour. Reason: positive framing improves instruction fidelity.
2. End each rule with a `Reason:` clause that explains why the rule exists. Reason: explicit rationale helps the agent generalise in edge cases.
3. State one operational behaviour per rule so the agent can apply it without guessing. Reason: single-focus rules are easier to execute consistently.
4. Place workspace-wide rules in `copilot-instructions.md` and file-scoped rules in a matching `*.instructions.md` file. Reason: correct scope preserves context budget and improves injection accuracy.
5. Compare the candidate rule against existing rules in the same file and keep only the non-contradictory version. Reason: contradiction reduces compliance reliability.
6. Confirm the rule in at least one real session before treating it as stable guidance. Reason: tested rules outperform speculative rules.

## Session Limits

- Add at most two new rules in one session. Reason: small batches make validation and rollback easier.
- Keep each rule concrete enough to test in the next governed session. Reason: observable checks are required for reliable iteration.
