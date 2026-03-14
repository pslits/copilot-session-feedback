# Frontmatter & Body Writing Guide

## Full File Structure

Every `SKILL.md` must be wrapped in a `` ```skill `` code fence. The YAML frontmatter and body content live inside that fence:

````
```skill
---
name: <skill-name>
description: "..."
---

# Skill Title

Body content here.
```
````

> **Note:** The outer `` ```skill `` / `` ``` `` code fence is required. Without it the agent runtime will not recognise the file as a skill.

## Frontmatter Template

```yaml
---
name: <skill-name>          # Must match directory name
description: "<What — third person, 1 sentence>. Use when <trigger conditions — 1–2 sentences>. Triggers on: <keyword list with synonyms>. Do not use for: <exclusion conditions> (if adjacent domains exist)."  # Max 1,024 chars, single line, quoted
# Optional fields — add only when needed:
# license: MIT
# compatibility: "Requires Python 3.10+"
# metadata:
#   version: "1.0.0"
#   author: "Name"
---
```

> **Note:** The VS Code SKILL.md parser does not support YAML multiline scalars (`>-`, `|`). Always write the `description` as a single-line quoted string.

## Description Rules

- Always third person ("Generates…", not "I help you…")
- Include "Use when:" with specific conditions
- Include "Triggers on:" with domain terms + synonyms
- Add "Do not use for:" when adjacent domains could false-trigger
- Use the full 1,024 chars when needed — short descriptions miss triggers

## Body Patterns

Choose patterns based on the task. Combine as needed.

| Pattern | When to Use |
|---------|-------------|
| Workflow checklist | Clear sequential steps with validation gates |
| Feedback loop | Run → Check → Fix → Repeat cycles |
| Strict template | Output must match exactly (file headers, naming) |
| Flexible template | Conventions with variation (test naming) |
| Input/output examples | Complex transformations where prose is ambiguous |
| Conditional workflow | Multi-variant tasks where context determines path |
| Domain vocabulary | Specialised terms requiring consistent usage |

## Body Writing Rules

1. Open with a one-line purpose statement.
2. Use imperative form ("Extract the data", not "The data should be extracted").
3. Reference bundled resources with explicit loading cues:
   - **Run:** `scripts/x.py <args>` — agent executes the script
   - **Read:** `[references/x.md](references/x.md)` — agent loads into context
   - **Copy:** `assets/template.html` — agent uses without reading
4. Target under 200 lines (hard max 500). If exceeded, move detail to `references/`.
5. Exclude what the agent already knows and "When to Use" sections (that belongs in the description).
