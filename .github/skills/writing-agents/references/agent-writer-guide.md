# How to Create a Custom Agent

A step-by-step guide for authoring `.agent.md` files that integrate correctly with VS Code Copilot Chat and slot into your existing multi-agent lifecycle.

> **Minimum VS Code version:** 1.106+ (custom agents were previously called "custom chat modes").

### Quick start

Building your first agent? Copy this starter, save it as `.github/agents/{your-role}.agent.md`, and adapt:

```yaml
---
name: Your Role Name
description: One sentence explaining what this agent does
tools:
  - read/readFile
  - search/fileSearch
  - search/textSearch
  - search/codebase
  - todo
model: Claude Sonnet 4.5 (copilot)
user-invokable: true
---

# Your Role Name

You are a [role]. Your goal is to [primary objective].

## Behavioural Guardrails

- **DO** [positive constraint].
- **DO NOT** [negative constraint].

## Workflow

1. [First step].
2. [Second step].
3. [Third step].
```

Then refine using these sections:

1. **[Section 3](#3-yaml-frontmatter-reference)** — Full frontmatter field catalogue
2. **[Section 4](#4-tool-scoping-guidelines)** — Pick the right tools for your role
3. **[Section 5](#5-agent-vs-skill-decision-framework)** — Decide what goes in the agent vs. a skill
4. **[Section 6](#6-markdown-body-structuring-agent-instructions)** — Structure the body using the 10-section template
5. **[Section 16](#16-validation-checklist)** — Run the checklist before committing

For team integration, subagents, and handoffs, continue with the remaining sections.

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Anatomy of an agent.md File](#2-anatomy-of-an-agentmd-file)
3. [YAML Frontmatter Reference](#3-yaml-frontmatter-reference)
4. [Tool Scoping Guidelines](#4-tool-scoping-guidelines)
5. [Agent vs. Skill: Decision Framework](#5-agent-vs-skill-decision-framework)
6. [Markdown Body: Structuring Agent Instructions](#6-markdown-body-structuring-agent-instructions)
7. [Naming Conventions](#7-naming-conventions)
8. [Handoff Design](#8-handoff-design)
9. [Subagent Architecture](#9-subagent-architecture)
10. [Integrating with the Team Lifecycle](#10-integrating-with-the-team-lifecycle)
11. [Agent Hooks Integration](#11-agent-hooks-integration)
12. [Skills Integration](#12-skills-integration)
13. [Prompt File Interaction](#13-prompt-file-interaction)
14. [Cross-Platform Compatibility](#14-cross-platform-compatibility)
15. [Diagnostics & Troubleshooting](#15-diagnostics--troubleshooting)
16. [Validation Checklist](#16-validation-checklist)
17. [Anti-Patterns to Avoid](#17-anti-patterns-to-avoid)
18. [Worked Example Templates](#18-worked-example-templates)
19. [References](#19-references)

---

## 1. Introduction

### What is a custom agent?

A custom agent is a **persona + tools + instructions** bundled in a single `.agent.md` file. When you select the agent in the Chat view, VS Code prepends the instructions to every prompt and scopes the available tools to exactly what the file declares. This creates a repeatable, role-specific AI experience.

### When to create a new agent vs. extend an existing one

| Situation | Action |
|-----------|--------|
| Need a new role in the workflow (e.g. database administrator) | Create a new `.agent.md` |
| Need a new role AND it requires domain expertise | Create an agent + one or more skills (see [Section 5](#5-agent-vs-skill-decision-framework)) |
| Existing agent needs a small domain reminder (~5 lines) | Add content to that agent's markdown body |
| Existing agent needs substantial domain knowledge (~30+ lines) | Create a skill and reference it from the agent body |
| Need to reuse instructions across multiple agents | Create shared `.instructions.md` files and reference them via Markdown links |
| Need a one-off task (e.g. generate a migration script) | Create a [prompt file](https://code.visualstudio.com/docs/copilot/customization/prompt-files) (`.prompt.md`) instead |
| Need a portable, composable capability | Create a [skill](https://code.visualstudio.com/docs/copilot/customization/agent-skills) (`.github/skills/*/SKILL.md`) instead |

### Where agents live

| Location | Scope | Shared via version control? |
|----------|-------|----------------------------|
| `.github/agents/` | Workspace | Yes |
| `.claude/agents/` | Workspace (Claude format) | Yes |
| User profile `prompts/` folder | All workspaces | No (sync via Settings Sync) |
| GitHub organization level | All org repos | Yes (org settings) |

> Additional locations can be configured with the `chat.agentFilesLocations` setting.

---

## 2. Anatomy of an `.agent.md` File

Every agent file has two layers:

```
┌──────────────────────────────────────────┐
│  YAML Frontmatter  (--- ... ---)         │  ← Machine-readable configuration
│  Parsed by VS Code at load time          │     (tools, model, handoffs, etc.)
├──────────────────────────────────────────┤
│  Markdown Body                           │  ← Human-readable instructions
│  Prepended to every prompt at runtime    │     (role, guardrails, workflow, etc.)
└──────────────────────────────────────────┘
```

**How VS Code processes your agent at runtime:**

1. Parses YAML frontmatter → resolves tools, model, handoffs
2. Reads Markdown body → prepends it to the user's prompt
3. Merges with always-on instructions (`copilot-instructions.md`, `AGENTS.md`)
4. Sends combined prompt + tools to the selected model

---

## 3. YAML Frontmatter Reference

### Complete field catalogue

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `name` | string | Yes | filename | Display name shown in the agents dropdown and used for `@mention` |
| `description` | string | Yes | — | One-sentence summary; shown as placeholder text. Also helps the model select this agent when used as a subagent |
| `argument-hint` | string | No | — | Ghost text shown after `@agent-name ` in the chat input box |
| `tools` | list | Yes | — | Tool/tool-set names available to this agent. Use `<mcp-server>/*` for all tools from an MCP server |
| `agents` | list | No | `*` | Which agents can be invoked as subagents: a list of names, `*` (all), or `[]` (none) |
| `model` | string or list | No | current picker | Model name, or a prioritized fallback array: `['Claude Sonnet 4.5 (copilot)', 'GPT-5 (copilot)']` |
| `user-invokable` | bool | No | `true` | Whether the agent appears in the agents dropdown. Set `false` for subagent-only agents |
| `disable-model-invocation` | bool | No | `false` | Prevents other agents from invoking this agent as a subagent. Set `true` when only explicit user selection is appropriate |
| `target` | string | No | `vscode` | Target environment: `vscode` or `github-copilot` |
| `mcp-servers` | list | No | — | MCP server configurations (only for `target: github-copilot`) |
| `handoffs` | list | No | — | Sequential workflow transitions. Each entry is an object (see below) |
| `handoffs[].label` | string | — | — | Button text displayed after the response completes |
| `handoffs[].agent` | string | — | — | Target agent identifier (must match that agent's `name` field) |
| `handoffs[].prompt` | string | — | — | Pre-filled prompt sent to the target agent |
| `handoffs[].send` | bool | — | `false` | `false` = button appears, user clicks to submit. `true` = auto-submits |
| `handoffs[].model` | string | No | — | Override the model for the handoff target |
| ~~`infer`~~ | ~~bool~~ | — | — | **Deprecated.** Use `user-invokable` and `disable-model-invocation` instead |

### Model selection guidance

| Consideration | Recommendation |
|---------------|----------------|
| **Consistency matters** (e.g. code generation, audits) | Pin a specific model: `model: Claude Sonnet 4.5 (copilot)` |
| **Cost-sensitive / exploratory** tasks | Use a smaller model or let the user choose (omit `model`) |
| **Fallback resilience** (model may be unavailable) | Use a prioritized array: `['Claude Sonnet 4.5 (copilot)', 'GPT-5 (copilot)']` |
| **Subagent-only agents** doing narrow tasks | A smaller, faster model reduces latency |
| **Handoff overrides** | Use `handoffs[].model` to select a different model per handoff target |

> **Tip:** Omitting `model` lets the user's current model picker selection apply. Pin a model only when the agent's behaviour depends on a specific model's capabilities.

### Annotated minimal example

```yaml
---
name: Documentation Reviewer                    # Appears in dropdown
description: Review documentation for accuracy   # One sentence, active voice
tools:                                           # Read-only — no edit tools
  - read/readFile
  - search/fileSearch
  - search/textSearch
  - search/codebase
model: Claude Sonnet 4.5 (copilot)              # Fixed model for consistency
user-invokable: true                             # Visible in dropdown
---
```

### Annotated full example

```yaml
---
name: Feature Builder                            # Coordinator agent
description: Orchestrate feature development from plan to review
argument-hint: Describe the feature to build
tools:
  - read/readFile
  - edit/editFiles
  - edit/createFile
  - search/listDirectory
  - search/fileSearch
  - search/textSearch
  - search/codebase
  - read/problems
  - execute/runTests
  - execute/runInTerminal
  - todo
  - search/changes
agents: ['Planner', 'Implementer', 'Reviewer']  # Restrict subagents
model:                                           # Prioritized fallback
  - Claude Sonnet 4.5 (copilot)
  - GPT-5 (copilot)
user-invokable: true
handoffs:
  - label: Start Implementation
    agent: Implementer
    prompt: Implement the plan outlined above following TDD principles.
    send: false
  - label: Review Code Quality
    agent: Reviewer
    prompt: Review the implementation for quality and security issues.
    send: false
    model: Claude Sonnet 4.5 (copilot)           # Override model for this handoff
---
```

---

## 4. Tool Scoping Guidelines

### The least-privilege principle

Grant only the tools the role genuinely needs. Over-permissioning leads to unintended side effects (e.g., an analyst accidentally editing files).

### Tool identifier taxonomy

| Category | Identifiers | Purpose |
|----------|-------------|---------|
| Read | `read/readFile`, `read/problems` | Read files and view diagnostics |
| Edit | `edit/editFiles`, `edit/createFile` | Modify or create files |
| Search | `search/listDirectory`, `search/fileSearch`, `search/textSearch`, `search/codebase`, `search/changes` | Navigate and search the codebase |
| Execute | `execute/runTests`, `execute/runInTerminal` | Run commands and tests |
| Track | `todo` | Manage todo lists for progress tracking |
| Git | `gitkraken/*` | Git operations |
| MCP | `<server-name>/*` | All tools from an MCP server |

### Scoping by role archetype

| Archetype | Tools | Rationale |
|-----------|-------|-----------|
| **Read-only analyst** | `read/readFile`, `edit/createFile`, `search/*`, `todo` | Gathers information, creates docs, never edits code |
| **Designer** | `read/readFile`, `edit/createFile`, `search/*`, `todo` | Creates design docs, never edits code |
| **Full engineer** | All read + edit + search + execute + git + todo | Needs full access for TDD workflow |
| **Auditor** | `read/readFile`, `search/*`, `read/problems`, `execute/runTests`, `execute/runInTerminal`, `todo` | Runs tools and reads, never edits |
| **Subagent-only worker** | Minimal set for its task | Context-isolated; keep it lean |

### Example tool matrix

For a team with four agents, the tool matrix might look like this:

| Tool | Analyst | Designer | Engineer | Auditor |
|------|:---:|:---:|:---:|:---:|
| `read/readFile` | ✅ | ✅ | ✅ | ✅ |
| `edit/editFiles` | — | — | ✅ | — |
| `edit/createFile` | ✅ | ✅ | ✅ | — |
| `search/*` | ✅ | ✅ | ✅ | ✅ |
| `execute/runTests` | — | — | ✅ | ✅ |
| `execute/runInTerminal` | — | — | ✅ | ✅ |
| `read/problems` | — | — | ✅ | ✅ |
| `todo` | ✅ | ✅ | ✅ | ✅ |

> **Tip:** Create a similar matrix for your own team and keep it in your agents README. It makes tool-scoping decisions visible and auditable.

### Tool sets

You can group tools into named sets via a `.jsonc` file and reference the set name in `tools`. This keeps frontmatter concise:

```jsonc
// .vscode/toolsets.jsonc
{
  "reader": {
    "tools": ["read/readFile", "search/codebase", "search/textSearch"],
    "description": "Read-only tools",
    "icon": "book"
  }
}
```

Then in frontmatter: `tools: ['reader', 'edit/createFile', 'todo']`

### Tool reference syntax in body text

Reference tools in the Markdown body with `#tool:<tool-name>`:

```markdown
Use #tool:githubRepo to search the upstream repository for patterns.
```

### Tool list priority order

When a prompt file references an agent, tools are resolved in this order (see also [Section 13](#13-prompt-file-interaction)):

1. Tools specified in the **prompt file** (if any)
2. Tools from the **referenced custom agent** (if any)
3. **Default tools** for the selected agent (if any)

---

## 5. Agent vs. Skill: Decision Framework

Agents and skills serve different purposes and complement each other. An agent defines **who** (role identity, behavioural guardrails, workflow, tool access). A skill defines **how** (procedural domain knowledge that any agent can pull in on demand). Getting this split right keeps your agents lean, your context window efficient, and your domain knowledge reusable.

### The architecture in a nutshell

This layered model (inspired by Anthropic's "build skills, not agents" architecture) shows how the pieces fit together:

```
┌──────────────────────────────────────────────────┐
│  Agent (.agent.md)                               │
│  Role identity · Workflow · Guardrails · Tools   │  ← Always in context
├──────────────────────────────────────────────────┤
│  Skills (.github/skills/*/SKILL.md)              │
│  Domain expertise · Procedures · Scripts         │  ← On-demand (progressive disclosure)
├──────────────────────────────────────────────────┤
│  MCP Servers                                     │
│  External data · APIs · System connectivity      │  ← Runtime connectivity
├──────────────────────────────────────────────────┤
│  Agent Runtime (VS Code / Copilot CLI)           │
│  Context management · Tool orchestration         │  ← Universal infrastructure
└──────────────────────────────────────────────────┘
```

The agent is the thin orchestration layer. Skills are the domain expertise layer. Keeping them separate means you can change domain knowledge without touching agent configuration, and vice versa.

### Decision matrix: what goes where?

| Criterion | Stays in the agent body | Extract to a skill |
|-----------|------------------------|--------------------|
| **Defines the role** ("You are a [Role Name]") | ✅ | |
| **Behavioural guardrails** (DO / DO NOT rules) | ✅ | |
| **Workflow skeleton** (phase sequence, handoff triggers) | ✅ | |
| **Domain procedure** ("how to create a value object") | | ✅ |
| **Reusable across agents** (multiple agents need the same knowledge) | | ✅ |
| **Changes independently** of the agent's role | | ✅ |
| **Contains scripts or executable assets** | | ✅ |
| **Large body of reference material** (checklists, standards, patterns) | | ✅ |
| **One-agent-only context** (specific to this role, small enough) | ✅ | |

### Why this matters: the context budget

Everything in an agent's markdown body is **always prepended** to every prompt — it permanently occupies the context window. Skills, by contrast, use **progressive disclosure**: only a short metadata line appears until the agent decides it needs the skill. This keeps the agent in the productive part of the context window (the "smart zone") and avoids wasting tokens on knowledge that isn't needed for the current task.

```
 Context window budget
 ┌─────────────────────────────────────────────────────┐
 │ ██████ Agent body (always loaded — keep this lean)  │
 │ ░░░░░░ Skill metadata (one line each — cheap)      │
 │        Skill content (loaded only when needed)      │
 │ ▓▓▓▓▓▓ User prompt + conversation                  │
 │        ← room for tool calls & reasoning →         │
 └─────────────────────────────────────────────────────┘
```

**Rule of thumb:** If a block of agent-body instructions is larger than ~30 lines and is not about role identity, guardrails, or workflow sequencing, it is a candidate for extraction into a skill.

> **Measuring your agent body:** Run `wc -l .github/agents/your-agent.agent.md` (or `(Get-Content .github/agents/your-agent.agent.md | Measure-Object -Line).Lines` in PowerShell) to check line count. Aim for **50–80 lines** for lean agents, **100–150 lines** for full coordinators. Beyond 150 lines, actively look for content to extract into skills.

### Example: mapping agents and skills

Here is how a typical team might map agents and skills:

| Component | Type | Rationale |
|-----------|------|----------|
| `@engineer` | Agent | Defines the TDD workflow, quality gates, handoff to review — this is role + process |
| `@reviewer` | Agent | Defines the audit workflow, report format, severity classification — role + process |
| `code-validator` | Skill | Procedural checklist for validating source files — reusable by any agent that touches code |
| `doc-generator` | Skill | Procedure for generating design docs — used by architect and engineer agents |
| `coding-standards` | Skill | Language conventions — domain knowledge reusable across all coding agents |

Notice the pattern: **agents own the workflow; skills own the expertise.**

### Optimisation pattern: keep agents lean

When writing or reviewing an agent, apply this three-step check:

1. **Identify domain knowledge blocks** — paragraphs that teach the model *how* to do something domain-specific (coding standards, validation rules, formatting conventions).
2. **Check reusability** — could another agent benefit from this same knowledge? If yes, extract to a skill.
3. **Check size** — is the block bloating the agent body beyond what's needed for role clarity? If yes, extract to a skill and replace with a one-line reference.

The resulting agent body should read like a **job description** (who you are, what you do, what you don't do, when you hand off), not like a **textbook** (here's everything you need to know about the tech stack and domain).

### Quick-decision flowchart

```
 Is it about WHO the agent is?  (role, guardrails, workflow, handoffs)
    │
    ├── Yes ──▶  Keep in agent body.
    │
    └── No ──▶  Is it about HOW to do something domain-specific?
                   │
                   ├── Yes ──▶  Could another agent also need this?
                   │               │
                   │               ├── Yes ──▶  Extract to a skill.
                   │               │
                   │               └── No ──▶  Is it > ~30 lines?
                   │                              │
                   │                              ├── Yes ──▶  Extract to a skill.
                   │                              │
                   │                              └── No ──▶  Keep inline.
                   │
                   └── No ──▶  Is it connectivity to an external system?
                                  │
                                  ├── Yes ──▶  Use an MCP server.
                                  │
                                  └── No ──▶  Probably belongs in
                                              copilot-instructions.md
                                              (always-on, cross-agent).
```

### What a skill looks like

If you've never created a skill before, here is the minimal structure. Full details are in the [VS Code skills documentation](https://code.visualstudio.com/docs/copilot/customization/agent-skills).

```
.github/skills/
  my-skill/
    SKILL.md            ← Entry point (required)
    scripts/            ← Optional executable assets
    examples/           ← Optional reference material
```

The `SKILL.md` file has a specific structure:

```markdown
---
name: My Skill
description: One sentence summary shown as metadata in the context window
---

## Instructions

Detailed procedural knowledge the agent reads on demand.

## Directory

- `scripts/transform.py` — Data transformation script
- `examples/good.php` — Example of correct pattern
```

At runtime, only the `name` and `description` appear in the context window (~1 line). The agent reads the full `SKILL.md` content only when it decides the skill is relevant to the current task.

### When NOT to extract to a skill

Not everything belongs in a skill. Keep these in the agent body:

| Keep in agent body | Why |
|--------------------|-----|
| Role-specific guardrails ("DO NOT write code") | These define the agent's identity, not reusable domain knowledge |
| Workflow sequencing (Red → Green → Refactor) | The phase order is integral to this agent's role |
| Handoff logic (when/how to hand off) | Handoffs are an agent concern configured in frontmatter + body |
| Very small domain notes (~5 lines) | Extracting adds overhead without meaningful context savings |

---

## 6. Markdown Body: Structuring Agent Instructions

### Recommended section order

Write sections in this order for consistency across all project agents:

#### 1. Role identity (required)

A single sentence establishing who the agent is.

```markdown
# Software Engineer (TDD & Architecture Focused)

You are a Software Engineer. Your primary goal is to deliver
high-quality, maintainable code while strictly adhering to the project's
established standards and progress tracking.
```

#### 2. Core operational principles

Numbered, named behavioural rules that define HOW the agent works.

```markdown
## Core Operational Principles

### 1. Planning & Governance
- Always follow existing Technical Plans and ADRs.
- If a technical blocker arises, stop and describe the issue.

### 2. Development Workflow (Strict TDD)
Follow Red-Green-Refactor for every feature.
```

#### 3. Guardrails (DO / DO NOT)

Explicit boundaries that prevent role bleed.

```markdown
## Behavioural Guardrails
- **DO NOT** write implementation code (this role gathers requirements only).
- **DO NOT** modify existing files — create new documents only.
- **DO** cite specific requirement sections when making recommendations.
```

#### 4. Workflow steps

Numbered, sequenced actions with expected artefacts at each step.

```markdown
## Workflow
### Phase 1: Evidence Collection
1. Run quality tools to gather objective metrics.
2. Record results in structured format.

### Phase 2: Systematic Audit
1. Review each component for requirement traceability.
2. Check for logic errors and edge cases.
```

#### 5. Handoff protocol

When and how to hand off to the next agent.

```markdown
## Handoff Protocol
After completing the review report, offer the user two options:
- **Fix Issues** → hands off to `@engineer`
- **Update Architecture** → hands off to `@architect`
```

#### 6. Quality gates (for execution agents)

Exact commands that must pass before work is considered done.

````markdown
## Quality Gates
Before committing ANY code changes:
```bash
npm test                     # All tests must pass
npm run lint                 # Linter rules clean
npm run typecheck            # Type checker clean
```
````

#### 7. Domain context

Project-specific knowledge the agent must have.

```markdown
## Project Context
- [Language version], [coding standard], [architecture patterns]
- Root namespace or module path: `YourApp\`
- Key conventions: [e.g. immutable value objects, repository pattern]
```

#### 8. Output format

What artefact(s) the agent produces and where to save them.

```markdown
## Output Format
Save the review report to `docs/REVIEW_YYYY-MM-DD.md`.
Use severity icons: 🔴 Critical, 🟡 High, 🟢 Medium.
```

#### 9. Skill references

List the skills this agent may use and when to trigger them. This is the bridge between the lean agent body and the rich skill library (see [Section 5](#5-agent-vs-skill-decision-framework)).

```markdown
## Available Skills
- **Code Validator** (.github/skills/code-validator/SKILL.md)
- **Style Guide** (.github/skills/style-guide/SKILL.md)
- **Architecture Patterns** (.github/skills/architecture-patterns/SKILL.md)

## When to Apply Skills
- Implementing a domain object? → Load the Architecture Patterns skill
- Running quality checks? → Load the Code Validator skill
- Writing documentation comments? → Load the Style Guide skill
```

#### 10. Shared instruction references

VS Code loads instructions from multiple sources. Use Markdown links to reference them rather than duplicating content:

| File | Scope | Loaded |
|------|-------|--------|
| `.github/copilot-instructions.md` | All agents, all prompts | Always prepended |
| `AGENTS.md` (in any directory) | All agents when working in that directory | Always prepended |
| `.instructions.md` (in any directory) | All agents when working in that directory | Always prepended |
| `.github/agents/*.agent.md` | Only when the specific agent is selected | Always prepended |
| `.github/skills/*/SKILL.md` | Any agent, on demand | Progressive disclosure |

Reference shared standards rather than repeating them:

```markdown
Follow the project coding standards defined in
[copilot-instructions.md](../copilot-instructions.md).
```

> **Key distinction:** `copilot-instructions.md` applies to **all** agents automatically. `AGENTS.md` and `.instructions.md` apply by directory scope. An `.agent.md` body applies only when that agent is selected. Skills are loaded only on demand.

### Writing tips (from official docs)

- **Keep instructions short and self-contained.** One rule per bullet.
- **Include the WHY behind rules.** This helps the model handle edge cases. E.g.: "Use `date-fns` instead of `moment.js` — moment.js is deprecated and increases bundle size."
- **Show preferred and avoided patterns** with concrete code examples.
- **Focus on non-obvious rules.** Skip things linters already enforce.
- **Reference files via Markdown links** instead of duplicating content.

---

## 7. Naming Conventions

| Element | Convention | Example |
|---------|-----------|---------|
| File name | `{lowercase-hyphenated-role}.agent.md` | `code-reviewer.agent.md` |
| `name` field | Plain-English role title (can contain spaces) | `Code Reviewer` |
| `@mention` | Auto-derived from `name` | `@Code Reviewer` |
| Claude format | Plain `.md` in `.claude/agents/` | `.claude/agents/code-reviewer.md` |

**Consistency rule:** The `name` field value must match exactly what other agents reference in their `handoffs[].agent` fields. If your `name` is `Code Reviewer`, then every handoff targeting this agent must use `agent: Code Reviewer`.

---

## 8. Handoff Design

### What handoffs are

Handoffs create **guided sequential workflows**. After a chat response completes, buttons appear that let the user switch to the next agent with a pre-filled prompt. They model lifecycle phase boundaries.

### Design process

1. **Draw the handoff graph first** — sketch which agents hand off to which, and what triggers each transition.
2. **Model handoffs as lifecycle edges** — each edge is a phase boundary (requirements → design → implementation → review).
3. **Support bidirectional cycles** — review agents should hand off back to implementation agents for fix iterations.

### Configuration

```yaml
handoffs:
  - label: Start Implementation           # Button text
    agent: Implementer                     # Target agent's `name` field
    prompt: Begin implementing the plan.   # Pre-filled prompt
    send: false                            # false = user clicks button
                                           # true  = auto-submits
    model: Claude Sonnet 4.5 (copilot)     # Optional: override model
```

### Example handoff graph

```
  Analyst ←──────── Architect
     │                 ↑       │
     └──▶ Architect    │       └──▶ Engineer
                       │            │       │
       Reviewer ──────┘            │       └──▶ Architect
          ↑                         │
          └───── Engineer ◀─────┘
                   (Reviewer: fix issues)
```

Handoff graphs are often a **mesh**, not a linear chain — review agents hand back to both implementation and architecture.

---

## 9. Subagent Architecture

### What subagents are

Subagents are independent AI agents that perform focused work in their **own context window** and report results back to the main agent. They prevent context bloat, enable parallel execution, and allow specialized tool/model configurations.

### When to use subagents

- **Context isolation** — prevent research noise from cluttering the main conversation
- **Parallel analysis** — run multiple review perspectives simultaneously
- **Specialized tools/models** — each subagent can use different tools and a different model
- **Exploratory work** — if the subagent hits a dead end, only its summary affects the main context

### The `agents` frontmatter field

```yaml
# Allow only specific subagents:
agents: ['Planner', 'Implementer', 'Reviewer']

# Allow all agents as subagents (default):
agents: ['*']

# Prevent any subagent use:
agents: []
```

> Explicitly listing an agent in `agents` overrides `disable-model-invocation: true` on the target agent.

### Creating subagent-only agents

Set `user-invokable: false` to hide the agent from the dropdown while keeping it available as a subagent:

```yaml
---
name: Planner
user-invokable: false
tools: ['read/readFile', 'search/codebase']
---
Break down feature requests into implementation tasks.
```

### Orchestration patterns

**Coordinator-worker pattern:**

```yaml
---
name: Feature Builder
tools:
  - read/readFile
  - edit/editFiles
  - edit/createFile
  - search/fileSearch
  - search/textSearch
  - search/codebase
agents: ['Planner', 'Implementer', 'Reviewer']
---
For each feature request:
1. Use the Planner agent to break it into tasks.
2. Use the Implementer agent to write code for each task.
3. Use the Reviewer agent to check the implementation.
4. If the reviewer finds issues, use the Implementer again.
Iterate between review and implementation until converged.
```

**Multi-perspective review pattern:**

```yaml
---
name: Thorough Reviewer
tools:
  - read/readFile
  - search/fileSearch
  - search/textSearch
  - search/codebase
---
Run these subagents in parallel:
- Correctness reviewer: logic errors, edge cases, type issues.
- Security reviewer: input validation, injection risks, data exposure.
- Architecture reviewer: codebase patterns, design consistency.
After all complete, synthesize findings into a prioritized summary.
```

### Subagents vs. skills: complementary, not competing

Subagents and skills solve different problems:

| Mechanism | Solves | Context cost |
|-----------|--------|--------------|
| **Subagent** | Context isolation, parallel execution, specialised tools | Runs in its own context window (free for the parent) |
| **Skill** | Domain expertise, procedural knowledge, reusable scripts | Metadata is ~1 line; full content loaded on demand |

A well-designed agent often uses **both**: skills for what it needs to *know*, subagents for what it needs to *delegate*. For example, a TDD Pipeline coordinator agent delegates Red/Green/Refactor work to subagents (context isolation) while each subagent loads an architecture-patterns skill on demand (domain expertise).

### Key behaviours

- Subagents are **synchronous** — the main agent waits for results.
- VS Code can spawn **multiple subagents in parallel** when appropriate.
- Subagents start with a **clean context window** — they don't inherit conversation history.
- Only the **final summary** is returned to the main agent.

---

## 10. Integrating with the Team Lifecycle

### Example flow

```
@analyst → @architect ⇄ @engineer ⇄ @reviewer
     │           │              │             │
  Requirements   Design       Code        Review
  Document       Docs       + Tests       Report
                  ↑              ↑
                  └── @reviewer ─┘
               (update design)  (fix issues)
```

The flow is typically a **mesh with feedback loops** — review agents can hand back to both architecture and implementation. Standalone agents (e.g. an autonomous problem-solver) may operate independently outside the lifecycle.

### Adding a new agent

| Goal | Approach |
|------|----------|
| New phase in the lifecycle | Insert a new node between existing agents and update handoffs on both neighbours |
| Specialised sub-task within a phase | Create a subagent-only agent (`user-invokable: false`) and reference it from the parent's `agents` list |
| Replace an existing agent | Update all `handoffs[].agent` references across all other agent files |

### What to update when adding an agent

1. Create the new `.agent.md` file in `.github/agents/`
2. Update `handoffs` in upstream and downstream agent files
3. Add a row to the tool matrix table in [README.md](README.md)
4. Add a node to the workflow diagram in [README.md](README.md)
5. Add an entry in the "Available Agents" section of [README.md](README.md)

### Renaming or retiring an agent

The `name` field is the **primary key** other agents use for handoffs and subagent references. Changing or removing it is a breaking change.

**To rename an agent:**

1. Search all `.agent.md` files for the old `name` value in `handoffs[].agent` and `agents` fields
2. Update every reference **atomically** — partial updates break the handoff chain
3. Update [README.md](README.md) entries
4. Reload VS Code and test every affected handoff button

**To retire an agent:**

1. Remove all `handoffs[].agent` references pointing to the agent
2. Remove the agent from any `agents` lists in other files
3. Update [README.md](README.md) (remove from workflow diagram, tool matrix, agent list)
4. Delete the `.agent.md` file
5. Consider whether a replacement agent is needed to maintain workflow continuity

---

## 11. Agent Hooks Integration

### What hooks are

Hooks execute **deterministic shell commands** at key lifecycle points during agent sessions. They complement agents by enforcing policies that instructions alone cannot guarantee.

### Hook file location

```
.github/hooks/*.json
```

### Common patterns for projects with custom agents

| Hook Event | Use Case | Example |
|------------|----------|---------|
| `PreToolUse` | Block destructive commands | Deny `rm -rf` or `DROP TABLE` |
| `PostToolUse` | Run formatters after edits | Run `prettier --write` after file changes |
| `SessionStart` | Inject project context | Add branch name, runtime version, current sprint |
| `Stop` | Require quality gates | Force test suite pass before session ends |
| `SubagentStart` | Track subagent usage | Log which subagents are spawned |

### Example hook configuration

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "type": "command",
        "command": "npx prettier --write .",
        "timeout": 30
      }
    ]
  }
}
```

### Safety consideration

If the agent has access to edit scripts run by hooks, it can modify those scripts during its own run. Use `chat.tools.edits.autoApprove` to require manual approval for hook script edits.

---

## 12. Skills Integration

This section covers the operational details of integrating skills with agents. For the strategic decision of *what* to put in an agent vs. a skill, see [Section 5](#5-agent-vs-skill-decision-framework).

### How skills differ from agent instructions

| Aspect | Agent Instructions | Skills |
|--------|-------------------|--------|
| Portability | VS Code only | VS Code, Copilot CLI, Copilot coding agent |
| Loading | Always prepended | On-demand (progressive disclosure) |
| Content | Instructions only | Instructions + scripts + examples + resources |
| Location | `.github/agents/` | `.github/skills/*/SKILL.md` |

### Referencing skills from agent body

List relevant skills in the agent body so the model knows they exist. Use the pattern from [Section 6, subsection 9](#6-markdown-body-structuring-agent-instructions): an "Available Skills" list with paths, followed by a "When to Apply Skills" trigger map.

### Skill-driven agent optimisation

If you already have an agent whose body has grown large, you can refactor it by extracting domain knowledge into skills. This is the recommended way to scale an agent's capabilities without bloating its permanent context.

#### Before: domain knowledge embedded in agent

```markdown
---
name: Engineer
description: TDD-focused implementation agent
tools: ['read', 'edit', 'search', 'execute', 'todo']
---

# Engineer

You are a Software Engineer focused on TDD ...

## Coding Patterns                      ← 40 lines of domain knowledge
[detailed rules for constructors, validation, design patterns ...]

## Type Checking Rules                  ← 25 lines of domain knowledge
[detailed rules for type hints, generics, strict comparison ...]

## Protocol Compliance                  ← 35 lines of domain knowledge
[detailed data format rules, field validation, API contracts ...]
```

This agent's body permanently occupies ~150+ lines of context on every prompt, even when the task has nothing to do with type checking or protocol compliance.

#### After: lean agent + skills

```markdown
---
name: Engineer
description: TDD-focused implementation agent
tools: ['read', 'edit', 'search', 'execute', 'todo']
---

# Engineer

You are a Software Engineer focused on TDD ...

## Available Skills
- **Code Validator** (.github/skills/code-validator/SKILL.md)
- **Style Guide** (.github/skills/style-guide/SKILL.md)
- **Architecture Patterns** (.github/skills/architecture-patterns/SKILL.md)

## When to Apply Skills
- Implementing a domain object? → Load the Architecture Patterns skill
- Running quality checks? → Load the Code Validator skill
- Writing documentation comments? → Load the Style Guide skill
```

The agent body is now ~30 lines. The three skills add only ~3 metadata lines to the context. When the agent decides it needs architecture knowledge for the current task, it reads the full skill content on demand — and only then.

#### The pattern: agent as coordinator, skills as expertise

```
  Agent (lean)                        Skills (rich)
  ┌─────────────────────┐             ┌───────────────────────┐
  │ Role identity        │──triggers──▶│ code-validator        │
  │ Workflow phases      │             │ style-guide           │
  │ Guardrails           │             │ architecture-patterns │
  │ Handoff rules        │             │ doc-generator         │
  │ Skill references     │             │ testing-patterns      │
  └─────────────────────┘             └───────────────────────┘
        ~30-50 lines                     loaded on demand
```

#### When to split an existing agent

Consider splitting when:

1. **The agent body exceeds ~100 lines** — scan for blocks that are domain procedures rather than role definition.
2. **Multiple agents duplicate the same instructions** — extract the shared parts into a skill both can reference.
3. **Domain knowledge changes faster than the agent's role** — a skill can be versioned and updated without touching the agent file.
4. **You're adding a new capability** — instead of making the agent body longer, create a skill and add a one-line reference.

---

## 13. Prompt File Interaction

### How prompt files relate to agents

Prompt files (`.prompt.md`) are reusable slash commands. A prompt file can specify an `agent` in its frontmatter to run with a specific agent's configuration:

```yaml
---
name: generate-component
agent: Engineer
tools: ['edit', 'search', 'read']
---
Generate a new component following TDD principles for: ${input:componentName}
```

### Tool priority order

See the [tool priority order in Section 4](#4-tool-scoping-guidelines) for how tools are resolved when a prompt file references an agent.

### When to use prompt files vs. agents

- **Prompt file**: A single, repeatable task with a fixed template (e.g., "generate a value object")
- **Agent**: An ongoing persona that handles varied requests within a role

---

## 14. Cross-Platform Compatibility

### VS Code format (primary)

- File: `.github/agents/{name}.agent.md`
- Tools: YAML list of tool identifiers
- Supported by VS Code 1.106+

### Claude Code format

VS Code also detects `.md` files in `.claude/agents/`:

```yaml
---
name: my-agent
description: What it does
tools: "Read, Grep, Glob, Bash"    # Comma-separated string
---
```

VS Code maps Claude-specific tool names to the corresponding VS Code tools.

### Organization-level agents

Define agents at the GitHub organization level for cross-repo sharing. Enable with:

```json
"github.copilot.chat.organizationCustomAgents.enabled": true
```

### Background agent compatibility

Custom agents can run in background (CLI) sessions using Git worktrees. Enable with:

```json
"github.copilot.chat.cli.customAgents.enabled": true
```

Only workspace-level agents are available for background sessions.

### Custom agent file locations

Add additional search paths with:

```json
"chat.agentFilesLocations": [
  ".github/agents",
  ".custom/agents"
]
```

---

## 15. Diagnostics & Troubleshooting

### Using the diagnostics view

Right-click in the Chat view → **Diagnostics**. This shows all loaded agents, tools, instruction files, and any errors.

### Common issues

| Problem | Cause | Fix |
|---------|-------|-----|
| Agent not in dropdown | File not in `.github/agents/`, wrong extension, or YAML parse error | Check location, ensure `.agent.md` extension, validate YAML |
| Agent not using expected tools | Tool name misspelled or tool not available | Verify tool identifiers against the taxonomy table above |
| Handoff button not appearing | Target agent `name` doesn't match `handoffs[].agent` | Ensure exact string match (case-sensitive, including special characters) |
| Subagent not being invoked | `disable-model-invocation: true` on the target, or parent's `agents` list doesn't include it | Check both agent files |
| Instructions not applied | Agent body is empty or malformed YAML breaks parsing | Check YAML validity (no tabs, quoted special chars) |
| "Cannot have more than 128 tools" | Too many tools/MCP servers enabled | Reduce tools list or use tool sets |

### YAML gotchas

- **Use spaces, not tabs** for indentation
- **Quote strings containing special characters** (`:`, `&`, `#`, `{`, `}`)
- **Boolean fields**: use `true`/`false` (not `yes`/`no`)
- **Lists** can be flow-style `['a', 'b']` or block-style with `-`

### Testing your agent

After creating or modifying an agent, validate it with this sequence:

1. **Reload VS Code** (`Ctrl+Shift+P` → "Developer: Reload Window")
2. **Check the dropdown** — verify the agent appears (or doesn't, if `user-invokable: false`)
3. **Open diagnostics** — right-click Chat view → Diagnostics → check for errors
4. **Run a smoke test** — ask the agent a simple question within its role and verify:
   - It follows the guardrails (doesn't do things it shouldn't)
   - It uses the right tools (check the tool-use indicators in the response)
   - It produces output in the expected format
5. **Test handoff buttons** — if the agent has `handoffs`, click each button and verify it switches to the correct agent with the correct pre-filled prompt
6. **Test subagent invocation** — if the agent uses subagents, trigger a task that should delegate work and verify the subagents are spawned
7. **Test skill loading** — if the agent references skills, trigger a task that requires domain knowledge and verify the skill is read (you'll see `read_file` calls to the `SKILL.md` path)

> **Tip:** Keep a short checklist of test scenarios for each agent so you can re-run them after changes.

### Security considerations

- **Never embed secrets** (API keys, tokens, passwords) in agent instructions — they are stored in plain text and version-controlled
- **Be cautious with `execute/runInTerminal`** — an agent with terminal access can run arbitrary commands. Only grant this to trusted roles
- **Audit MCP server access** — `<server>/*` grants access to all tools from an MCP server. Prefer granting specific tools when possible
- **Review agent instructions for prompt injection vectors** — if agent instructions reference user-supplied content (e.g., issue titles, PR descriptions), ensure the instructions don't make the agent blindly execute content from those sources
- **Use `chat.tools.edits.autoApprove` carefully** — auto-approving edits means the agent can modify any file without confirmation, including scripts that hooks may execute

---

## 16. Validation Checklist

Before committing a new or modified agent:

- [ ] YAML frontmatter parses without error (test with a YAML validator)
- [ ] `name` field matches the `handoffs[].agent` value used by other agents
- [ ] `description` is a single, clear sentence in active voice
- [ ] `tools` list follows least-privilege for the role
- [ ] `model` field uses a valid model name (check the model picker dropdown)
- [ ] `agents` list is intentionally set (not accidentally left as `*`)
- [ ] Body contains: role identity, guardrails, workflow, output format
- [ ] Agent appears in VS Code chat dropdown after window reload
- [ ] Handoff buttons render and switch context correctly (test each one)
- [ ] Diagnostics view shows no errors for this agent
- [ ] Run a test conversation to verify behaviour matches intent
- [ ] [README.md](README.md) updated:
  - [ ] "Available Agents" section entry added
  - [ ] Tool matrix row added
  - [ ] Workflow diagram node added
  - [ ] "Agent Configuration" table updated
- [ ] Skills referenced in agent body actually exist in `.github/skills/`
- [ ] Agent body is lean: domain knowledge extracted to skills where possible (see [Section 5](#5-agent-vs-skill-decision-framework))
- [ ] Other agents' `handoffs` updated if this agent is a new lifecycle node

---

## 17. Anti-Patterns to Avoid

### Over-permissioning tools

Giving `edit/editFiles` to a read-only reviewer violates least-privilege and risks unintended code changes.

### Vague `description` fields

A description like "Helps with code" doesn't help the model select the correct agent for subagent use, and doesn't help users choose the right agent from the dropdown.

**Bad:** `description: Helps with code`

**Good:** `description: Provide rigorous, evidence-based critiques of code implementations`

### Missing guardrails (role bleed)

Without explicit DO/DO NOT rules, analysts write code, engineers skip TDD, and auditors modify files. Always include a guardrails section.

### Duplicating instructions

If content already exists in `copilot-instructions.md` or `.instructions.md` files, reference it via Markdown link rather than copying it into the agent body.

### Using deprecated fields

The `infer` field is deprecated. Use `user-invokable` and `disable-model-invocation` for independent control over dropdown visibility and subagent availability.

### Forgetting to update README

The [README.md](README.md) is the source of truth for the agent team. If you add or modify an agent and don't update the README, team members won't know about the change and handoffs may break.

### Bloating agents with domain knowledge

Embedding large blocks of procedural knowledge (coding standards, protocol rules, validation checklists) directly in the agent body wastes context on every prompt — even when irrelevant to the current task. Extract domain knowledge into skills and reference them from the agent body. See [Section 5](#5-agent-vs-skill-decision-framework) for the decision framework and [Section 12](#12-skills-integration) for the before/after pattern.

**Smell:** The agent body reads like a textbook rather than a job description.

### Creating overly broad subagent access

Leaving `agents: ['*']` (the default) means any agent can be invoked as a subagent. For focused workflows, explicitly list allowed subagents to prevent the model from selecting the wrong one.

---

## 18. Worked Example Templates

### Template A: Minimal read-only agent

```markdown
---
name: Documentation Reviewer
description: Review project documentation for accuracy, completeness, and consistency
argument-hint: Specify the document or area to review
tools:
  - read/readFile
  - search/listDirectory
  - search/fileSearch
  - search/textSearch
  - search/codebase
  - todo
agents: []
model: Claude Sonnet 4.5 (copilot)
user-invokable: true
handoffs:
  - label: Fix Documentation
    agent: Engineer
    prompt: Please fix the documentation issues identified in the review.
    send: false
---

# Documentation Reviewer

You are a Documentation Reviewer. Your goal is to ensure all project
documentation is accurate, complete, and consistent with the codebase.

## Behavioural Guardrails

- **DO NOT** modify any files — document findings only.
- **DO NOT** write or suggest code changes.
- **DO** cite specific file paths and line numbers for every finding.
- **DO** check that code examples in docs actually match the codebase.

## Available Skills
- **Code Validator** (.github/skills/code-validator/SKILL.md)
- **Doc Generator** (.github/skills/doc-generator/SKILL.md)

## When to Apply Skills
- Reviewing source code docs? → Load the Code Validator skill for standards reference
- Checking design doc completeness? → Load the Doc Generator skill for expected structure

## Workflow

### Phase 1: Scope Assessment
1. List all documentation files (docs/, README.md, ADRs).
2. Create a todo list tracking which documents to review.

### Phase 2: Systematic Review
For each document, check:
- Technical accuracy (does the doc match the code?)
- Completeness (are all public APIs documented?)
- Consistency (naming, formatting, cross-references)
- Currency (are version numbers and dates current?)

### Phase 3: Report
Summarise findings as a prioritised list with:
- 🔴 Incorrect information (factual errors)
- 🟡 Missing information (gaps)
- 🟢 Style/formatting issues

## Output Format
Present findings in chat as a structured list grouped by document.
```

### Template B: Full-featured coordinator with subagents

```markdown
---
name: TDD Pipeline
description: Orchestrate test-driven development using Red-Green-Refactor subagents
argument-hint: Describe the feature to implement via TDD
tools:
  - read/readFile
  - edit/editFiles
  - edit/createFile
  - search/listDirectory
  - search/fileSearch
  - search/textSearch
  - search/codebase
  - read/problems
  - execute/runTests
  - execute/runInTerminal
  - todo
agents: ['Red', 'Green', 'Refactor']
model: Claude Sonnet 4.5 (copilot)
user-invokable: true
handoffs:
  - label: Review Code Quality
    agent: Reviewer
    prompt: Review the TDD implementation for quality and security issues.
    send: false
---

# TDD Pipeline Coordinator

You are a TDD Pipeline Coordinator. You orchestrate test-driven development
by delegating to three specialised subagents in sequence.

## Core Operational Principles

### 1. Strict Phase Discipline
Never skip a phase. Always: Red → Green → Refactor.

### 2. Subagent Delegation
Delegate ALL implementation work to subagents. Your role is coordination only.

### 3. Quality Gate Enforcement
After each phase, verify quality gates pass before proceeding.

## Behavioural Guardrails

- **DO NOT** write tests or code directly — delegate to subagents.
- **DO** verify quality gates between each phase.
- **DO** create a todo list tracking each TDD cycle.

## Available Skills
- **Code Validator** (.github/skills/code-validator/SKILL.md)
- **Architecture Patterns** (.github/skills/architecture-patterns/SKILL.md)
- **Style Guide** (.github/skills/style-guide/SKILL.md)

## When to Apply Skills
- Implementing a domain object? → Ensure subagents load the Architecture Patterns skill
- Running quality checks? → Load the Code Validator skill
- Writing documentation comments? → Load the Style Guide skill

## Workflow

### Step 1: Understand the Feature
Read relevant source files and requirements to understand what needs to be built.

### Step 2: Red Phase
Use the **Red** subagent to write failing tests that define the desired behaviour.
Verify the tests actually fail.

### Step 3: Green Phase
Use the **Green** subagent to implement the minimum code to make tests pass.
Verify all tests pass.

### Step 4: Refactor Phase
Use the **Refactor** subagent to improve code quality while keeping tests green.
Verify all tests still pass.

### Step 5: Quality Gates
Run full quality suite:
```bash
npm test
npm run lint
npm run typecheck
```

### Step 6: Iterate or Complete
If more features remain, return to Step 2.
Otherwise, offer the handoff to @reviewer.

## Output Format
After each TDD cycle, report:
- Tests added (count and names)
- Code added/changed (files and line counts)
- Quality gate results (pass/fail)
```

> **Note:** The subagent files (`Red.agent.md`, `Green.agent.md`, `Refactor.agent.md`) would each have `user-invokable: false` and a minimal tool set appropriate for their phase.

---

## 19. References

### Official VS Code documentation

- [Custom agents](https://code.visualstudio.com/docs/copilot/customization/custom-agents) — file structure, frontmatter schema, creation workflow
- [Agent tools](https://code.visualstudio.com/docs/copilot/agents/agent-tools) — tool types, approval, terminal commands, tool sets
- [Subagents](https://code.visualstudio.com/docs/copilot/agents/subagents) — orchestration patterns, parallel execution, context isolation
- [Background agents](https://code.visualstudio.com/docs/copilot/agents/background-agents) — CLI sessions, Git worktrees
- [Custom instructions](https://code.visualstudio.com/docs/copilot/customization/custom-instructions) — `copilot-instructions.md`, `AGENTS.md`, `.instructions.md`
- [Agent hooks](https://code.visualstudio.com/docs/copilot/customization/hooks) — lifecycle events, JSON configuration
- [Agent skills](https://code.visualstudio.com/docs/copilot/customization/agent-skills) — `SKILL.md` format, progressive disclosure
- [Prompt files](https://code.visualstudio.com/docs/copilot/customization/prompt-files) — `.prompt.md` format, variables, tool priority

### Community resources

- [github/awesome-copilot](https://github.com/github/awesome-copilot) — 100+ community-contributed agents, instructions, skills, and hooks
