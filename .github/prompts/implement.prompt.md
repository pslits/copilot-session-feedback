---
description: Execute an approved plan using the implementer agent
argument-hint: path to approved plan (e.g., sessions/plans/2026-03-15-add-hooks.md)
agent: implementer
---

Execute the following approved plan:

Plan file: ${input:planPath}

## Instructions

1. Read the plan file fully before taking any action.
2. Follow the implementer's six-step procedure — intake, execute, reflect, checkpoint, verify, finalise.
3. Implement one step at a time; mark each complete only after its success criteria pass.
4. Pause for human approval on any scope or risk change.

## Constraints

- Do not implement without an approved plan file.
- Do not modify files outside the plan's approved scope.
- Never claim success without running the specified checks.
- Prefer minimal, reversible changes over broad refactors.

## Output Format

Provide the implementer's standard output:

### Execution Baseline
- Plan file, approved scope, current phase, first step, expected checks.

### Step Results
| Phase | Step | Files Changed | Checks Run | Result | Notes |

### Final Report
- What changed, validation outcomes, deviations from plan, open follow-ups.
