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

Every file type in this repo follows a specific header pattern. Apply these rules
when creating new files or reviewing generated output.

### GitHub Actions Workflows (`.github/workflows/*.yml`)

Start with `name:`, immediately followed by a one- or two-line comment that states
the trigger event and the workflow's purpose. No other preamble.

```yaml
name: HITL Escalation

# Runs hourly to detect SLA breaches on issues waiting for a human decision.
# Can also be triggered manually for immediate checks.
on:
```

### Shell Scripts (`.github/scripts/*.sh`)

Start with the shebang, then a comment block containing: filename and one-sentence
description, blank comment, Usage section, blank comment, Requirements line.

```bash
#!/usr/bin/env bash
# sync-labels.sh — create or update all HITL labels defined in docs/hitl/labels.md.
#
# Usage:
#   ./.github/scripts/sync-labels.sh [--repo OWNER/REPO] [--delete-unlisted]
#
# Requirements: gh CLI authenticated (gh auth login).
```

### PowerShell Scripts (`.github/scripts/*.ps1`)

Same structure as shell scripts but without a shebang. First line is
`# filename — description`.

```powershell
# sync-labels.ps1 — create or update all HITL labels defined in docs/hitl/labels.md.
#
# Usage:
#   .\..\scripts\sync-labels.ps1 [-Repo OWNER/REPO] [-DeleteUnlisted] [-DryRun]
#
# Requirements: gh CLI authenticated (gh auth login).
```

### Markdown Documents (`docs/**/*.md`, `sessions/**/*.md`)

Start with an H1 title (`#`), then a single plain-text sentence describing the
document's purpose. No frontmatter, no metadata block.

```markdown
# HITL Operator Runbook

This runbook is the primary reference for anyone involved in operating the
Human-in-the-Loop (HITL) intervention workflow.
```

### Agent, Skill, and Prompt Files (`*.agent.md`, `*.prompt.md`, `SKILL.md`)

Use YAML frontmatter with at minimum `name` and `description`. The `description`
field must be a single string that is rich enough for tool/agent routing (include
trigger phrases where relevant). No additional comment header outside the frontmatter.

```yaml
---
name: planner
description: Produces a verified, human-approved implementation plan ...
tools: [search, read, edit, vscode]
---
```

### GitHub Issue Templates (`.github/ISSUE_TEMPLATE/*.yml`)

Use the GitHub-parsed `name` and `description` fields as the header — no additional
comment block. Do not add YAML comments above these fields.

```yaml
name: HITL Intervention Request
description: Request a human-in-the-loop intervention gate for an agentic or automated action.
```

### Rules (apply to all file types)

- Never add "auto-generated — do not edit" notices. All files in this repo are
  meant to be maintained.
- Never add author, date, or version metadata to file headers. Git history is
  the authoritative record.
- Keep headers minimal: only what a reader needs to understand the file's purpose
  and how to use it before opening it fully.

---