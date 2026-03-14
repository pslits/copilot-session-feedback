---
description: Create an implementation plan using the planner agent
argument-hint: task to plan (e.g., refactor auth middleware, add export retries)
agent: planner
---

Create a planning artifact for the following task:

Task: ${input:task}

## Instructions
1. Use the planner workflow to analyze the codebase and produce a phased implementation plan.
2. Save the plan in `sessions/plans/YYYY-MM-DD-<slug>.md`.
3. Present the saved plan path and ask for explicit approval before any implementation handoff.

## Constraints
- Planning only; do not implement source code changes.
- Read all relevant files fully before producing the final plan.
- Keep scope strictly to the requested task.

## Output Format
### Plan Path
- path: <relative-path>

### Plan Summary
- objective: <one sentence>
- phases: <count>
- key risks: <comma-separated list>

### Approval Gate
- question: I have saved the plan to `sessions/plans/<filename>.md`. Does this plan match your intent? Approve to hand off to the implementer, or tell me what to change.
