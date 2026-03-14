---
name: writing-prompts
description: "Creates, updates, and corrects prompt files (*.prompt.md) for GitHub Copilot in VS Code. Covers the full prompt lifecycle: routing decision, frontmatter fields (description, agent modes ask/agent/plan/custom, tools, model, argument-hint), body structure, context injection (Markdown links, #tool: references), parameterisation (${input:} and built-in variables like ${file} ${selection}), six prompt patterns, chaining, validation, and debugging. Use when: creating a new prompt file, updating or improving an existing prompt, fixing a broken prompt that doesn't load or misbehaves, converting a repeated chat workflow into a prompt, reviewing a prompt for anti-patterns, or writing *.prompt.md files. Triggers on: 'create prompt', 'write prompt', 'new prompt', 'update prompt', 'fix prompt', 'prompt file', 'slash command', 'prompt.md', 'prompt writer'. Do not use for: writing copilot-instructions.md, custom agents (.agent.md), skills (SKILL.md), hooks, or general prompt engineering outside VS Code."
metadata:
  version: "2.0.0"
  author: "Paul Slits"
---

# Writing Prompts

Create, update, or correct prompt files (`*.prompt.md`) for GitHub Copilot in VS Code.

## Mode Selection

Determine the mode from the user's request:

| Signal | Mode | Section |
|--------|------|---------|
| "Create a prompt", "write a prompt", "new prompt", convert chat workflow | **Create** | Create Mode below |
| "Update", "improve", "tighten", "the output format is inconsistent" | **Update** | Update Mode below |
| "Fix", "correct", "prompt doesn't load", "prompt is broken" | **Correct** | Correct Mode below |

---

## Create Mode (6-Step Process)

### Step 1: Routing Check

Verify a prompt file is the right surface. Ask two questions:

1. **Is this a repeatable, multi-step task?** If no → one-off, type in chat directly.
2. **Does it need a specialised persona, handoffs, or bundled resources?** If no → **prompt file**. If yes → agent or skill.

If the answer is **not** a prompt file, tell the user which surface to use and stop.

### Step 2: Identify the Pattern

Match the user's task to one of the six prompt patterns:

| Pattern | Use When | Agent Mode |
|---------|----------|------------|
| **Research** | Explore and report without changes | `ask` |
| **Generation** | Create new files following conventions | `agent` |
| **Review / Audit** | Analyse code against a checklist | `ask` |
| **Workflow / Pipeline** | Orchestrate multi-phase tasks with gates; plan before acting | `agent` or `plan` |
| **Transformation** | Convert code or data between formats | `agent` |
| **Capture / Documentation** | Extract and preserve knowledge | `agent` |

If the task combines two patterns, compose them. Keep body under 150 lines.

### Step 3: Determine File Location and Name

- **Team prompts:** `.github/prompts/<command-name>.prompt.md`
- **Personal prompts:** VS Code profile `prompts` folder

Naming rules:
- Lowercase with hyphens
- 1–3 words, verb-noun pattern: `research-topic`, `gen-model`, `review-code`
- Avoid vague names: `help`, `do-stuff`, `run`

### Step 4: Write the Frontmatter

Read [references/prompt-writer-guide.md](references/prompt-writer-guide.md) section "Frontmatter Template" for the full field reference. Apply these rules:

**`description` (required):**
- Start with a verb: "Research…", "Create…", "Review…"
- Keep under ~80 characters
- State the output or benefit
- Formula: `<Verb> <what> <output/benefit>`

**`argument-hint` (if `${input:}` used):**
- One phrase with parenthetical examples: `topic to research (e.g., authentication, caching)`
- Pair with the primary `${input:}` variable

**`agent` (when not default):**
- `ask` — read-only conversational mode; no file edits or tool calls
- `agent` — full agent mode with all tools (default when omitted)
- `plan` — generates an implementation plan before taking any action; use for complex multi-step tasks where upfront planning improves outcomes
- `<custom-agent-name>` — delegates to a named `.agent.md`; applies its persona, tools, and model

**`tools` (when restricting):**
- Omit for full access; list only to restrict
- Read-only: `[search, readFile, listDirectory]`
- Pure conversation: `[]`

**`model` (only when needed):**
- Pin complex reasoning to a high-capability model
- Use array syntax for fallback across plans

### Step 5: Write the Body

Follow the four-part structure:

```
1. Task Statement     — one sentence saying what to do
2. Instructions       — numbered steps
3. Constraints        — scope boundaries
4. Output Format      — structural template
```

**Body rules:**
- Imperative mood: "Search for…" not "It would be good if…"
- Be specific: name files, directories, tools
- Frame instructions positively; negation is fine for constraints
- State act vs. advise explicitly
- Place file references at the **top** (front-load context)
- Variables work only in the body, never in frontmatter
- One `${input:}` variable is ideal; two acceptable; three+ → redesign
- Use `${input:variableName:placeholder text}` to provide a hint inside the input field

**Built-in context variables (VS Code-resolved, no user input):**
- `${file}` — full path of the currently open file
- `${fileBasename}` — filename with extension (e.g., `Money.ts`)
- `${fileBasenameNoExtension}` — filename without extension (e.g., `Money`)
- `${fileDirname}` — directory of the current file
- `${selection}` / `${selectedText}` — currently selected text in the active editor
- `${workspaceFolder}` — full path of the workspace folder
- `${workspaceFolderBasename}` — workspace folder name only

