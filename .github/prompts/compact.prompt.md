---
name: compact
description: Capture session memory into five compact sections
tools: [read, search]
---

Create a compact session summary that preserves the session's reusable knowledge.

## Instructions
1. Read the current chat context and any relevant workspace files needed to recover the session state.
2. Produce exactly these five sections in this order:
   - `## Session Decisions`
   - `## Rules to Promote`
   - `## What Was Tried`
   - `## Workflow Steps Discovered`
   - `## Corrections`
3. In `## Session Decisions`, list the decisions made this session and the reason each decision was made.
4. In `## Rules to Promote`, list candidate rules that are not yet captured in project instructions using the format `Rule: <text> Reason: <why>`.
5. In `## What Was Tried`, use a table with the columns `| Attempt | Outcome | Reason for abandonment |`.
6. In `## Workflow Steps Discovered`, use a numbered list of reusable workflows found during the session.
7. In `## Corrections`, use a table with the columns `| Correction | Recurrence count | Source lens (1–4) | Promotion candidate (Y/N) |`.
   Source lens values: 1=Recurring Correction, 2=Domain Vocabulary, 3=Workflow Friction, 4=Quality Guardrail.
8. Prefer bullets and tables over prose paragraphs so the output stays compact and reviewable.

## Constraints
- Keep the total output under 400 lines.
- Keep each section under 80 lines.
- Use only the allowed read-only tools.
- Preserve only session knowledge that can be reused in a later session.
- Leave the workspace unchanged.

## Output Format
## Session Decisions
- <decision> — <reason>

## Rules to Promote
- Rule: <text> Reason: <why>

## What Was Tried
| Attempt | Outcome | Reason for abandonment |
|---|---|---|
| <attempt> | <outcome> | <reason> |

## Workflow Steps Discovered
1. <workflow step>

## Corrections
| Correction | Recurrence count | Source lens (1–4) | Promotion candidate (Y/N) |
|---|---|---|---|
| <correction> | <count> | <lens> | <Y/N> |
