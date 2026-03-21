---
name: Adoption Roadmap
description: Apply a maturity-gated adoption sequence when planning session-feedback system work. Prevents skipping phases and over-engineering. Apply to any plan in sessions/plans/.
applyTo: "sessions/plans/**"
---

# Progressive Adoption Roadmap

This instruction governs the sequencing of Copilot feedback system features.
Each phase maps to a maturity level with observable completion criteria that
must be met before proceeding. Time estimates are parenthetical guidance only.

> See also: [ADR-0014](../../docs/adr/0014-criteria-based-adoption-roadmap.md) —
> rationale for criteria-based phase gates.

## Level-Skip Guard

Do not implement Phase N+1 features until **all** Phase N completion criteria are marked ✓.
Reason: each level's features depend on the observability and stability established
by the prior level. Skipping creates fragile systems with undetectable failures.

## Adoption Phases

| Phase (time est.) | Maturity Level | Features | Entry criteria | Completion criteria (all must pass) |
|-------------------|---------------|----------|----------------|-------------------------------------|
| **Phase 1** (≈1 week) | Level 2 — Assisted | #2 `/compact`, #8 lenses instruction, #12 rule checklist, #15 routing tree, #19 `/verify`, #22 `/audit` | VS Code + GitHub Copilot installed and configured | ✓ `/verify` passes in a live session; ✓ ≥1 rule committed from a session finding; ✓ `/compact` produces all 5 sections; ✓ lenses instruction active in VS Code |
| **Phase 2** (≈1 week) | Level 3 — Automated | #1 stop hook, #18 security gate, #21 PostToolUse format, #9 `/research`, #13 token budget | Phase 1 completion criteria all ✓ | ✓ Stop hook operational (exits 0 on session end); ✓ ≥1 hook event logged to sessions.jsonl; ✓ security gate soft-blocks destructive commands; ✓ PostToolUse formats files without manual invocation |
| **Phase 3** (≈2 weeks) | Level 4 — Coordinated | #3 PreCompact, #4 PostCompact, #5 SessionStart, #10 `@researcher`, #16 `@planner`, #17 `@implementer`, #14 template library, #20 success metrics, #23 feedback debt | Phase 2 completion criteria all ✓; ≥ 4 sessions completed | ✓ RPI chain used end-to-end ≥1 time; ✓ `@implementer` executes a `@planner`-produced plan successfully; ✓ feedback debt tracker has ≥1 item in Done status |
| **Ongoing** | Level 4–5 — Team Scale | #6 SessionEnd, #7 notification, #11 feedback-analyser skill, #24 this document, #25 stop checklist injection | Phase 3 completion criteria all ✓ | ✓ corrections per session trending ↓ over 4 consecutive sessions |

## Friction Checkpoints

Before advancing each phase, verify the friction risks below are mitigated:

| Transition | Risk | Mitigation |
|------------|------|------------|
| Phase 1 → 2 | Session analysis feels manual; lenses add overhead | Lenses are a 4-row routing table — one pass per compact output; no iteration |
| Phase 2 → 3 | Hook latency adds perceptible delay | Keep all hook scripts < 500ms; test each hook independently before deployment |
| Phase 3 → Ongoing | Agent chain clicks add workflow steps | RPI agents are Phase 3 only after single-agent workflows are validated; do not introduce agents earlier |
| Ongoing | Metrics tracking becomes a chore | SessionEnd hook automates timestamp logging; only corrections-per-session requires a manual tally |

## Planning Rules

When producing a plan under `sessions/plans/**`:

1. Identify the current phase from the completion criteria above.
2. Scope the plan to features in the current or next phase only.
3. List the completion criteria for the current phase as the plan's acceptance tests.
4. Include the friction checkpoint for the transition being planned.
Reason: plans scoped beyond the current maturity level produce incomplete implementations
that fail at integration time.
