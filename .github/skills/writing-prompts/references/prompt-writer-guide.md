# Prompt Writer Reference Guide

Authoritative reference for writing `*.prompt.md` files in GitHub Copilot VS Code.
Read the section you need — each section is self-contained.

---

## Routing

A prompt file is the right surface when the task is:

1. Repeatable — you've typed these instructions more than twice.
2. Multi-step — it needs numbered steps, not a single sentence.
3. Parameterised — one or two inputs change per invocation.
4. Team-useful — others benefit from the same workflow.

**Quick surface comparison:**

| Surface | Use When |
|---------|----------|
| `copilot-instructions.md` | Always-on rules (coding standards, naming) |
| `*.instructions.md` | File-type-specific rules (`applyTo` scope) |
| **`*.prompt.md`** | **On-demand repeatable task template** |
| `*.agent.md` | Persistent persona, handoffs, tool/model isolation |
| `SKILL.md` | Portable expertise, bundled resources, cross-tool |
| Hook JSON | Deterministic lifecycle actions |

**Do NOT write a prompt when:**
- It is a single sentence — type in chat directly.
- It needs a specialised persona with handoffs — use `*.agent.md`.
- It needs bundled scripts or cross-tool portability — use `SKILL.md`.
- It is always-on coding guidance — use `copilot-instructions.md`.

---

## Frontmatter Template

```yaml
---
name: optional-override           # Overrides the slash command name from filename
description: Verb + what + output # Required. Under ~80 chars. Verb-first. Shown in / picker.
argument-hint: topic to research (e.g., authentication, caching)  # Pairs with ${input:}
agent: ask                        # ask | agent | plan | <custom-agent-name>
model: claude-sonnet-4            # Optional. String or prioritised array.
tools:                            # Optional. Omit for all tools. List to restrict.
  - search
  - readFile
  - listDirectory
---
```

### Field Reference

| Field | Required | Default | Notes |
|-------|----------|---------|-------|
| `name` | No | Filename (minus `.prompt.md`) | Override the slash command name |
| `description` | **Yes** | — | Shown in `/` picker — only thing users see before invoking |
| `argument-hint` | No | — | Placeholder after `/command` — pair with primary `${input:}` |
| `agent` | No | `agent` | `ask` = read-only; `agent` = full tools; `plan` = plan-first; custom name = delegate |
| `model` | No | User default | String or `[string, string]` priority array for fallback |
| `tools` | No | All tools | **Restriction only** — omit for full access; list to restrict |

### `description` Formula

```
<Verb> <what> <output or benefit>
```

- Start with a verb: "Research…", "Create…", "Review…", "Generate…", "Compact…"
- Keep under ~80 characters — truncated if longer
- State the deliverable: "…and produce a structured report"
- Bad: `"Does stuff with code"` → Good: `"Review code for security issues and produce a findings table"`

### `agent` Mode Guide

| Mode | Behaviour | Use For |
|------|-----------|---------|
| `ask` | Conversational — no file edits or tool calls | Research, review, audit |
| `agent` (default) | Full agent mode with all tools | Generation, transformation, implementation |
| `plan` | Generates a plan before taking action | Complex multi-step tasks where upfront planning matters |
| `<custom-name>` | Delegates to a named `.agent.md` — applies its persona, tools, model | Reusing an agent's specialisation |

### `tools` List — Common Patterns

| Use Case | Example |
|----------|---------|
| Read-only research | `[search, readFile, listDirectory]` |
| Code generation | `[editFiles, createFile, runCommands, search, readFile]` |
| Pure conversation | `[]` |
| Full access (default) | *(omit `tools` entirely)* |

**Tool list priority chain** (when `agent` field references a custom agent):
1. Tools in the **prompt file** (highest priority)
2. Tools from the **referenced custom agent**
3. **Default tools** for the selected agent

128-tool limit per request — be selective with MCP server wildcards (`<server>/*`).

---

## Body — Four-Part Structure

```markdown
[File references at the top — front-load context]

Task statement incorporating ${input:variable}.

## Instructions
1. First step — imperative verb.
2. Second step.
3. Third step.

## Constraints
- Scope boundaries.
- What NOT to do (negative framing is fine here).

## Output Format
### Section Heading
- item: description
```

