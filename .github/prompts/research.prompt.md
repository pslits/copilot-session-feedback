---
name: research
description: Read-only codebase research to map the workspace before making changes. Use at the start of any RPI workflow before planning or implementing.
# REVIEW(R-10): 'agent: agent' activates generic agent mode, not @researcher.
# If the intent is always to invoke @researcher, use a custom agent name value
# (if VS Code supports it for the installed version) or document that this prompt
# must be used with @researcher already active. The current form may route to
# whichever agent is currently selected, producing non-deterministic invocations.
agent: agent
tools: [read, search]
---

Perform a structured, read-only research pass across the workspace to map it before any
changes are made. Do not write, edit, or delete any files during this research.

## Instructions

1. Clarify the research scope from the provided input: `${input:scope}`.
2. List all top-level directories and note the purpose of each.
3. For each area relevant to the scope, read the key files and extract:
   - What the file/module does
   - What it depends on
   - Any constraints or conventions it enforces
4. Search for patterns, naming conventions, or recurring structures in the codebase that
   would affect the scoped work.
5. Note any gaps, missing files, or inconsistencies relevant to the scope.
6. Produce the structured output below.

## Constraints

- Use read-only tools only. Never call `editFiles`, `createFile`, or terminal commands.
- Read files completely rather than guessing from their names.
- Cite every finding with `file:line` references.
- Do not proceed to planning or implementation — this step ends with the handoff table.

## Output Format

### Research Scope
- Scope: <the input scope as understood>
- Files inspected: <count>

### Workspace Map
| Directory | Purpose |
|-----------|---------|
| <dir> | <purpose> |

### Findings by Area
For each relevant area:

#### <Area Name>
- **Key files:** `<path>` (`<purpose>`)
- **Constraints:** <any enforced rules or conventions>
- **Gaps / inconsistencies:** <anything missing or inconsistent>

### Handoff to Planner
| # | Finding | Relevant files | Suggested surface | Priority |
|---|---------|---------------|-------------------|----------|
| 1 | <finding> | `<file:line>` | <surface> | P0/P1/P2/P3 |
