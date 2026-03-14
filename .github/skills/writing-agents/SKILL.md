---
name: writing-agents
description: "Creates, updates, and corrects custom agent files (*.agent.md) for GitHub Copilot in VS Code. Covers the full agent lifecycle: routing decision, frontmatter fields (name, description, tools, agents, handoffs, model control, user-invokable, disable-model-invocation), persona design, procedure writing, output format definition, rule constraints, agent chains (RPI pattern), subagent architecture, and cross-model validation. Use when: creating a new agent, updating or improving an existing agent, fixing a broken agent, designing an agent chain or subagent architecture, converting a repeated workflow into an agent, or reviewing an agent for anti-patterns. Triggers on: 'create agent', 'write agent', 'new agent', 'update agent', 'fix agent', 'agent.md', 'agent chain', 'handoff', 'agent writer', 'custom agent', 'agent spec', 'subagent', 'coordinator agent', 'RPI pattern'. Do not use for: writing copilot-instructions.md, SKILL.md, prompt.md, hook configurations, or MCP servers."
metadata:
  version: "2.0.0"
  author: "Paul Slits"
---

# Writing Agents

Create, update, or correct custom agent files (`*.agent.md`) for GitHub Copilot.

## Mode Selection

Determine the mode from the user's request:

| Signal | Mode | Section |
|--------|------|---------|
| "Create an agent", "write an agent", "new agent", design a chain | **Create** | Create Mode below |
| "Update", "improve", "refactor", "the agent is too verbose" | **Update** | Update Mode below |
| "Fix", "correct", "agent doesn't work", "agent is broken" | **Correct** | Correct Mode below |

---

## Create Mode (7-Step Process)

### Step 1: Determine Whether an Agent Is the Right Surface

An agent is the correct surface when:

- The task requires a **specialised persona** with a distinct role and expertise.
- The agent needs its own **tool set** different from the default.
- The workflow involves **handoffs** between stages (agent chains).
- The task is a **workflow mode** the user enters and stays in (not one-shot).

If none of these apply, use the correct alternative:

| Knowledge Type | Right Surface |
|---------------|---------------|
| Global coding standards, project rules | `copilot-instructions.md` |
| File-type-specific rules | `*.instructions.md` with `applyTo` |
| One-shot reusable command | `*.prompt.md` |
| Multi-step procedural expertise with bundled resources | `SKILL.md` |
| Deterministic lifecycle action | Hook JSON |
| External API integration | MCP server |

### Step 2: Gather Agent Identity

Determine the following from the user's request or by asking:

| Field | Question |
|-------|----------|
| **Name** | What should the agent be called? (lowercase + hyphens, e.g., `code-reviewer`) |
| **Purpose** | One sentence: what does this agent do? |
| **Persona** | What role does the agent play? What expertise does it have? |
| **Invocation** | User-invokable (`@agent-name`) or handoff-only? |
| **Chain position** | Standalone, or part of a chain? If chained: position and neighbours. |

If the agent is part of a chain, also determine:

| Field | Question |
|-------|----------|
| **Receives from** | Which agent hands off to this one? |
| **Hands off to** | Which agent does this one hand off to? |
| **Handoff label** | What button text should the user see? |
| **Auto-send** | Should the handoff auto-submit or wait for user confirmation? |

### Step 3: Select Tools

Choose the minimal set of tools the agent needs using the **principle of least privilege**. Available tool IDs (use the `category/name` format):

| Category | Tool ID | Capability |
|----------|---------|-----------|
| Read | `read/readFile` | Read file contents |
| Read | `read/problems` | View diagnostics and lint errors |
| Edit | `edit/editFiles` | Create, edit, and delete files |
| Edit | `edit/createFile` | Create new files only |
| Search | `search/listDirectory` | List directory contents |
| Search | `search/fileSearch` | Find files by name pattern |
| Search | `search/textSearch` | Search by text or regex |
| Search | `search/codebase` | Semantic codebase search |
| Search | `search/changes` | View git changes |
| Execute | `execute/runTests` | Run test suite |
| Execute | `execute/runInTerminal` | Execute terminal commands |
| Track | `todo` | Manage todo lists for progress tracking |
| Git | `gitkraken/*` | All GitKraken git operations |
| MCP | `<server-name>/*` | All tools from a named MCP server |

**Role archetype tool sets:**

| Archetype | Typical Tools |
|-----------|--------------|
| Read-only analyst | `read/readFile`, `edit/createFile`, `search/*`, `todo` |
| Designer | `read/readFile`, `edit/createFile`, `search/*`, `todo` |
| Full engineer | All read + edit + search + execute + `todo` |
| Auditor | `read/readFile`, `search/*`, `read/problems`, `execute/runTests`, `execute/runInTerminal`, `todo` |
| Subagent worker | Minimal set for its specific task |