**Rules:**

1. Imperative mood: "Search for…" not "It would be good if you searched for…"
2. Be specific: name the exact files, directories, and tools to use
3. Frame task statements positively ("Read all mentioned files") — reserve negation for Constraints
4. Explicitly state act vs. advise: "Implement changes rather than suggesting" or "Report findings without modifying files"
5. Place file references at the **top** — front-load context before instructions (Anthropic: queries at end improve quality 30%)
6. Variables work in the **body only** — never in frontmatter
7. Keep body under 80 lines (soft limit); 80–150 for complex workflows; split or upgrade to skill above 150

**Standard guard clauses — include as appropriate:**

| Clause | Body Text |
|--------|-----------|
| Anti-overengineering | `Only make changes that are directly requested. Do not add features, refactor code, or improve beyond what was asked.` |
| Anti-hallucination | `Never speculate about code you have not opened. Read relevant files FULLY before answering.` |
| Anti-drift | `Do not add features or scope beyond what is described in this prompt.` |
| Parallelism | `When calling multiple tools with no dependencies between them, make all calls in parallel.` |
| Read-first | `Read all mentioned files FULLY before acting or spawning sub-tasks.` |
| Chainability | `## Next Step\nTo create an implementation plan, run \`/plan\`.` |

**Output format specification:**
- Always include when the prompt produces a deliverable
- Use headers, tables, and code blocks to define structure precisely
- Provide a template with `| ... |` placeholders for tables
- In the final instruction step: "Replace all example rows with real data. Include every section even if empty (state 'None found')."

---

## Context Injection

### File References — Markdown Link Syntax (Canonical)

```markdown
Follow the patterns in [Money model](../../src/models/Money.ts)
and the [Money tests](../../tests/models/Money.test.ts).
```

- Paths are **relative to the prompt file** (`.github/prompts/`), so workspace-root files need `../../`
- Agent receives the full file contents in its context window
- Use Markdown links in prompt files (canonical); `#file:path` works in both prompts and interactive chat

### `#tool:<tool-name>` References

```markdown
Use #tool:githubRepo to search the upstream repository for patterns.
```

- Explicitly tells the agent to use a specific tool
- Distinct from `tools` frontmatter: `tools` *restricts availability*; `#tool:` *directs usage*
- Tool names: type `#` in chat to see the full list

### When to Use File References

| Pattern | Example |
|---------|---------|
| Show the pattern to replicate | `[Money model](../../src/models/Money.ts)` as a template |
| Inject coding rules | `[copilot-instructions](../../.github/copilot-instructions.md)` |
| Provide existing tests as template | `[Money tests](../../tests/models/Money.test.ts)` |
| Inject a spec or API contract | `[API spec](../../docs/api-spec.yaml)` |

### Context Budget

- Total injected content: keep under ~3,000 lines across all references
- Prefer focused files over large monoliths
- Don't inject files already loaded by `copilot-instructions.md`
- Use absolute paths = broken on other machines → always use relative paths

---

## Variables

### `${input:}` — User-Provided Input

```
${input:variableName}                     ← Input field labelled "variableName"
${input:variableName:placeholder text}    ← Input field with placeholder hint
```

- Each `${input:}` triggers a separate input dialog at invocation
- Use descriptive names: `${input:topic}`, `${input:className}`, `${input:featureName}`
- Rule of thumb: **1 variable is ideal**, 2 is acceptable, 3+ → redesign prompt

Pair with `argument-hint` frontmatter for the primary variable:
```yaml
argument-hint: topic to research (e.g., authentication, caching)
```

### Built-in Context Variables (VS Code-resolved)

| Variable | Resolves To |
|----------|-------------|
| `${workspaceFolder}` | Full path of the workspace folder |
| `${workspaceFolderBasename}` | Folder name only (not full path) |
| `${selection}` | Currently selected text in the active editor |
| `${selectedText}` | Same as `${selection}` |
| `${file}` | Full path of the currently open file |
| `${fileBasename}` | Filename with extension (e.g., `Money.ts`) |
| `${fileDirname}` | Directory of the current file |
| `${fileBasenameNoExtension}` | Filename without extension (e.g., `Money`) |

