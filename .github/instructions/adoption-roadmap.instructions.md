---
name: Adoption Roadmap
description: Apply a maturity-gated adoption sequence when planning session-feedback system work. Prevents skipping phases and over-engineering. Apply to any plan in sessions/plans/.
applyTo: "sessions/plans/**"
---

# Progressive Adoption Roadmap

This instruction governs the sequencing of Copilot feedback system features.
Each week maps to a maturity level with explicit entry and exit criteria.

## Level-Skip Guard

Do not implement Week N+1 features until **all** Week N exit criteria are marked ✓.
Reason: each level's features depend on the observability and stability established
by the prior level. Skipping creates fragile systems with undetectable failures.

## Adoption Phases

| Week | Maturity Level | Features | Entry criteria | Exit criteria (all must pass) |
|------|---------------|----------|----------------|-------------------------------|
| **1** | Level 2 — Assisted | #2 `/compact`, #8 lenses instruction, #12 rule checklist, #15 routing tree, #19 `/verify`, #22 `/audit` | VS Code + GitHub Copilot installed and configured | ✓ `/compact` produces all 5 sections; ✓ lenses instruction active in VS Code; ✓ `/verify` shows all surfaces loaded |
| **2** | Level 3 — Automated | #1 stop hook, #18 security gate, #21 PostToolUse format, #9 `/research`, #13 token budget | Week 1 exit criteria all ✓ | ✓ stop hook archives transcripts on session close; ✓ security gate soft-blocks destructive commands; ✓ PostToolUse formats files without manual invocation |
| **4** | Level 4 — Coordinated | #3 PreCompact, #4 PostCompact, #5 SessionStart, #10 `@researcher`, #16 `@planner`, #17 `@implementer`, #14 template library, #20 success metrics, #23 feedback debt | Week 2 exit criteria all ✓; ≥ 4 sessions completed | ✓ `@researcher` → `@planner` handoff produces a plan without re-reading research; ✓ feedback debt tracker has ≥ 1 item in Done status |
| **Ongoing** | Level 4–5 — Team Scale | #6 SessionEnd, #7 notification, #11 feedback-analyser skill, #24 this document, #25 stop checklist injection | Week 4 exit criteria all ✓ | ✓ corrections per session trending ↓ over 4 consecutive weeks |

## Friction Checkpoints

Before advancing each week, verify the friction risks below are mitigated:

| Week | Risk | Mitigation |
|------|------|------------|
| 1 → 2 | Session analysis feels manual; lenses add overhead | Lenses are a 4-row routing table — one pass per compact output; no iteration |
| 2 → 4 | Hook latency adds perceptible delay | Keep all hook scripts < 500ms; test each hook independently before deployment |
| 4 → Ongoing | Agent chain clicks add workflow steps | RPI agents are Week 4 only after single-agent workflows are validated; do not introduce agents earlier |
| Ongoing | Metrics tracking becomes a chore | SessionEnd hook automates timestamp logging; only corrections-per-session requires a manual tally |

## Planning Rules

When producing a plan under `sessions/plans/**`:

1. Identify the current maturity level from the exit criteria above.
2. Scope the plan to features in the current or next level only.
3. List the exit criteria for the current level as the plan's acceptance tests.
4. Include the friction checkpoint for the transition being planned.
Reason: plans scoped beyond the current maturity level produce incomplete implementations
that fail at integration time.
