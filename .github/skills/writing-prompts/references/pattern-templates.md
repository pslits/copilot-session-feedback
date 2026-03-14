````markdown
# Prompt Pattern Templates

Frontmatter skeletons and body templates for each of the six prompt patterns.

**Variable syntax reminders:**
- `${input:variableName}` — user input (shows labelled input box)
- `${input:variableName:placeholder text}` — user input with placeholder hint
- `${file}`, `${fileBasename}`, `${fileBasenameNoExtension}`, `${fileDirname}` — current file (no user input)
- `${selection}` / `${selectedText}` — current editor selection (no user input)
- `${workspaceFolder}`, `${workspaceFolderBasename}` — workspace path (no user input)

All variables work only in the **body** (not in YAML frontmatter).

---

## Pattern 1: Research

**Frontmatter:**

```yaml
---
description: Research <topic> and produce a structured report
agent: ask
argument-hint: topic to research (e.g., authentication, caching)
tools:
  - search
  - readFile
  - listDirectory
---
```

**Body template:**

```markdown
Research ${input:topic} in this codebase and produce a structured report.

## Instructions

1. Search for all files related to ${input:topic}.
2. Read each relevant file fully before drawing conclusions.
3. Identify patterns, dependencies, and potential issues.

## Constraints

- Never speculate about code you have not opened.
- Do not suggest any changes — report only.
- Make independent tool calls in parallel.

## Output Format

### Summary
One paragraph overview.

### Findings
| File | Observation | Relevance |
|------|------------|-----------|
| …    | …          | High/Med/Low |

### Recommendations
Numbered list of actionable suggestions.
```

---

## Pattern 2: Generation

**Frontmatter:**

```yaml
---
description: Create a new <artefact> following project conventions
argument-hint: name for the new <artefact>
tools:
  - editFiles
  - createFile
  - runCommands
  - search
  - readFile
---
```

**Body template:**

```markdown
Follow the patterns in [example model](../../src/models/Example.ts)

Create a new <artefact> named ${input:name}.

## Instructions

1. Read the referenced example file fully.
2. Create the new file following the same patterns and conventions.
3. Add necessary imports and exports.
4. Run tests to verify the new file compiles.

## Constraints

- Only make changes that are directly requested.
- Follow existing naming conventions exactly.
- Do not refactor existing code.

## Output Format

Created files and their paths, followed by test results.
```

---

## Pattern 3: Review / Audit

**Frontmatter:**

```yaml
---
description: Review <scope> against <standard> and produce findings
agent: ask
argument-hint: file or directory to review (defaults to current file)
tools:
  - search
  - readFile
  - listDirectory
---
```

**Body template:**

```markdown
Current file: ${file}
Review ${input:target:file or directory, or leave blank for current file} against the project's coding standards.

## Instructions

1. Read all files in the specified scope fully.
2. Check each file against the checklist below.
3. Report findings with severity levels.

## Checklist

- [ ] Naming conventions followed
- [ ] Error handling present
- [ ] Tests exist for public interfaces
- [ ] No hardcoded values
- [ ] Documentation up to date

## Constraints

- Never speculate about code you have not opened.
- Do not modify any files — report only.

## Output Format

| # | File | Finding | Severity | Suggestion |
|---|------|---------|----------|------------|
| 1 | …    | …       | 🔴/🟠/🟡/🟢 | … |

### Summary
Total findings by severity. Top 3 priorities.
```

---

## Pattern 4: Workflow / Pipeline

**Frontmatter (plan-first variant — for complex tasks):**

```yaml
---
description: Plan and execute the <workflow> pipeline for <target>
argument-hint: target for the workflow
agent: plan
---
```

**Frontmatter (direct execution variant):**

```yaml
---
description: Execute the <workflow> pipeline end-to-end
argument-hint: target for the workflow
agent: agent
---
```

**Body template:**

```markdown
Execute the <workflow> pipeline for ${input:target}.

## Phase 1: Preparation
1. Read all relevant files.
2. Verify prerequisites are met.
3. **Gate:** Confirm all prerequisites pass before continuing.

## Phase 2: Implementation
1. Apply the required changes.
2. Run lint checks.
3. **Gate:** All lint checks pass before continuing.

## Phase 3: Verification
1. Run tests.
2. Verify no regressions.
3. Report results.

## Constraints

- Stop at any gate that fails and report the failure.
- Only make changes that are directly requested.
- Do not add features beyond what is described in this prompt.
```

---

## Pattern 5: Transformation

**Frontmatter:**

```yaml
---
description: Transform <source format> to <target format>
argument-hint: file or directory to transform
tools:
  - editFiles
  - search
  - readFile
  - runCommands
---
```

**Body template:**

```markdown
Transform ${input:target} from <source format> to <target format>.

## Instructions

1. Read all source files fully before making any changes.
2. Convert each file preserving behaviour and semantics.
3. Run tests after each conversion to verify no regressions.
4. Remove old format files only after tests pass.

## Constraints

- Preserve all existing behaviour — no functional changes.
- Only make changes that are directly requested.
- Make independent tool calls in parallel.

## Output Format

| Source File | Target File | Status |
|-------------|-------------|--------|
| …           | …           | ✅/❌   |

### Summary
Total converted, total failed, any manual follow-ups needed.
```

---

## Pattern 6: Capture / Documentation

**Frontmatter:**

```yaml
---
description: Capture session knowledge into a structured file
argument-hint: short description for the filename
agent: agent
tools:
  - editFiles
  - createFile
  - createDirectory
---
```

**Body template:**

```markdown
Capture the current session knowledge about ${input:topic} into a documentation file.

## Instructions

1. Review the conversation history for key decisions and findings.
2. Create a dated file: `docs/YYYY-MM-DD-${input:topic}.md`
3. Structure the content with clear headers.
4. Include context, decisions, rationale, and next steps.

## Constraints

- Only document what was actually discussed — don't invent details.
- Use present tense for current state, past tense for decisions made.

## Output Format

```markdown
# <Topic>

**Date:** YYYY-MM-DD
**Participants:** ...

## Context
Why this was discussed.

## Decisions
Numbered list of decisions with rationale.

## Next Steps
Actionable follow-ups.
```
```

---

## Composing Patterns

When a task spans multiple patterns:

1. **Sequential composition:** Chain two prompts manually (`/research-topic` → `/implement-topic`).
2. **Inline composition:** Combine two patterns in one prompt body — keep under 150 lines total.
3. **Naming convention:** Use consistent prefixes: `/research-*` → `/plan-*` → `/implement-*`.

````