For a full tool matrix and tool scoping examples, read [references/agent-writer-guide.md § 4. Tool Scoping Guidelines](references/agent-writer-guide.md).

### Step 4: Write the Agent File

Create the file at `.github/agents/<name>.agent.md`. The agent file has two parts: YAML frontmatter and Markdown body. The file must start with the YAML frontmatter block (`---`). The body sections must appear in this exact order: Persona → Procedure → Output Format → Rules. Keep the body under 150 lines — if it exceeds 200 lines, the agent is likely doing too much (see anti-pattern #4: The Novel).

#### 4a. Frontmatter

Read [references/frontmatter-guide.md](references/frontmatter-guide.md) for the complete field reference and template.

Key fields:

| Field | Required | Purpose |
|-------|----------|---------|
| `name` | Yes | Agent identifier, used as `@name` invocation |
| `description` | Yes | One-line summary — used for discovery and handoff context |
| `tools` | No | Restrict to specific tools (omit for all tools); use `category/name` format |
| `agents` | No | Which agents can be subagents: list of names, `*` (all, default), or `[]` (none) |
| `model` | No | Pin to a specific model, or use a prioritised fallback array |
| `user-invokable` | No | `false` hides from dropdown (subagent-only agents) |
| `disable-model-invocation` | No | `true` prevents auto-selection; only reachable via handoff |
| `argument-hint` | No | Ghost text shown after `@agent-name` in the chat input |
| `handoffs` | No | Agents this agent can hand off to |
| `target` | No | `vscode` (default) or `github-copilot` |

#### 4b. Body — Persona

Open with a persona statement: who the agent is, what it does, and what it does NOT do. Use second person ("You are a…").

```markdown
You are a codebase researcher. Your job is to thoroughly explore the codebase
and produce structured, factual reports about what exists. You never edit files
or suggest implementation details.
```

**Persona guidelines:**
- One paragraph, 2–4 sentences maximum. Do not exceed 4 sentences.
- State the role affirmatively, then add boundaries ("You never…").
- If the agent is part of a chain, mention what it hands off to ("When complete, hand off to @planner").
- Don't repeat information from the description — the persona adds behavioural nuance.

#### 4c. Body — Procedure

Write the step-by-step procedure the agent follows. Use numbered steps with imperative verbs.

**Procedure guidelines:**
- Each step is a concrete action ("Read", "Extract", "Produce", "List").
- Include sub-steps for complex operations.
- Specify what to include and exclude in each step. Use parenthetical exclusions inline: `List all *.md files in sessions/ (exclude feedback-debt.md and *-feedback-plan.md)`.
- When a step has multiple sub-items, state the count and add "do not skip any": `extract all five categories (do not skip any):`. This prevents models from partially completing the step.
- For steps that models tend to skip (e.g., cross-referencing, aggregation), add "(this step is mandatory — do not skip it)".
- Reference specific file paths, directories, or patterns when applicable.
- If the procedure depends on input from a previous agent, state what input is expected.
- **Context injection:** If the agent needs external knowledge (skills, references, docs), include a Markdown link in the procedure. The agent reads the linked file on demand.

#### 4d. Body — Output Format (Optional)

If the agent produces a structured report, define the format with a Markdown template. Write each output section as a heading at the same level as Procedure and Rules:

```markdown
## Sessions Reviewed

| # | File | Date | Topic |
|---|------|------|-------|
| ... | | | |

## Findings

| Finding | Evidence | Count |
|---------|----------|-------|
| ... | ... | ... |
```

For simple single-block formats, a `## Output Format` wrapper with sub-headings is acceptable.

**Output format guidelines:**
- Write the output format sections at the same heading level as the Procedure and Rules sections — do not nest them under a single `## Output Format` wrapper unless the format is a single block.
- Use tables for structured data.
- Include example rows with `| ... |` placeholders.
- In the final procedure step, instruct the agent to replace example rows with real data and include every section even if empty (state "None found"). Without this, GPT 4.1 may reproduce examples verbatim or omit empty sections.
- Define every section heading the agent should produce.
- Specify whether sections are required or conditional.

#### 4e. Body — Rules

End with explicit constraints. Rules are hard boundaries the agent must not cross.

```markdown
## Rules
- Read-only. Never edit files.
- Cite exact file paths for every finding.
- Report only what is documented — no interpretation.
```

**Rule guidelines:**
- Keep rules short and unambiguous.
- Use imperative negatives for prohibitions ("Never…", "Do not…").
- For citation rules, include a concrete format example: `Cite as sessions/file.md § Section Heading`.
- Include a rule for what to do when the agent is uncertain.
- Include a rule for what to do when input is missing or empty.

### Step 5: Validate

**Structural checks:**

- [ ] File is at `.github/agents/<name>.agent.md`
- [ ] `name` in frontmatter matches filename (minus `.agent.md`)
- [ ] `description` is present and non-empty
- [ ] `tools` list contains only valid `category/name` tool IDs
- [ ] `agents` list is intentionally scoped (not accidentally left as `*` for focused workflows)
- [ ] `user-invokable` is set correctly (subagent-only agents should be `false`)
- [ ] `handoffs` reference agents that exist (or will exist)
- [ ] If `disable-model-invocation: true`, agent is reachable via handoff
- [ ] Body has persona statement, procedure, and rules (output format if applicable)
- [ ] Agent body under 150 lines — if over 200, extract domain knowledge to skills
- [ ] No extraneous files (README.md, CHANGELOG.md) in the agents directory

**Functional checks:**

- [ ] Invocation test: `@agent-name` activates the agent and loads persona
- [ ] Procedure test: following the steps produces correct output
- [ ] Tool restriction test: agent uses only its declared tools
- [ ] Handoff test (if chained): handoff button appears, context carries forward
- [ ] Subagent test (if chained): subagents are spawned with correct context
- [ ] Edge case test: empty input, missing files, ambiguous requests handled gracefully
- [ ] Boundary test: agent does not violate its rules (e.g., read-only agent doesn't edit)

For the full validation checklist, read [references/agent-writer-guide.md § 16. Validation Checklist](references/agent-writer-guide.md).

### Step 6: Iterate

Observe agent behaviour on real tasks. Common fixes:

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| Agent ignores persona | Persona too vague | Make persona more specific with explicit boundaries |
| Agent skips steps | Procedure too verbose or ambiguous | Shorten, make steps more concrete |
| Agent uses wrong tools | Tool list too broad | Restrict to minimum needed tools |
| Handoff doesn't appear | Missing or misspelled `handoffs` field | Verify handoff target name matches |
| Agent invoked accidentally | Should be handoff-only | Add `disable-model-invocation: true` |
| Agent produces wrong format | No output format defined | Add output format template |

### Step 7: Cross-Model Convergence

Ensure the agent produces equivalent output on GPT 4.1 compared to the Claude Opus baseline.

1. **Establish baseline.** Set the agent's `model` frontmatter field to Claude Opus. Run a representative scenario and save the output as the reference baseline.
2. **Switch model.** Change `model` to GPT 4.1.
3. **Run the same scenario.** Execute the identical scenario on GPT 4.1.
4. **Compare outputs.** Diff the GPT 4.1 output against the Opus baseline. Focus on:
   - Structural completeness (all sections present)
   - Correctness of content (no hallucinated or missing details)
   - Consistent persona adherence
   - Tool usage patterns (correct tools, correct order)
   - Handoff behaviour (if chained)
5. **Diagnose divergences.** If GPT 4.1 output differs materially:
   - **Skipped steps** → Make procedure more explicit; number all sub-steps. Add "(this step is mandatory)" annotation.
   - **Partial extraction** → State the count: "extract all five categories (do not skip any)".
   - **Example data reproduced verbatim** → Add instruction: "Replace all example rows with real data."
   - **Empty sections omitted** → Add instruction: "Include every section even if empty (state 'None found')."
   - **Persona drift** → Strengthen persona boundaries; add "You never…" constraints.
   - **Wrong tools used** → Add explicit tool guidance in procedure steps.
   - **Hallucinated content** → Add rules: "Only report what is documented", "Do not invent…".
   - **Missing output sections** → Add output format template with all required headings.
   - **Citation format inconsistent** → Add concrete format example in the rule itself.
6. **Apply fixes and re-test** on GPT 4.1.
7. **Verify Opus is not regressed.** Switch `model` back to Claude Opus and confirm baseline output is still equivalent.
8. **Repeat** steps 3–7 until outputs converge.

---

## Agent Chain Design

When building multi-agent workflows, follow the **Research → Plan → Implement (RPI)** pattern:

| Stage | Role | Tools | Handoff |
|-------|------|-------|---------|
| **Researcher** | Read-only exploration, produces findings report | `search/*`, `read/readFile`, `search/listDirectory` | → Planner |
| **Planner** | Receives findings, produces actionable plan | `search/*`, `read/readFile` | → Implementer |
| **Implementer** | Executes the plan, writes code, runs tests | `edit/editFiles`, `edit/createFile`, `execute/runTests`, `execute/runInTerminal`, `search/*`, `read/readFile` | Terminal |

**Chain design rules:**

1. Only the entry-point agent should be user-invokable. Set `user-invokable: false` or `disable-model-invocation: true` on all other agents in the chain.
2. Each agent has a distinct persona — never combine research and implementation in one agent.
3. Each handoff produces a reviewable artefact. The user reviews before clicking the handoff button.
4. Tools escalate through the chain — researchers are read-only, implementers get write access.
5. Context carries forward through handoffs. Each agent should state what input it expects.

**Handoff configuration:** See [references/frontmatter-guide.md § Handoff Configuration](references/frontmatter-guide.md) for the full YAML syntax (simple and detailed forms), field reference, and examples.

---

## Subagent Architecture

Use subagents to **isolate context**, **enable parallel execution**, and **assign specialised tools/models** to focused tasks. The parent agent delegates work; subagents run in their own context window and return only a summary.

**Key patterns:**

- **Coordinator-worker:** Coordinator agent sets `agents: ['WorkerA', 'WorkerB']` and delegates tasks in its procedure. Workers have `user-invokable: false`.
- **Multi-perspective review:** Coordinator spawns multiple review subagents in parallel, then synthesises findings.
- **TDD pipeline:** Coordinator orchestrates Red → Green → Refactor subagents in sequence.

**Subagent vs. skill:** Subagents solve context isolation and parallel work. Skills solve domain expertise. A well-designed agent often uses **both**: skills for what it needs to *know*, subagents for what it needs to *delegate*.

For full patterns and worked examples, read [references/agent-writer-guide.md § 9. Subagent Architecture](references/agent-writer-guide.md).

---

## Update Mode

1. Read the existing agent file.
2. Identify the user's concern or improvement goal.
3. Diagnose against [references/anti-patterns.md](references/anti-patterns.md).
4. Apply improvements:
   - **Persona too vague** → Rewrite with explicit role and boundaries.
   - **Procedure too long** → Shorten steps, remove obvious instructions.
   - **Tool set too broad** → Restrict to minimum needed.
   - **Description too generic** → Rewrite to be specific about the agent's specialisation.
   - **Missing output format** → Add structured template.
   - **Overlapping with another agent** → Narrow persona, clarify boundaries.
5. Re-validate (Step 5 above).

---

## Correct Mode

1. Validate structure (Step 5 structural checks).
2. If structural issues found, fix them first.
3. Use VS Code Chat Diagnostics (right-click Chat view → Diagnostics) to check agent loading and activation logs.
4. Diagnose the behavioural issue:

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| Agent not in dropdown | File not in `.github/agents/`, wrong extension, or YAML parse error | Check location, ensure `.agent.md` extension, validate YAML |
| Agent never activates | Name mismatch between filename and frontmatter | Fix `name` to match filename |
| Agent activates for wrong tasks | Description too broad | Narrow description |
| Agent ignores instructions | Body too long or verbose | Shorten, make steps imperative |
| Handoff button missing | `handoffs` field missing or misspelled target | Add/fix `handoffs` |
| Agent edits files when it shouldn't | `tools` includes `edit/editFiles` | Remove write tools |
| Agent invoked when it shouldn't be | Missing `disable-model-invocation` | Add `disable-model-invocation: true` |
| Chain breaks at handoff | Context not carried forward | Verify handoff target exists and context is preserved |
| Agent hallucinates content | No guardrail rules | Add explicit rules: "Only report documented facts" |
| Wrong model used | No model control | Set `model` in agent frontmatter, or override via handoff/prompt `model` field |
| Subagent not being invoked | `disable-model-invocation: true` on target, or parent `agents` list excludes it | Check both agent files |
| Agent body too large | Domain knowledge embedded in body | Extract to skills; see [agent-writer-guide.md § 5](references/agent-writer-guide.md) |
| Too many tools error | Over 128 tools enabled | Reduce `tools` list or use tool sets |

5. Apply fixes.
6. Re-validate (Step 5 above).

For advanced diagnosis, read [references/agent-writer-guide.md § 15. Diagnostics & Troubleshooting](references/agent-writer-guide.md).

---

## Deep Reference

For detailed guidance on specific aspects, read from `references/`:

- **Comprehensive guide (all topics)** → [references/agent-writer-guide.md](references/agent-writer-guide.md)
  - Frontmatter field catalogue + annotated examples → `§ 3. YAML Frontmatter Reference`
  - Tool scoping by archetype + full tool matrix → `§ 4. Tool Scoping Guidelines`
  - Agent vs. skill decision framework → `§ 5. Agent vs. Skill: Decision Framework`
  - Markdown body section order + writing tips → `§ 6. Markdown Body: Structuring Agent Instructions`
  - Naming conventions → `§ 7. Naming Conventions`
  - Handoff design + graph patterns → `§ 8. Handoff Design`
  - Subagent architecture patterns → `§ 9. Subagent Architecture`
  - Validation checklist → `§ 16. Validation Checklist`
  - Anti-patterns (full gallery) → `§ 17. Anti-Patterns to Avoid`
  - Worked example templates → `§ 18. Worked Example Templates`
- Frontmatter field reference + handoff syntax → [references/frontmatter-guide.md](references/frontmatter-guide.md)
- Anti-pattern quick check → [references/anti-patterns.md](references/anti-patterns.md)