These resolve automatically — no user input needed.

**Combining built-in + user input:**
```markdown
Add ${input:featureName} to the module in ${fileDirname}.
```

**Variables work in the body only** — they are not resolved in YAML frontmatter.

---

## Six Prompt Patterns

Full frontmatter skeletons and body templates for each pattern are in [pattern-templates.md](pattern-templates.md).

| # | Pattern | Agent Mode | Tools | Purpose |
|---|---------|-----------|-------|---------|
| 1 | **Research** | `ask` | `search, readFile, listDirectory` | Explore and report without changes |
| 2 | **Generation** | `agent` | `editFiles, createFile, runCommands, search, readFile` | Create new artefacts following conventions |
| 3 | **Review / Audit** | `ask` | `search, readFile` | Analyse against checklist, produce findings |
| 4 | **Workflow / Pipeline** | `agent` | All | Orchestrate multi-phase tasks with gates |
| 5 | **Transformation** | `agent` | `editFiles, runCommands, search, readFile` | Convert code/data between formats |
| 6 | **Capture / Documentation** | `agent` | `editFiles, createFile, search, readFile` | Extract and preserve knowledge |

**Composing Patterns:**
- Research + Generation: explore first, then create
- Review + Capture: audit findings and document them
- Transformation + Review: convert and verify

Keep composed prompts under 150 lines. If longer, split into separate prompts and chain them.

---

## Prompt Chaining

### Manual Chaining (user controls flow)

Design each prompt to produce a **self-contained file artefact** (not just chat output):

1. `/research auth` → creates `docs/research-auth.md`
2. User reviews, then `/plan` references `#file:docs/research-auth.md`
3. `/implement` follows the plan

Add chainability hints at the end of output-producing prompts:
```markdown
## Next Step
To create an implementation plan from this research, run `/plan`.
```

### In-Session Chaining (shared context)

Within a single session, conversation history is preserved between `/command` invocations.
Prompts don't need to re-inject context that's already visible in the conversation.

### When to Upgrade to Agent Chains

Upgrade from manual prompt chaining to `handoffs` in a custom `.agent.md` when:
- Each phase needs a **different persona or tool set**
- The handoff should be **automated** (button click, not re-typing)
- The workflow is **identical every time** and manual chaining adds friction

---

## Prompt Engineering Techniques

From Anthropic prompting research — apply selectively:

**XML tags for structure** (longer prompts with mixed content):
```markdown
<instructions>
Numbered steps here.
</instructions>

<context>
File references and background here.
</context>

<output-format>
Structural template here.
</output-format>
```

**Examples with `<example>` tags:**
Include 3–5 examples to steer output format, tone, and structure. Especially effective for review and generation prompts.

**Scope control (anti-overengineering):**
Claude tends to add extras by default. Add: "Only make changes that are directly requested. Don't add features, refactor code, or make improvements beyond what was asked."

**Anti-hallucination (research prompts):**
"Never speculate about code you have not opened. Read relevant files FULLY before answering."

**Parallelism (multi-file tasks):**
"When calling multiple tools with no dependencies between the calls, make all calls in parallel." This typically halves execution time for large research tasks.

**Positive framing (trajectory principle):**
Mentioning an undesired action can increase its probability. "Don't edit files" is weaker than "This is a read-only task — report findings only."

**Front-load context, back-load query:**
Place file references and context blocks at the top of the body. Put the task statement and instructions after. Anthropic research shows ending with the query improves response quality up to 30%.

**Include the WHY:**
"Stay objective. Report what exists, do not suggest changes. Reason: this prompt feeds into a separate planning phase." The model makes better edge-case decisions with the reasoning.

---

## Validation Checklist

### Structural

- [ ] File in `.github/prompts/` (or configured via `chat.promptFilesLocations`)
- [ ] Filename ends with `.prompt.md`
- [ ] Both `---` YAML delimiters present; YAML uses spaces only (no tabs)
- [ ] `description` present, non-empty, <80 chars, starts with a verb
- [ ] `argument-hint` present when `${input:}` is used in body
- [ ] `tools` entries match valid tool IDs (if specified)
- [ ] File references (Markdown links) resolve to existing files
- [ ] `${input:}` and built-in variables used **only in the body**, not in frontmatter

