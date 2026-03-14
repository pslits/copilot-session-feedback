# Plan: File Header Conventions

Date: 2026-03-14
Status: Implemented
Author: planner

## Objective

Codify existing implicit file-header conventions into `copilot-instructions.md`
so all future contributors and agents produce consistent headers, then retrofit
the one existing file that deviates from the pattern.

## Scope

- `.github/copilot-instructions.md` — add "File Header Conventions" section
- `.github/workflows/hitl-intake.yml` — add missing description comment

## Out of Scope

All other generated files already conform; no changes needed to them.

---

### Phase A — Document the conventions
Precondition: `copilot-instructions.md` is the only governance document; no
existing header rules exist.

- [x] Step 1 — Append a "File Header Conventions" section to
  `.github/copilot-instructions.md` covering five file types:
  workflows, shell scripts, PowerShell scripts, Markdown docs,
  and agent/skill/prompt frontmatter files.
  Success: section is present; each type has a one-sentence rule
  and a minimal example drawn from the existing files.

Phase A done when: the new section is saved and parseable.

---

### Phase B — Retrofit the deviant file
Precondition: Phase A complete; conventions are documented.

- [x] Step 1 — Add a 2-line description comment directly below `name:` in
  `.github/workflows/hitl-intake.yml` (after line 1), matching the pattern
  used by `hitl-gate.yml`, `hitl-escalation.yml`, etc.
  Success: `hitl-intake.yml` lines 1–4 contain name + comment; no functional
  YAML changed.

Phase B done when: `hitl-intake.yml` header matches the workflow convention.

---

## Key Risks

- Over-prescribing the rule could conflict with GitHub Actions' own YAML
  schema expectations → mitigated by keeping the rule to comment lines only,
  never inside parsed keys.
- Touching `hitl-intake.yml` after it is live could create a noisy commit →
  mitigated by the change being a pure comment addition with no logic impact.
