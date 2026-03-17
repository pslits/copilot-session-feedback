## Commit Message Guidelines

Keep commit messages clear, consistent and machine-friendly so changelogs and code review history are useful.

Recommended format (based on Conventional Commits, adapted for this repo):

- Header: type(scope?): short summary
- Blank line
- Body: more detailed explanation (wrap at ~72 chars)
- Blank line
- Footer: references (e.g., issue numbers, breaking changes)

Rules:
- Use imperative, present-tense verb in the header ("Add", "Fix", "Remove").
- Keep the header <= 50 characters when possible.
- Use a scope when it helps clarify the area changed, e.g., `ValueObject`, `Tests`, `CI`.
- Limit body lines to ~72 characters.
- Reference issue or PR numbers in the footer using `Fixes #123` or `Refs #123`.
- Mark breaking changes in the footer using `BREAKING CHANGE: description`.

Common types we use:
- feat: a new feature
- fix: a bug fix
- docs: changes to documentation
- style: formatting, missing semicolons, whitespace (no code change)
- refactor: code change that neither fixes a bug nor adds a feature
- test: adding or updating tests
- chore: tooling, build processes, package updates, ci
- ci: changes to CI configuration

Examples:

- feat(ValueObject): add RepositoryIdentity value object

   Introduce a new immutable value object to represent repository identity.
   Includes validation and unit tests.

- fix(Email): validate email addresses with stricter regex

   Fixes an edge case where emails with plus addressing were rejected.

- docs: update CONTRIBUTING.md with testing instructions

Prefixing with ticket IDs (e.g., `ABC-123: ...`) is optional—use it when your workflow links commits to issue trackers.

When in doubt, write a short, descriptive header and a body that explains the why, not only the what.

---

## File Header Conventions

Every file in this repository must begin with a header that declares its purpose. Apply the rule for the relevant file type below.

### GitHub Actions Workflows (`.github/workflows/*.yml`)

After `name: <Title>`, leave one blank line, then add one or more `#` comment lines describing what the workflow does and when it runs. The `on:` key follows immediately after the comment block.

```yaml
name: HITL Gate

# Processes slash-commands posted as issue comments.
# Only runs on issues (not pull requests) that carry a state:* label.
on:
  issue_comment:
    types: [created]
```

### Python Scripts (`*.py`)

Start with the `#!/usr/bin/env python3` shebang, followed immediately by a `# <filename> — <one-sentence description>` comment.

```python
#!/usr/bin/env python3
# sync-labels.py — create or update all HITL labels defined in docs/hitl/labels.md.
```

### PowerShell Scripts (`*.ps1`)

Start with a `# <filename> — <one-sentence description>` comment (no shebang required).

```powershell
# sync-labels.ps1 — create or update all HITL labels defined in docs/hitl/labels.md.
```

### Markdown Documents (`*.md`)

Start with a top-level ATX heading (`# Title`) as the very first line.

```markdown
# HITL Label Taxonomy
```

### Agent, Skill, and Prompt Frontmatter Files (`.agent.md`, `SKILL.md`, `.prompt.md`)

Begin with a YAML frontmatter block (`---`) containing at minimum `name` and `description` fields.

```yaml
---
name: planner
description: Produces a verified, human-approved implementation plan using the
  Planning, Reflection, Goal Setting, and Human-in-the-Loop patterns.
---
```

---

## Knowledge Artifact Size Budgets

Rule: Check any knowledge artifact's line count against the caps below before writing; if it
would exceed the cap, apply the overflow action instead of truncating.
Reason: Oversized instruction files silently drop later rules as the context window fills —
splitting by domain is cheaper than debugging forgotten rules.

| Surface | Hard cap | If exceeded |
|---------|----------|-------------|
| `copilot-instructions.md` | 200 lines | Split domain-specific rules into `*.instructions.md` with `applyTo` |
| `*.instructions.md` | 100 lines per file | Create a second scoped file for the same domain |
| `SKILL.md` | 500 lines | Split into core `SKILL.md` + bundled reference documents in `references/` |
| Hook `additionalContext` | 200 tokens | Select only the 3–5 highest-priority rules; summarise to fit |
| `*.prompt.md` body | 150 lines | Extract reusable sections into a skill reference |
