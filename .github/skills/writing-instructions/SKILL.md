```skill
---
name: writing-instructions
description: "Creates, updates, and corrects GitHub Copilot instruction files — copilot-instructions.md (global, always-on) and *.instructions.md (conditional, file-scoped) — for use in VS Code Chat and agent mode. Covers the full instruction lifecycle: routing decisions (global vs conditional vs other surfaces), frontmatter fields (name, description, applyTo, excludeAgent), positive rule framing via the trajectory principle, Reason: annotations, applyTo glob engineering, context budget management, and validation. Use when: writing a new instruction file, adding rules to an existing instruction file, updating or improving instructions, correcting a rule that isn't working, scoping an instruction to specific file types, migrating .cursorrules or CLAUDE.md rules into Copilot format, or auditing an instruction file for anti-patterns. Triggers on: 'create instructions', 'write instructions', 'new instruction', 'update instructions', 'fix instructions', 'instruction file', 'copilot-instructions', 'instructions.md', 'instruction rule', 'applyTo glob', 'instruction writer', 'add rule', 'write rule'. Do not use for: writing skills (SKILL.md), prompt files (*.prompt.md), custom agents (.agent.md), hooks, or MCP servers."
metadata:
  version: "1.0.0"
  author: "Paul Slits"
---

# Writing Instructions

Create, update, or correct GitHub Copilot instruction files (`copilot-instructions.md` and `*.instructions.md`).

## Mode Selection

Determine the mode from the user's request:

| Signal | Mode | Section |
|--------|------|---------|
| "Create an instruction file", "write instructions", "new rule", convert a correction | **Create** | Create Mode below |
| "Update", "improve", "add a rule", "tighten", "refactor" | **Update** | Update Mode below |
| "Fix", "correct", "rule not working", "instruction ignored" | **Correct** | Correct Mode below |

---

## Create Mode (5-Step Process)

### Step 1: Routing Check

Confirm an instruction file is the right surface before writing anything:

| Question | Answer → Surface |
|----------|-----------------|
| Is it true for every request in this workspace? | Yes → `copilot-instructions.md` |
| Does it only apply when certain file types are open? | Yes → `*.instructions.md` with `applyTo` |
| Is it a step-by-step procedure for producing something? | Yes → Skill (`SKILL.md`) |
| Is it a reusable task template invoked by name? | Yes → Prompt file (`*.prompt.md`) |
| Is it a persona definition with custom tool config? | Yes → Custom agent (`.agent.md`) |

If the answer is **not** an instruction file, tell the user which surface to use and stop.

When the answer is an instruction file, proceed to Step 2.

### Step 2: Decide Scope — Global or Conditional

**Global (`copilot-instructions.md`)** — use when the rule:
- Applies to every file in the workspace regardless of type or layer
- Defines project-wide naming conventions, architectural constraints, domain vocabulary, or toolchain facts

**Conditional (`*.instructions.md`)** — use when the rule:
- Only matters for specific file types, directories, or domain layers
- Would waste tokens on unrelated files if placed globally

Conditional files live in `.github/instructions/<name>.instructions.md`.

### Step 3: Write the Frontmatter (conditional files only)

Global `copilot-instructions.md` has no frontmatter — pure Markdown only.

For `*.instructions.md`, write YAML frontmatter using these fields:

```yaml
---
name: Human-Readable Label          # Optional — shown in picker; cosmetic only
description: >-                     # Optional — drives semantic auto-injection
  One precise sentence describing when this instruction applies.