### Functional

- [ ] **Discoverability test:** appears in `/` picker and diagnostics view
- [ ] **Cold invocation test:** works in a fresh session with no prior context
- [ ] **Output format test:** response matches specified structure
- [ ] **Tool restriction test:** agent uses only allowed tools (if `tools` specified)
- [ ] **Scope test:** agent doesn't make out-of-scope changes
- [ ] **Edge cases:** empty input, ambiguous input, non-matching workspace

---

## Debugging Diagnostic Steps

1. Verify the prompt appears in the `/` picker.
2. Open **diagnostics view**: right-click in Chat → Diagnostics. Check for load errors.
3. Start a fresh session and invoke the prompt cold (no prior context).
4. Ask the agent: "What instructions did you receive from the prompt I just invoked?"
5. Compare the agent's understanding with your intended instructions.
6. If there's a gap:
   - YAML issue → fix delimiters, remove tabs, quote special chars
   - Body not followed → make steps more imperative and specific
   - Wrong tools → add/fix `tools` field; check priority chain
7. Check tool list priority if the agent uses unexpected tools.

**Diagnostic table:**

| Symptom | Most Likely Cause | First Fix |
|---------|-------------------|-----------|
| Not in `/` picker | Wrong location, extension, or YAML parse error | Check `.github/prompts/`, `.prompt.md` extension, open diagnostics |
| Agent ignores body | Invalid YAML — `---` delimiters or tabs | Validate YAML; enable "Render Whitespace" |
| Agent uses restricted tools | `tools` field missing or wrong IDs | Add/fix `tools`; check tool priority chain |
| File reference not loaded | Wrong relative path | Verify path relative to prompt file location |
| `${input:}` not substituted | Variable name mismatch, or used in frontmatter | Move to body; check exact spelling |
| Built-in variable not resolved | Wrong variable name | Check `${file}` not `${currentFile}`; body only |
| Works in one session, not another | Depends on prior conversation context | Make self-contained; pass cold invocation test |
| Agent overengineers | No scope control clauses | Add anti-overengineering and anti-drift clauses |
| Output varies each time | No output format spec | Add structural template with headings and placeholders |
| Agent asks instead of acting | No "act vs. advise" directive | Add "Implement changes rather than suggesting" |
| Agent hallucinates code details | No anti-hallucination clause | Add "Read files FULLY before answering" |

---

## Security

- **Never embed secrets** (API keys, tokens, passwords) in prompt files — they are version-controlled plain text
- **Audit file references** — verify referenced files don't contain sensitive data before team-sharing the prompt
- **Absolute paths break portability** — always use relative paths; absolute paths also reveal local filesystem structure
- **User profile prompts** (`prompts/` folder) are not version-controlled — keep sensitive personal prompts there, not in `.github/prompts/`
- **`tools: []`** (no tools) is the most restrictive configuration — use for prompts that should be pure conversational only

---

## YAML Pitfalls

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| **Tabs in YAML** | Frontmatter silently ignored; prompt appears broken | Use spaces only; enable "Render Whitespace" in VS Code |
| **Missing `---` delimiter** | Frontmatter not parsed; `description` missing from picker | Add both opening and closing `---` |
| **Unquoted special chars** | YAML parse error on `:`, `&`, `#`, `{`, `}` in strings | Wrap strings containing special chars in double quotes |
| **`tools` as string not array** | `tools: search` fails to parse | Use array syntax: `tools:\n  - search` or `tools: [search]` |
| **Variables in frontmatter** | `${input:}` not substituted; appears literally | Move all variables to the Markdown body |
| **Boolean misspelling** | Value not recognised | Use `true`/`false` (not `yes`/`no`, `True`/`False`) |
| **Trailing spaces** | Occasional parse errors | Trim trailing whitespace |
| **Multi-line description** | YAML scalar rejected or truncated | Keep `description` as a single-line quoted string |
