---
name: audit
description: Audit instruction quality for contradictions and drift
agent: ask
---

Audit `copilot-instructions.md` for contradicted, orphaned, and redundant rules.

## Instructions
1. Count the rules in `copilot-instructions.md` and report the files included in the audit scope.
2. Skip the audit and report the rule count when the global rule count is below 15.
3. Run Pass 1 for contradictions by checking whether any rule in `copilot-instructions.md` conflicts with another rule in the same file.
4. Run Pass 2 for orphaned rules by checking whether the codebase contains evidence that each reviewed rule is still needed.
5. Run Pass 3 for redundancy only when the rule count is above 50 by checking whether two rules express the same constraint.
6. Record every flag in the audit report table with a category and a recommended action.
7. Cite `file:line` evidence for each flagged rule, or write `NONE` when no supporting evidence exists.
8. End with an audit summary that reports total rules reviewed and flags by category.

## Constraints
- Stay in read-only mode.
- Produce recommendations only.
- Audit `copilot-instructions.md` first.
- Audit scoped `*.instructions.md` files only when their rule count is above 15.
- Keep the critique fixed to the three allowed categories.

## Output Format
## Audit Scope
- Files: <list>
- Rule counts: <file -> count>

| Rule | Category | Evidence (file:line or NONE) | Recommended Action |
|---|---|---|---|
| <rule> | <Contradicted/Orphaned/Redundant> | <evidence> | <action> |

## Audit Summary
- Total rules reviewed: <count>
- Contradicted: <count>
- Orphaned: <count>
- Redundant: <count>
