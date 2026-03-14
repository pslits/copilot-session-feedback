# Agent Frontmatter Reference

## Frontmatter Template

```yaml
---
name: <agent-name>                   # Must match filename (minus .agent.md)
description: "<One-line summary of what this agent does and its specialisation.>"
tools:                               # Use category/name format; omit for all tools
  - read/readFile
  - search/codebase
argument-hint: "<ghost text shown after @agent-name>"  # Optional
agents: ['*']                        # Optional — which agents can be subagents
model: Claude Sonnet 4.5 (copilot)  # Optional — pin to a specific model
user-invokable: true                 # Optional — false hides from dropdown
disable-model-invocation: false      # Optional — true = handoff-only
handoffs:                            # Optional — agents this agent can hand off to
  - label: Next Phase
    agent: <target-agent-name>
    prompt: Proceed with the plan above.
    send: false
---
```

## Field Reference

### Required Fields

| Field | Constraint | Description |
|-------|-----------|-------------|
| `name` | Non-empty string, must match filename | Agent identifier. Used as `@name` invocation in Chat. |
| `description` | Non-empty string | One-line summary of the agent's role and specialisation. Shown during discovery and handoff context. |

### Optional Fields

| Field | Default | Description |
|-------|---------|-------------|
| `tools` | All tools | Restricts the agent to specific tools. Principle of least privilege — only include tools the agent needs. Use `category/name` format. |
| `agents` | `*` (all) | Which agents can be invoked as subagents: a list of names, `*` (all), or `[]` (none). |
| `model` | User's selected model | Pin to a specific model (`Claude Sonnet 4.5 (copilot)`) or a prioritised fallback array. |
| `user-invokable` | `true` | `false` hides agent from the dropdown — useful for subagent-only agents. |
| `disable-model-invocation` | `false` | `true` prevents auto-selection as subagent. Agent reachable only via handoff. |
| `argument-hint` | None | Ghost text shown in the chat input after `@agent-name `. |
| `handoffs` | None | List of agents this agent can hand off to. Creates handoff buttons in Chat UI. |
| `target` | `vscode` | Target environment: `vscode` or `github-copilot`. |
| `mcp-servers` | None | MCP server configurations (only for `target: github-copilot`). |

### Tool IDs (category/name format)

| Category | Tool ID | Capability | Typical Agent Type |
|----------|---------|-----------|-------------------|
| Read | `read/readFile` | Read file contents | All |
| Read | `read/problems` | View diagnostics and lint errors | Engineers, auditors |
| Edit | `edit/editFiles` | Create, edit, and delete files | Implementers only |
| Edit | `edit/createFile` | Create new files | Implementers, generators |
| Search | `search/listDirectory` | List directory contents | Researchers, explorers |
| Search | `search/fileSearch` | Find files by name pattern | All |
| Search | `search/textSearch` | Search by text or regex | All |
| Search | `search/codebase` | Semantic codebase search | Researchers |
| Search | `search/changes` | View git changes | Engineers, auditors |
| Execute | `execute/runTests` | Run test suite | Engineers, auditors |
| Execute | `execute/runInTerminal` | Execute terminal commands | Engineers |
| Track | `todo` | Manage todo lists for progress tracking | All |
| Git | `gitkraken/*` | All GitKraken git operations | Engineers |
| MCP | `<server-name>/*` | All tools from a named MCP server | As needed |

### Handoff Configuration

**Simple form** — agent name only:
```yaml
handoffs:
  - planner
```

**Detailed form** — with label, prompt, auto-send, and model override:
```yaml
handoffs:
  - label: Create Implementation Plan
    agent: planner
    prompt: Create a plan based on the research above
    send: true
    model: claude-sonnet-4
```

| Handoff Field | Required | Default | Description |
|---------------|----------|---------|-------------|
| `label` | No | Agent name | Button text shown to the user in Chat UI |
| `agent` | Yes | — | Target agent name (must match target's `name` field) |
| `prompt` | No | Empty | Pre-filled prompt text for the next agent |
| `send` | No | `false` | If `true`, auto-submit the handoff without user confirmation |
| `model` | No | Inherits | Override the model for the target agent |

### Invocation Control

| Field | Value | Behaviour |
|-------|-------|----------|
| `user-invokable` | `true` (default) | Agent appears in the dropdown; user can invoke via `@name` |
| `user-invokable` | `false` | Agent hidden from dropdown; only reachable via handoff or `agents` list |
| `disable-model-invocation` | `false` (default) | Agent can be auto-selected as a subagent by other agents |
| `disable-model-invocation` | `true` | Agent cannot be auto-selected; only reachable via explicit handoff |

### Model Control

Model selection for agents can be controlled at multiple levels:

| Method | Where | Use Case |
|--------|-------|----------|
| `model` frontmatter field | Agent file | Pin the agent to a specific model regardless of user selection |
| User model picker | Chat UI | User selects model at invocation time (default when no `model` field) |
| Handoff `model` field | `handoffs` config | Override model when handing off to next agent |
| Prompt `model` field | `*.prompt.md` referencing the agent via `agent: <name>` | Pin model when invoking agent through a prompt |

The `model` frontmatter field is useful for cross-model convergence testing — set the model in the agent file to switch between models without changing the Chat UI picker.

### Model Selection Guidance

| Consideration | Recommendation |
|---------------|----------------|
| **Consistency matters** (code generation, audits) | Pin a specific model: `model: Claude Sonnet 4.5 (copilot)` |
| **Cost-sensitive / exploratory** tasks | Use a smaller model or let the user choose (omit `model`) |
| **Fallback resilience** (model may be unavailable) | Use a prioritised array: `['Claude Sonnet 4.5 (copilot)', 'GPT-5 (copilot)']` |
| **Subagent-only agents** doing narrow tasks | A smaller, faster model reduces latency |
| **Handoff overrides** | Use `handoffs[].model` to select a different model per handoff |

## Agent File Location

Agents are stored at `.github/agents/<name>.agent.md`.

> Minimum VS Code version: 1.106+.

The `name` field in frontmatter must match the filename. For example:
- File: `.github/agents/code-reviewer.agent.md`
- Frontmatter: `name: code-reviewer`

## Body Structure Template

```markdown
---
name: <agent-name>
description: <one-line description>
tools:
  - <tool-1>
  - <tool-2>
handoffs:
  - <target-agent>
# model: <model-name>         # Optional — pin to a specific model
---

You are a <role>. Your job is to <primary responsibility>.
You never <boundary 1>. You do not <boundary 2>.

## Procedure
1. <First action step>
2. <Second action step>
3. For each <item>, extract all <N> categories (do not skip any):
   - **Sub-item A** — description
   - **Sub-item B** — description
4. <Aggregation or synthesis step> (this step is mandatory — do not skip it)
5. Produce the output using the section templates below. Replace all example rows with real data. Include every section even if empty (state "None found").

## Section 1

| Column A | Column B | Column C |
|----------|----------|----------|
| ... | ... | ... |

## Section 2

| Column D | Column E |
|----------|----------|
| ... | ... |

## Rules
- <Hard constraint 1>
- <Hard constraint 2>
- If <edge case>, then <behaviour>.
```
