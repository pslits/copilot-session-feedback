# Copilot Instructions

<!-- # PRIORITY: HIGH: Commit header ≤50 chars, imperative verb (Add/Fix/Remove), Conventional Commits type(scope): summary -->
<!-- # PRIORITY: HIGH: Every AI-assisted commit must add footer: Co-Authored-By: GitHub Copilot <copilot@github.com> -->
<!-- # PRIORITY: HIGH: File headers by type — .py: shebang+one-line comment; .md: H1+sentence; agents/prompts/skills: YAML frontmatter -->
<!-- # PRIORITY: HIGH: Knowledge artifact caps — copilot-instructions.md≤200 lines; *.instructions.md≤100 lines; *.prompt.md≤150 lines -->
<!-- # PRIORITY: HIGH: Hooks exit 0=success, 2=soft-block; SessionEnd+PostCompact always exit 0 (must not block session) -->
<!-- # PRIORITY: HIGH: Always use terminal git for commit/push — never MCP git tools; MCP git bypasses the pre-tool-use security gate -->
<!-- # PRIORITY: HIGH: Never commit directly to main — create a feature branch and open a PR -->

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

### AI-Assisted Commits

If a commit was significantly produced with GitHub Copilot, add a trailer:

```
Co-Authored-By: GitHub Copilot <copilot@github.com>
```

This goes in the footer section, after any `Fixes #` or `Refs #` lines.

---
## File Header Conventions

Every file in this repository must begin with a header that declares its purpose. Apply the rule for the relevant file type below.

### GitHub Actions Workflows (`.github/workflows/*.yml`)

After `name: <Title>`, leave one blank line, then add one or more `#` comment lines describing what the workflow does and when it runs. The `on:` key follows immediately.

```yaml
name: HITL Gate

# Processes slash-commands posted as issue comments.
# Only runs on issues (not pull requests) that carry a state:* label.
on:
  issue_comment:
    types: [created]
```

### Shell Scripts (`.github/scripts/*.sh`)

Start with the shebang, then a comment block: filename and one-sentence description, blank comment, Usage section, blank comment, Requirements line.

```bash
#!/usr/bin/env bash
# sync-labels.sh — create or update all HITL labels defined in docs/hitl/labels.md.
#
# Usage:
#   ./.github/scripts/sync-labels.sh [--repo OWNER/REPO] [--delete-unlisted]
#
# Requirements: gh CLI authenticated (gh auth login).
```

### Python Scripts (`*.py`)

Start with the `#!/usr/bin/env python3` shebang, followed immediately by a `# <filename> — <one-sentence description>` comment.

```python
#!/usr/bin/env python3
# session-start.py — inject project metadata into session context.
```

### PowerShell Scripts (`*.ps1`)

Start with a `# <filename> — <one-sentence description>` comment (no shebang required).

```powershell
# sync-labels.ps1 — create or update all HITL labels defined in docs/hitl/labels.md.
#
# Usage:
#   .\..\scripts\sync-labels.ps1 [-Repo OWNER/REPO] [-DeleteUnlisted] [-DryRun]
#
# Requirements: gh CLI authenticated (gh auth login).
```

### Markdown Documents (`*.md`)

Start with a top-level ATX heading (`# Title`) as the very first line, then a single plain-text sentence describing the document's purpose.

```markdown
# HITL Operator Runbook

This runbook is the primary reference for anyone involved in operating the
Human-in-the-Loop (HITL) intervention workflow.
```

### Agent, Skill, and Prompt Files (`*.agent.md`, `*.prompt.md`, `SKILL.md`)

Begin with a YAML frontmatter block (`---`) containing at minimum `name` and `description` fields. The description must be rich enough for tool/agent routing. No comment header outside the frontmatter.

```yaml
---
name: planner
description: Produces a verified, human-approved implementation plan using the
  Planning, Reflection, Goal Setting, and Human-in-the-Loop patterns.
---
```

---

## Git Operations

Rules:
- **Always use terminal `git`** for commit and push. MCP git tools (`mcp_gitkraken_git_add_or_commit`, `mcp_gitkraken_git_push`, etc.) bypass the pre-tool-use security gate and are hard-blocked by it.
- **Never commit directly to `main`.** Create a feature branch, commit there, and open a PR — even for small changes.

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
