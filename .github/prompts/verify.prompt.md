---
name: verify
description: Verify all six knowledge surfaces are loaded
agent: ask
---

Review the workspace and report whether each knowledge surface is present and verifiable.

## Instructions
1. Check these six surfaces in order: `copilot-instructions.md`, scoped `*.instructions.md`, `*.prompt.md`, `*.agent.md`, `SKILL.md`, and hooks.
2. For each surface, identify the most relevant file in the workspace and state the concrete check that would confirm the surface is working.
3. Mark the row `✓` only when the file is present and the check is observable from the workspace or a documented editor behaviour.
4. Mark the row `✗` when the file is absent, incomplete, or cannot be verified from the available evidence.
5. Fill the `Action if ✗` column with the next concrete recovery step for that surface.
6. Keep the assessment binary and evidence-based rather than subjective.

## Constraints
- Stay in read-only mode.
- Leave the workspace unchanged.
- Report exactly one row per surface.
- Use specific checks such as file presence, matching location, or documented picker visibility.
- Record the reason in the check text when a surface cannot be verified directly.

## Output Format
| Surface | File | Check | Status (✓/✗) | Action if ✗ |
|---|---|---|---|---|
| `copilot-instructions.md` | <file> | <observable check> | <✓/✗> | <action> |
| `*.instructions.md` | <file> | <observable check> | <✓/✗> | <action> |
| `*.prompt.md` | <file> | <observable check> | <✓/✗> | <action> |
| `*.agent.md` | <file> | <observable check> | <✓/✗> | <action> |
| `SKILL.md` | <file> | <observable check> | <✓/✗> | <action> |
| Hook | <file> | <observable check> | <✓/✗> | <action> |