applyTo: '**/pattern/**'            # Optional — glob-based auto-injection
excludeAgent: 'code-review'         # Optional — 'code-review' or 'coding-agent'
---
```

**Provide both `applyTo` AND `description` for any file that should auto-inject.** The glob provides deterministic matching; the description provides semantic backup.

Common `applyTo` patterns:

| Scope | Pattern |
|-------|---------|
| Test files | `**/*.test.*` or `**/*.spec.*` |
| Domain models | `**/models/**` or `**/ValueObject/**` |
| React components | `**/components/**/*.tsx` |
| TypeScript + TSX | `**/*.{ts,tsx}` |
| API controllers | `**/controllers/**` |
| Documentation | `**/*.md` |
| Infrastructure layer | `**/Infrastructure/**` |

For code-review–only instructions, set `excludeAgent: "coding-agent"`.
For coding-only instructions, set `excludeAgent: "code-review"`.

### Step 4: Write the Rules

Apply these rules to every instruction statement before committing it:

**The Trajectory Principle — never describe prohibited behavior.**

Describing what NOT to do statistically increases the model reproducing that behavior. Always describe the desired output.

| BAD (prohibition) | GOOD (positive framing) |
|-------------------|------------------------|
| "Don't use setters." | "Properties are `private`; all state is set through the constructor. Reason: immutability." |
| "Never put validation in controllers." | "All input validation belongs in model constructors. Controllers trust the models they receive. Reason: fail-fast at the boundary." |
| "Avoid `var`." | "Use `const` for all bindings; use `let` only when reassignment is required. Reason: signals intent to the reader." |

**Rule checklist — apply to every bullet before committing:**

- [ ] Positively framed (describes desired behavior, not prohibited behavior)
- [ ] Includes `Reason: …` annotation so the agent applies the rule correctly in edge cases
- [ ] Specific enough to operationalise without guessing
- [ ] One constraint per bullet (compound rules cause the agent to miss the second clause)
- [ ] Uses strong modals ("always", "use", "must") not weak ones ("should", "could", "may")

**Rule formula:**

```
- Use X for Y. Reason: Z.
- X always includes Y. Reason: Z.
- When X, prefer Y over Z. Reason: Z.
- Name X as `pattern`. Reason: Z.
```

Add a short code block example only when prose alone would be ambiguous. Show only the positive pattern in the rule text; use `// Preferred:` / `// Instead of:` labels in the code block.

### Step 5: Validate

**Structural checks:**

- [ ] Conditional file: frontmatter is valid YAML, all used fields are spelled correctly
- [ ] `applyTo` glob tested against a file that should match (appears in Chat "References" section)
- [ ] `applyTo` glob tested against a file that should NOT match (absent from "References" section)
- [ ] Global file stays under 200 lines (~3,000 tokens)
- [ ] Each conditional file stays under 100 lines
- [ ] No rule uses negative framing ("don't", "never", "avoid", "no")
- [ ] No rule lacks a `Reason:` annotation
- [ ] No rule duplicates what a linter already enforces automatically

**Functional check:**

Open a cold Chat session. Ask the agent to produce output that the new rule governs. Confirm the agent follows the rule on the first attempt without prompting.

---

## Update Mode

1. Read the existing file and identify what is being changed or added.
2. Route new content: confirm it belongs in this instruction file (Step 1 routing check).
3. Check the rule against the rule checklist (Step 4 above).
4. Check the context budget: if the file is approaching 200 lines (global) or 100 lines (conditional), consider splitting content into a new scoped conditional file.
5. Test the `applyTo` glob if changed (Step 5 structural checks).
6. Run the functional check: verify the updated rule is followed in a cold Chat session.

---

## Correct Mode

Use when a rule exists but is not being followed, or when instructions behave unexpectedly.

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| Rule is ignored completely | Negative framing (trajectory principle) | Rewrite as positive imperative |
| Rule followed inconsistently | No `Reason:` annotation | Add `Reason: …` so the agent generalises correctly |
| Instruction file not loading | `applyTo` glob doesn't match open file | Test glob; broaden or fix pattern |
| Instruction not loading | File name missing `.instructions.md` suffix | Rename file |
| Code review ignores instructions | File exceeds 4,000-character hard cap | Move lower-priority rules to end; trim file |
| Two rules contradict each other | Overlapping instruction files govern same concern | Remove the rule from the lower-priority file |
| Rule applies to unintended files | `applyTo` glob too broad | Narrow glob; test negative case |
| Too many tokens; agent "forgets" earlier rules | Global file too large | Split into scoped conditional files with `applyTo` |
| Conditional file never fires | Missing both `applyTo` and `description` | Add `applyTo` glob and/or `description` to frontmatter |

**Diagnosis tools:**
- **"References" section** in Chat response bottom — lists every instruction file that loaded.
- **`/instructions` in Chat** — opens the Configure Instructions picker; shows all discovered files and their status.
- **Diagnostics view** — right-click a `.instructions.md` file → "Diagnostics"; shows frontmatter parse errors and glob issues.

---

## Context Budget Reference

| File | Recommended max | Hard cap (code review) |
|------|----------------|----------------------|
| `copilot-instructions.md` | 200 lines | 4,000 characters |
| Single `*.instructions.md` | 100 lines | 4,000 characters |

Check character count before committing:

```powershell
(Get-Content .github/copilot-instructions.md -Raw).Length
```

---

## Deep Reference

For comprehensive guidance, read specific sections from [references/instruction-writer-guide.md](references/instruction-writer-guide.md):

- Routing decision matrix and visual tree → §2 When to Write Instructions
- Instruction anatomy and frontmatter fields → §3 Anatomy of Instruction Files
- Global instruction content categories → §4 Global Instructions Deep Dive
- Conditional instruction mechanics → §5 Conditional Instructions Deep Dive
- Rule writing — trajectory principle, reasoning, specificity → §6 Writing Effective Rule Statements
- `applyTo` glob syntax and testing → §7 `applyTo` Glob Engineering
- Recommended section structures → §8 Content Categories and Organisational Patterns
- Token budget management → §9 Context Budget Management
- File references (`#file:`) in instructions → §10 File References in Instructions
- Priority, accumulation, conflict resolution → §11 Priority, Loading Behavior, and Accumulation
- Cross-tool compatibility (Cursor, Claude Code) → §12 Cross-Tool Compatibility
- Anti-patterns gallery → §14 Anti-Patterns Gallery
```