Combine: `${input:featureName}` for what the user specifies + `${file}` for context the editor already knows.

**Include these clauses as appropriate to the pattern:**
- Anti-overengineering: "Only make changes that are directly requested."
- Anti-hallucination: "Never speculate about code you have not opened."
- Parallelism: "Make independent tool calls in parallel."
- Read-first: "Read all mentioned files FULLY before acting."
- Anti-drift: "Do not add features beyond what is described in this prompt."
- Chainability: "## Next Step\nTo do X, run `/next-command`."

Read [references/prompt-writer-guide.md](references/prompt-writer-guide.md) section "Six Prompt Patterns" for frontmatter skeletons and body templates for each pattern.

### Step 6: Validate

**Structural checks:**

- [ ] File in `.github/prompts/` or configured location
- [ ] Filename ends with `.prompt.md`
- [ ] Both `---` delimiters present; YAML uses spaces only
- [ ] `description` present, non-empty, <80 chars, verb-first
- [ ] `tools` entries match valid tool IDs (if set)
- [ ] File references (Markdown links) resolve to existing files
- [ ] `${input:}` paired with `argument-hint`; variables (`${input:}` and built-in) only in body
- [ ] Three invocation methods tested: `/command`, Command Palette (`Chat: Run Prompt`), play button in editor title

**Functional checks:**

- [ ] **Discoverability test:** appears in `/` picker and diagnostics view
- [ ] **Cold invocation test:** works in a fresh session with no prior context
- [ ] **Output format test:** response matches specified structure
- [ ] **Tool restriction test:** agent uses only allowed tools
- [ ] **Scope test:** agent doesn't make out-of-scope changes
- [ ] **Edge cases:** empty input, ambiguous input, non-matching workspace

---

## Update Mode

1. Read the existing prompt file fully.
2. Identify the user's concern or improvement goal.
3. Diagnose against the anti-patterns list in [references/anti-patterns.md](references/anti-patterns.md). Quick diagnosis: check #6 (Invisible Prompt), #17 (Tab-Indented YAML), #9 (Magic Dependency) first. Extended check for:
   - Wall of Text (body >150 lines)
   - Vague Command (no specific steps)
   - Swiss Army Knife (does too many things)
   - Phantom Input (`${input:}` without `argument-hint`)
   - Context Bomb (too many large file references)
   - Format Ambiguity (no output format spec)
   - Magic Dependency (works only with prior context)
   - Overengineer Enabler (no anti-overengineering clause)
   - Silent Hallucinator (no anti-hallucination clause)
4. Apply improvements:
   - **Body too long** → Split into focused prompts or upgrade to a skill
   - **Output inconsistent** → Add explicit output format section with headers
   - **Agent goes off-scope** → Add anti-drift, anti-overengineering clauses
   - **Agent speculates** → Add anti-hallucination clause and read-first pattern
   - **Description vague** → Rewrite with description formula (verb + what + output)
   - **Missing parallelism** → Add parallelism clause for multi-file tasks
5. Re-validate (Step 6 above).

---

## Correct Mode

1. Validate structure (Step 6 structural checks).
2. If structural issues found, fix them first.
3. Use the diagnostics view: right-click in Chat → Diagnostics to see loaded prompts and errors.
4. Diagnose the issue:

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| Not in `/` picker | Wrong location, extension, or invalid YAML | Check location, filename; diagnostics view |
| Agent ignores body | Invalid YAML frontmatter — `---` delimiters or tabs | Validate `---`; use spaces only |
| Agent uses restricted tools | `tools` field missing or wrong IDs | Add/fix `tools`; check priority chain |
| File reference not loaded | Wrong relative path (must be relative to prompt file) | Verify and fix relative paths |
| `${input:}` not substituted | Variable in frontmatter or name mismatch | Move to body; check spelling |
| Works in one session, fails in another | Depends on prior conversation context | Make self-contained; pass cold invocation test |
| Agent overengineers | No scope control clauses | Add anti-overengineering and anti-drift clauses |
| Output varies each time | No output format specification | Add structural template with headers |
| Agent asks instead of acting | No "act vs. advise" directive | Add "Implement changes rather than suggesting" |
| Agent hallucinates about code | No anti-hallucination clause | Add "Read files FULLY before answering" |

5. Apply fixes.
6. Re-validate (Step 6 above).

---

## Deep Reference

For detailed guidance on any aspect, read specific sections from [references/prompt-writer-guide.md](references/prompt-writer-guide.md):

- Routing decisions → search for `## Routing`
- Frontmatter fields → search for `## Frontmatter Template`
- Body structure and writing style → search for `## Body — Four-Part Structure`
- Context injection (file refs, tool refs) → search for `## Context Injection`
- Variables and parameterisation → search for `## Variables`
- Six prompt patterns (templates) → search for `## Six Prompt Patterns`
- Prompt chaining → search for `## Prompt Chaining`
- Prompt engineering techniques → search for `## Prompt Engineering Techniques`
- Anti-patterns (full gallery) → search for `## Anti-Patterns`
- Validation and testing → search for `## Validation Checklist`
- Debugging and diagnostics → search for `## Debugging Diagnostic Steps`
- Security considerations → search for `## Security`
- YAML pitfalls → search for `## YAML Pitfalls`
