# The Skill Writer's Guide

> **Purpose:** A comprehensive, project-agnostic guide for writing Agent Skills — the open
> standard from [agentskills.io](https://agentskills.io) — for GitHub Copilot, Claude Code,
> and any skills-compatible agent.
>
> **Companion to:** [Copilot Session-to-Knowledge Feedback Guide](copilot-session-feedback-guide.md)
> — which defines *when* to create a skill. This guide covers *how* to write one well.
>
> **Revision:** v3 — 2026-03-01 | **Audience:** Any developer using a skills-compatible agent

---

## Table of Contents

- [How to Use This Guide](#how-to-use-this-guide)
- [1. Introduction — What Skills Are and Why They Matter](#1-introduction--what-skills-are-and-why-they-matter)
- [2. When to Write a Skill (Routing)](#2-when-to-write-a-skill-routing)
- [3. Anatomy of a Skill](#3-anatomy-of-a-skill)
- [4. Core Principles](#4-core-principles)
- [5. The Skill Creation Process — Six Steps](#5-the-skill-creation-process--six-steps)
- [6. Progressive Disclosure Patterns (Deep Dive)](#6-progressive-disclosure-patterns-deep-dive)
- [7. Writing Effective Descriptions (Trigger Engineering)](#7-writing-effective-descriptions-trigger-engineering)
- [8. Writing Effective Body Content](#8-writing-effective-body-content)
- [9. Bundled Resources — Scripts, References, Assets](#9-bundled-resources--scripts-references-assets)
- [10. Testing and Validation](#10-testing-and-validation)
- [11. Iteration and Evolution](#11-iteration-and-evolution)
- [12. Anti-Patterns Gallery](#12-anti-patterns-gallery)
- [13. Examples and Case Studies](#13-examples-and-case-studies)
- [14. Integration with the Feedback Loop](#14-integration-with-the-feedback-loop)
- [15. Naming Conventions](#15-naming-conventions)
- [16. Security Considerations](#16-security-considerations)
- [17. Distribution and Discovery](#17-distribution-and-discovery)
- [18. Debugging and Troubleshooting](#18-debugging-and-troubleshooting)
- [19. Skill Composition](#19-skill-composition)
- [20. Glossary](#20-glossary)
- [21. Quick-Reference Card](#21-quick-reference-card)

---

## How to Use This Guide

This document is a comprehensive reference (~2,200 lines). Use it in layers based on your role:

| Reader | Path | Sections |
|--------|------|----------|
| **First-time skill author** | Start to finish | All sections in order (1 → 21) |
| **Experienced author (quick reference)** | Jump to specifics | §3 Anatomy, §7 Descriptions, §21 Quick-Reference Card |
| **Decision maker ("should I write a skill?")** | Routing only | §1 Introduction, §2 Routing |
| **Migrating existing docs** | Conversion path | §11 Iteration (migration subsection), §9 Resources, §10 Testing |

### Section Dependency Diagram

Arrows show prerequisite knowledge. Sections without arrows can be read independently.

```
Standalone (no prerequisites):  §1 Introduction, §2 Routing,
  §14 Feedback Loop, §17 Distribution, §20 Glossary, §21 Quick-Ref

Core knowledge chain:
  §3 Anatomy ──→ §4 Principles ──→ §7 Descriptions ──→ §8 Body Content
       │                │                                      │
       │                ▼                                      ▼
       │         §15 Naming                             §5 Six-Step Process
       │                                                      │
       ▼                                               ┌──────┼──────┐
  §9 Resources                                         ▼      ▼      ▼
       │                                          §6 Disc.  §10 Test  §16 Security
       ▼                                                      │
  §19 Composition                                      ┌──────┴──────┐
                                                       ▼             ▼
                                                 §11 Iteration  §18 Debug

  §12 Anti-Patterns ◄── synthesised from all above
  §13 Examples      ◄── applies all above
```

Each section ends with a boxed **Key Takeaway** callout (1–2 sentences) summarising the essential insight.

---

## 1. Introduction — What Skills Are and Why They Matter

### Skills as Transferable Procedural Memory

An agent skill is a self-contained package that teaches an agent how to perform a specific task. It captures your expertise — the multi-step procedures, domain knowledge, decision logic, and scripts you would otherwise explain (or re-explain) every session — and makes it available on demand.

Think of building a skill like writing an onboarding guide for a new hire. You capture your expertise once so that any agent can perform the task repeatably, without you being in the room. Day 1, a fresh agent knows nothing about your domain. Day 30, the same agent — equipped with your skill library — dramatically outperforms on tasks that require your team's specific workflows.

Skills teach the agent *how* to perform a task, not just *what* to know. This is the distinction between a skill (procedural) and an instruction file (declarative). An instruction says "always use PSR-12 coding standards." A skill says "here's how to generate a value object following our conventions: Step 1, validate the inputs; Step 2, generate the class with these patterns; Step 3, run PHPStan to verify."

### An Open Standard

Agent Skills is an open standard developed by Anthropic and released at [agentskills.io](https://agentskills.io). It is adopted by a growing ecosystem of tools:

- **GitHub Copilot** (VS Code, CLI, coding agent)
- **Claude Code**, **Claude.ai**, **Claude API**
- **Cursor**, **Roo Code**, **Gemini CLI**, **Goose**, **Factory**, and more

A skill written for one tool works in any other compatible tool. Write once, use everywhere.

### How Skills Compare to Other Surfaces

Skills are one of several ways to customise agent behaviour. Each surface has a distinct purpose:

| Surface | What It Does | Analogy |
|---------|-------------|---------|
| **Instructions** (`copilot-instructions.md`) | Declarative rules the agent always follows | Company policy handbook |
| **Conditional instructions** (`*.instructions.md`) | Rules that apply to specific file types or events | Department-specific policy |
| **Agents** (`*.agent.md`) | Specialised personas with distinct expertise | Team member with a specific role |
| **Prompts** (`*.prompt.md`) | One-shot reusable commands | A form you fill out and submit |
| **Skills** (`SKILL.md`) | Procedural expertise loaded on demand | Onboarding guide for a complex task |
| **Hooks** (JSON config) | Deterministic actions triggered by events | Automated workflow (CI/CD trigger) |
| **MCP servers** | External tool integrations | API client library |

### Composability

Don't build one skill that does everything. Build multiple focused skills that the agent loads as needed. A "code-review" skill, a "testing" skill, and a "deployment" skill compose into a full workflow — each loaded only when relevant, each maintainable independently. See §19 for detailed composition patterns and anti-patterns.

### Who This Guide Is For

Any developer using a skills-compatible agent — GitHub Copilot in VS Code, Claude Code, Cursor, or any other tool that supports the Agent Skills standard. No prerequisite knowledge is required beyond familiarity with Markdown and YAML.

If you want to know whether a skill is the right artefact for your needs, start with §2 (Routing). If you want to jump straight into writing one, start with §3 (Anatomy).

> **Key Takeaway:** Skills are transferable procedural memory — write once, use across any compatible agent.

---

## 2. When to Write a Skill (Routing)

Before investing in writing a skill, confirm it is the right artefact. A skill solves a specific category of problem; other integration surfaces exist for other categories. Choosing the wrong surface wastes effort and can degrade agent performance.

### The Key Decision Gate

> **Is it procedural expertise that benefits from bundled resources and semantic auto-loading?**

If yes → write a skill. If no → use the correct alternative surface.

### Heuristic Checklist — Write a Skill When:

- [ ] The knowledge is a **multi-step procedure** (not a single rule).
- [ ] It is **reusable** across projects, tools, or sessions.
- [ ] It needs **bundled resources** (scripts, references, assets).
- [ ] It benefits from **semantic auto-loading** (the agent decides when to use it) rather than always-on inclusion.
- [ ] The procedure would otherwise be **rewritten or re-explained** every session.

### When NOT to Write a Skill

If the knowledge fits one of these categories, use the listed alternative instead:

| Knowledge Type | Right Surface | Example |
|---------------|---------------|---------|
| Global coding standards and project rules | `copilot-instructions.md` | "Use PSR-12", "Always use strict types" |
| File-type-specific rules | `*.instructions.md` with `applyTo` glob | "PHP files must have this file header" |
| Specialised persona | `*.agent.md` | Security auditor, database architect |
| One-shot reusable command | `*.prompt.md` | Generate boilerplate, create a ticket template |
| Deterministic lifecycle action | Hook JSON | Pre-commit lint, auto-format on save |
| External API integration | MCP server | Database queries, GitHub API calls, Slack notifications |

### VS Code Customisation Surface Comparison

Quick reference for all seven integration surfaces:

| Surface | Scope | Loading | Use Case |
|---------|-------|---------|----------|
| `copilot-instructions.md` | Always-on, whole project | Automatic, every session | Coding standards, naming conventions, project rules |
| `*.instructions.md` | Conditional (glob/event match) | When condition matches | File-type-specific rules, language overrides |
| `*.agent.md` | Specialised persona | Manual invocation via `@agent` | Reviewer, architect, security auditor |
| `*.prompt.md` | One-shot command | Manual invocation via `/prompt` | Generate boilerplate, create ticket |
| `SKILL.md` | Procedural expertise | Semantic auto-load + `/skill-name` | Multi-step workflows, domain knowledge with resources |
| Hook JSON | Deterministic action | Lifecycle event trigger | Pre-commit checks, auto-format, notifications |
| MCP server | External tool | Tool discovery + agent invocation | API calls, database queries, external services |

### Routing Decision Tree

For the full visual routing decision tree (Mermaid diagram), see the [Session Feedback Guide — Routing Decision Tree](copilot-session-feedback-guide.md#section-5--routing-decision-tree).

A simplified version:

```
Is it a single declarative rule?
  → Yes: copilot-instructions.md or *.instructions.md
  → No: Is it a multi-step procedure?
     → No: Is it a persona? → *.agent.md
            Is it a one-shot command? → *.prompt.md
            Is it a lifecycle action? → Hook JSON
            Is it an API integration? → MCP server
     → Yes: Does it benefit from bundled resources (scripts, references)?
        → Yes: SKILL.md ✓
        → No: Can it be a prompt file? → *.prompt.md
               Otherwise: SKILL.md ✓ (simpler skills without resources are still valid)
```

> **Key Takeaway:** If it's not a multi-step procedure that benefits from bundled resources, it's not a skill.

---

## 3. Anatomy of a Skill

Every skill is a directory containing a required SKILL.md file and optional bundled resources. This section is the structural reference — master these components first, then apply the principles from §4 onward.

### 3a. Directory Structure

```
.github/skills/<skill-name>/
├── SKILL.md            # Required — frontmatter + procedural body
├── scripts/            # Optional — executable code (Python, Bash, etc.)
├── references/         # Optional — on-demand documentation
└── assets/             # Optional — output resources (templates, images)
```

The directory name must match the `name` field in the SKILL.md frontmatter exactly.

### 3b. Skill Locations

Skills can be stored in four places. Choose based on scope and audience:

| Location | Scope | Use When |
|----------|-------|----------|
| **Project skills** — `.github/skills/`, `.claude/skills/`, `.agents/skills/` | Team-shared, version-controlled | The skill is relevant to this repository's workflows |
| **Personal skills** — `~/.copilot/skills/`, `~/.claude/skills/`, `~/.agents/skills/` | Individual, not committed | The skill reflects personal preferences or cross-project workflows |
| **Extension-contributed skills** — registered via `chatSkills` in extension `package.json` | Distributable via marketplace | The skill should be installable by anyone via the VS Code Marketplace |
| **Configurable locations** — `chat.agentSkillsLocations` VS Code setting | Custom, cross-project | Skills are stored centrally (e.g., a shared skills monorepo) |

### 3c. SKILL.md — Frontmatter (YAML)

The frontmatter is a YAML block between `---` delimiters at the top of SKILL.md. It contains metadata that the agent reads during discovery.

#### Spec-Standard Fields (agentskills.io)

| Field | Required | Constraint | Description |
|-------|----------|-----------|-------------|
| `name` | Yes | 1–64 chars, lowercase alphanumeric + hyphens, no leading/trailing/consecutive hyphens, must match directory name, no XML tags, no reserved words (`anthropic`, `claude`) | Unique skill identifier. Appears as the slash command name. |
| `description` | Yes | 1–1,024 chars, non-empty, no XML tags | Discovery text — the primary triggering mechanism. See §7 for detailed guidance. |
| `license` | No | Free text | License name or reference to a bundled LICENSE file. |
| `compatibility` | No | Max 500 chars | Environment requirements: platform, packages, network dependencies. |
| `metadata` | No | Key-value map (string → string) | Arbitrary metadata (e.g., `version`, `author`). Use unique key names. |
| `allowed-tools` | No | Space-delimited list | Pre-approved tools the skill may invoke (experimental; varies by implementation). |

#### VS Code Extension Fields (GitHub Copilot-Specific)

| Field | Required | Default | Description |
|-------|----------|---------|-------------|
| `argument-hint` | No | — | Hint text shown in the chat input when invoked as `/skill-name`. |
| `user-invokable` | No | `true` | Show the skill in the `/` slash command menu. Set `false` to hide it from users. |
| `disable-model-invocation` | No | `false` | Prevent the agent from auto-loading this skill. Set `true` for manual-only activation. |

#### Invocation Control Matrix

These two VS Code fields combine to control how a skill can be activated:

| `user-invokable` | `disable-model-invocation` | Slash command? | Auto-load? | Use Case |
|---|---|---|---|---|
| `true` (default) | `false` (default) | Yes | Yes | General-purpose skills — activated by user or agent |
| `false` | `false` | No | Yes | Background knowledge — agent loads when relevant, user cannot invoke directly |
| `true` | `true` | Yes | No | On-demand only — user must explicitly invoke via `/skill-name` |
| `false` | `true` | No | No | Effectively disabled — neither user nor agent activates it |

### 3d. SKILL.md — Body (Markdown)

The body is the Markdown content below the frontmatter. It contains the procedural instructions the agent follows once the skill activates.

**Constraints:**
- Maximum 500 lines (specification limit). Prefer under 200 for optimal performance.
- No format restrictions — write whatever helps agents perform effectively.
- Use imperative/infinitive form: "Extract the metadata", not "The metadata should be extracted".

**Recommended content:**
- Step-by-step instructions for the skill's core procedure.
- Decision logic (tables, if/then branches) for variant workflows.
- Input/output examples for ambiguous transformations.
- References to bundled resources with clear "when to read" guidance.

**What to exclude from the body:**
- Information the agent already knows (well-known concepts, common programming patterns).
- "When to Use This Skill" sections — that information belongs in the `description` field, which is the only content read during discovery. By the time the body loads, activation has already occurred.

### 3e. Bundled Resources

Three optional subdirectories extend the skill beyond what SKILL.md alone can provide:

| Directory | Purpose | Loading Behaviour | Token Cost |
|-----------|---------|-------------------|------------|
| `scripts/` | Executable code for deterministic, repetitive tasks | Executed without reading into context | Lowest — output only |
| `references/` | Documentation loaded on demand via `read_file` | Loaded when the agent determines relevance | Variable — depends on file size |
| `assets/` | Files used in output (templates, images, boilerplate) | Not loaded into context — copied or modified directly | Zero |

**Guidelines for each type:**
- **Scripts:** Test by actually running them. Use command-line arguments, not interactive prompts. Include `--help` output.
- **References:** Structure files >100 lines with a table of contents. For files >10K words, include grep search patterns in SKILL.md.
- **Assets:** Organize in subdirectories by purpose. Use descriptive filenames.

### 3f. What NOT to Include

A skill should contain only files that directly support its functionality. Do not add:

- `README.md`, `INSTALLATION_GUIDE.md`, `CHANGELOG.md`, or similar documentation.
- User-facing documentation or auxiliary context about the creation process.
- Setup/testing procedures for the skill itself.

These add clutter without serving the agent. The skill is for the agent, not for human readers.

### 3g. Extension-Contributed Skills

VS Code extensions can register skills via the `chatSkills` contribution point in `package.json`:

```json
{
  "contributes": {
    "chatSkills": [
      {
        "path": "./skills/my-skill/SKILL.md"
      }
    ]
  }
}
```

Extension-contributed skills follow the same SKILL.md format as project and personal skills. The `name` field must match the parent directory name.

> **Key Takeaway:** Everything starts with SKILL.md — master the frontmatter fields and directory structure before writing any content.

---

## 4. Core Principles

Five design principles govern every skill decision. Internalise these before writing your first line of SKILL.md.

### 4a. Concise Is Key — The Context Window as a Public Good

The context window is a shared, finite resource. Skills compete for space with the system prompt, conversation history, other skills' metadata, workspace files, and the user's actual request. Together, instructions and skills can consume 10–15% of the context window before the agent even starts working.

**Default assumption: the agent is already very smart.** It knows how to write code, follow conventions, and reason about problems. Only add information the agent cannot already know — your domain-specific procedures, your team's conventions, your project's schemas.

Challenge every piece of content with two questions:

1. "Does the agent really need this explanation?"
2. "Does this paragraph justify its token cost?"

Prefer concise examples over verbose explanations. A 3-line code sample often communicates more effectively than a 20-line prose description.

### 4b. Degrees of Freedom

Match the level of specificity in your instructions to the task's fragility and variability:

| Freedom Level | Form | Use When | Example |
|---------------|------|----------|---------|
| **High** | Text-based instructions | Multiple approaches are valid; decisions depend on context; heuristics guide the approach | "Review the code for security issues, focusing on input validation and authentication" |
| **Medium** | Pseudocode or scripts with parameters | A preferred pattern exists; some variation is acceptable; configuration affects behaviour | "Generate a migration using `scripts/migrate.py --type <alter\|create> --table <name>`" |
| **Low** | Exact scripts, few parameters | Operations are fragile and error-prone; consistency is critical; a specific sequence must be followed | "Run `scripts/rotate_pdf.py <input> <degrees>` — do not attempt manual rotation" |

Think of the agent as walking a path:
- A **narrow bridge with cliffs** needs specific guardrails (low freedom).
- An **open field** allows many valid routes (high freedom).

When in doubt, start with higher freedom. If the agent consistently makes poor choices, constrain further.

### 4c. Progressive Disclosure — Three-Level Loading

Skills use a three-level loading strategy to manage context efficiently:

| Level | What Loads | When | Token Budget |
|-------|-----------|------|-------------|
| **1 — Discovery** | `name` + `description` only | Always (for all installed skills) | ~100 tokens per skill |
| **2 — Body** | Full SKILL.md Markdown content | When the agent decides this skill is relevant | <5,000 tokens (max 500 lines) |
| **3 — On-demand resources** | Files from `references/`, output from `scripts/` | When the agent reads or executes them | Unlimited (scripts execute without entering context) |

This matters because:
- A workspace may have 50–100 installed skills. At Level 1, the agent scans all their descriptions (~5,000–10,000 tokens) to decide which to activate.
- Only activated skills pay the Level 2 cost.
- Level 3 content loads only when the agent explicitly requests it.

Design with this hierarchy in mind: put discovery triggers in the description, procedures in the body, and deep reference material in `references/`.

### 4d. Test with Multiple Models

Skills must work across model capabilities. Small models (Haiku-class) benefit from more explicit, step-by-step guidance. Large models (Opus-class) can be over-directed by too much detail — they may follow instructions too rigidly when flexibility is appropriate.

**Rule of thumb:** If a skill works on the smallest model your team uses, it will work everywhere. Test the same skill with at least two different model sizes to calibrate the degree of freedom.

Practical approach:
1. Write the skill for your primary model.
2. Test on a smaller model — if it struggles, add more specific steps.
3. Re-test on the larger model — if it becomes too rigid, move detail to `references/`.

### 4e. Content Hygiene

Three rules that prevent skills from degrading over time:

**Avoid time-sensitive information.** Dates, version numbers, and API endpoint URLs change. Instead of hardcoding `"Use API v3.2 at https://api.example.com/v3.2"`, write `"Look up the current API version in the project's configuration"`.

**Use consistent terminology.** Pick one term and use it everywhere in the skill. If you call it "record" in one place, don't call it "entry" in another. Inconsistent vocabulary confuses the agent and leads to misinterpretation.

**Solve, don't punt.** The skill should actually perform the task — not describe how to do it and then ask the user to confirm each step. If a script can do it deterministically, bundle the script and instruct the agent to run it.

> **Key Takeaway:** Every line in a skill must justify its token cost. When in doubt, leave it out.

---

## 5. The Skill Creation Process — Six Steps

This is the procedural heart of the guide. Follow these steps from idea to shipping skill.

### Step 1: Understand the Skill with Concrete Examples

Start from **concrete usage scenarios**, not abstract descriptions. Ask:

- "What functionality should this skill support?"
- "What would a user say that should trigger this skill?"
- "What does success look like? What would the agent produce?"
- "Can you give 3 examples of real tasks this skill would handle?"

Generate example interactions if working alone:

| User Says | Skill Should Do |
|-----------|----------------|
| "Add docblocks to this class" | Read the class, generate PHPDoc for each method, apply changes |
| "Document this controller" | Analyse parameters and return types, write method-level docblocks |
| "Annotate the model with @property tags" | Inspect the schema, add `@property` tags to the class docblock |

**Conclude this step** when you have a clear list of 3–5 concrete scenarios covering the simple case, a medium-complexity case, and at least one edge case.

### Step 2: Plan Reusable Contents

For each scenario, analyse:

1. **How would you execute this from scratch?** What steps, what tools, what knowledge?
2. **What would be helpful to have ready for doing this repeatedly?** Scripts, reference docs, templates?

Map scenarios to resource types:

| Scenario | Repetitive Element | Resource Type | Path |
|----------|--------------------|---------------|------|
| Rotate a PDF | Same rotation code each time | Script | `scripts/rotate_pdf.py` |
| Build a frontend app | Same HTML/React boilerplate each time | Asset | `assets/hello-world/` |
| Query BigQuery | Re-discovering table schemas each time | Reference | `references/schema.md` |
| Generate a migration | Same migration template each time | Script + Template | `scripts/migrate.py` + `assets/migration.stub` |

**Output:** A list of resources to include — scripts, references, and assets — with clear justification for each.

### Step 3: Initialise the Skill

Create the skill directory and scaffold:

**Manual approach:**
```
mkdir -p .github/skills/my-skill-name
touch .github/skills/my-skill-name/SKILL.md
```

**Automated approach** (if `init_skill.py` is available):
```bash
scripts/init_skill.py my-skill-name --path .github/skills
```

This generates the SKILL.md template with frontmatter and example resource directories. After initialisation, delete any example files you don't need.

**Resulting scaffold:**
```
.github/skills/my-skill-name/
├── SKILL.md
├── scripts/        (if needed)
├── references/     (if needed)
└── assets/         (if needed)
```

### Step 4: Edit the Skill

Work in this order — resources first, then metadata, then body. Steps 4b–4c reference §7, §8, and §15 — read those sections first if this is your first skill, or follow the cross-references as you go.

#### 4a. Start with Bundled Resources

Implement the scripts, references, and assets identified in Step 2:

- **Scripts:** Write, then test by actually running them. Verify output matches expectations. If you have many similar scripts, test a representative sample.
- **References:** Write the documentation content. Structure files >100 lines with a table of contents.
- **Assets:** Add templates, images, or boilerplate. Organise in subdirectories by purpose.

Delete any scaffold example files you don't need.

#### 4b. Write the Frontmatter

Craft the `name` and `description` with care:

- **Name:** Follow the conventions in §15 (gerund form, 1–64 chars, lowercase + hyphens).
- **Description:** Follow the trigger engineering guidance in §7 (three-part formula, third person, trigger keywords).

Add optional fields only when needed:
- `license` — if distributing the skill.
- `compatibility` — if the skill requires specific runtimes or packages.
- `metadata` — for version tracking or authorship.

#### 4c. Write the Body

Apply the body content patterns from §8:

1. Open with a one-line purpose statement (for orientation, not triggering).
2. Write the core procedure using the appropriate pattern (workflow checklist, feedback loop, conditional workflow, etc.).
3. Reference bundled resources with explicit "when to read/run/copy" guidance.
4. Keep under 200 lines when possible; 500 is the hard maximum.
5. Apply progressive disclosure patterns (§6) — move detail to `references/` when the body grows too long.

#### 4d. Apply Progressive Disclosure

If the body exceeds 200 lines, or handles multiple variants/domains, split content:

- Core workflow stays in SKILL.md body.
- Variant-specific details go to `references/` (see §6 for patterns).
- Reference each file from the body with clear navigation cues.

### Step 5: Validate the Skill

Before sharing, validate both structure and behaviour:

**Structural validation:**
- `name` matches directory name.
- `description` ≤ 1,024 characters.
- Body ≤ 500 lines.
- No extraneous files (README.md, CHANGELOG.md, etc.).

**Automated validation** (if `skills-ref` CLI is available):
```bash
skills-ref validate .github/skills/my-skill-name
```

**Functional validation** (see §10 for the full testing protocol):
- Trigger test: ask the agent something that should activate the skill.
- Negative trigger test: ask something that should NOT activate it.
- Procedure test: follow the skill's steps and verify the output.

### Step 6: Iterate

Skills improve through use. The iteration cycle:

```
Use → Notice struggles → Identify improvements → Implement → Test → Repeat
```

**Evaluation-driven development** (build evaluations before writing):
1. Create 3 representative scenarios (simple, medium, edge case).
2. Run the agent on those scenarios **without** the skill — establish a baseline.
3. Write the minimal skill body that improves on the baseline.
4. Re-run the scenarios — measure improvement.
5. Iterate: add detail only where the agent still struggles.

This prevents over-writing and ensures every line justifies its token cost.

**Claude A/B iteration pattern:**
- **Agent A (author):** writes and refines the skill.
- **Agent B (tester):** executes the skill on fresh tasks, unaware of design intent.
- Agent B's struggles reveal unclear instructions, missing steps, or assumptions the author didn't notice.
- Iterate until Agent B succeeds consistently without additional guidance.

Capture iteration insights and feed them back through the [session feedback loop](copilot-session-feedback-guide.md#section-3--analysing-session-outputs-four-diagnostic-lenses).

> **Key Takeaway:** Build evaluations before writing instructions — let observed gaps drive content.

---

## 6. Progressive Disclosure Patterns (Deep Dive)

Section 4c introduced the three-level loading hierarchy. This section teaches concrete patterns for splitting content across SKILL.md and resource files — with a visual explanation of how each level affects the context window.

### Context Window Dynamics

Understanding what loads when helps you design skills that stay lean:

```
┌─────────────────────────────────────────────────────────┐
│                    CONTEXT WINDOW                       │
│                                                         │
│  ┌─────────────────────────────────────────────────┐    │
│  │ System prompt + all skill metadata (Level 1)    │    │ ← Always present
│  │   skill-a: name + description (~100 tokens)     │    │
│  │   skill-b: name + description (~100 tokens)     │    │
│  │   ...50 more skills...                          │    │
│  └─────────────────────────────────────────────────┘    │
│                                                         │
│  ┌─────────────────────────────────────────────────┐    │
│  │ User message triggers skill-a (Level 2)         │    │ ← On activation
│  │   Full SKILL.md body loaded (<5K tokens)        │    │
│  └─────────────────────────────────────────────────┘    │
│                                                         │
│  ┌─────────────────────────────────────────────────┐    │
│  │ Agent reads references/schema.md (Level 3)      │    │ ← On demand
│  │   Additional context loaded as needed           │    │
│  └─────────────────────────────────────────────────┘    │
│                                                         │
│  ┌─────────────────────────────────────────────────┐    │
│  │ Agent executes scripts/validate.py (Level 3)    │    │ ← On demand
│  │   Script output returned — script NOT loaded    │    │ ← Most efficient!
│  └─────────────────────────────────────────────────┘    │
│                                                         │
│  ┌─────────────────────────────────────────────────┐    │
│  │ Conversation history + workspace files          │    │
│  └─────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
```

**Key insight:** Scripts are the most context-efficient resource type. They execute without being read into the context window — only their output enters context. References, by contrast, are read in full when loaded.

### Pattern 1: High-Level Guide with References

SKILL.md provides the quick start and workflow overview. Detailed documentation lives in `references/`.

```markdown
# PDF Processing

## Quick Start

Extract text with pdfplumber:
...brief code example...

## Advanced Features

- **Form filling**: See [references/FORMS.md](references/FORMS.md) for the complete guide.
- **API reference**: See [references/REFERENCE.md](references/REFERENCE.md) for all methods.
- **Examples**: See [references/EXAMPLES.md](references/EXAMPLES.md) for common patterns.
```

The agent loads `FORMS.md` only when the user asks about form filling, `REFERENCE.md` only when API details are needed. The body stays lean.

**When to use:** The skill has one core workflow but deep reference material for advanced features.

### Pattern 2: Domain-Specific Organisation

Content organised by domain or variant in `references/`. The agent loads only the relevant branch.

```
bigquery-skill/
├── SKILL.md              (overview + "which domain?" decision logic)
└── references/
    ├── finance.md         (revenue, billing metrics, table schemas)
    ├── sales.md           (opportunities, pipeline, CRM tables)
    ├── product.md         (API usage, features, event tables)
    └── marketing.md       (campaigns, attribution, UTM tracking)
```

SKILL.md contains the decision logic:

```markdown
## Domain Selection

| User's question mentions… | Load |
|---------------------------|------|
| Revenue, billing, invoices, ARR, MRR | [references/finance.md](references/finance.md) |
| Pipeline, opportunities, deals, CRM | [references/sales.md](references/sales.md) |
| API usage, features, events, sessions | [references/product.md](references/product.md) |
| Campaigns, attribution, UTMs, channels | [references/marketing.md](references/marketing.md) |
```

**Mutual exclusivity optimisation:** When reference files represent mutually exclusive contexts (e.g., AWS vs GCP deployment), keeping them separate saves tokens — only one path loads per task.

**When to use:** The skill handles multiple domains, frameworks, or variants that share a common workflow but differ in specifics.

### Pattern 3: Conditional Details

Basic instructions in the body; advanced content linked for on-demand loading.

```markdown
# DOCX Processing

## Creating Documents

Use docx-js for new documents. Basic creation:
...brief example...

## Editing Documents

For simple edits, modify the XML directly.

**For tracked changes (redlining):** See [references/REDLINING.md](references/REDLINING.md).
**For OOXML internals:** See [references/OOXML.md](references/OOXML.md).
```

The agent reads `REDLINING.md` only when redlining is needed. Most document tasks never touch it.

**When to use:** The skill has common and advanced paths. Most users need only the common path.

### Pattern 4: Code-as-Documentation

Scripts serve a dual purpose: executable tools AND reference documentation. Make it clear in SKILL.md whether a script should be *run* or *read*:

```markdown
- **Run:** Execute `scripts/extract.py <file>` to extract form fields from the PDF.
- **Read:** See `scripts/extract.py` for the extraction algorithm (read into context for
  understanding, not execution).
```

Running a script is more token-efficient than reading it — the script's code never enters context, only its output. Reading a script is appropriate when the agent needs to understand the algorithm to adapt it or explain it to the user.

**When to use:** Complex logic is best expressed as code, and the agent might need to either execute it or understand it depending on the task.

### Guidelines for Splitting Content

| Signal | Action |
|--------|--------|
| Body exceeds 200 lines | Move reference material to `references/` |
| Body handles multiple variants | Split variants into separate reference files (Pattern 2) |
| Advanced features rarely used | Move to conditional references (Pattern 3) |
| Same code rewritten repeatedly | Extract to `scripts/` (Pattern 4) |
| Information duplicated between body and references | Pick one canonical location; cross-reference the other |

**Avoid deeply nested references.** Keep reference files one level deep from SKILL.md — no `references/advanced/deep/nested.md`. All reference files should be linked directly from SKILL.md.

**Structure longer reference files.** For files >100 lines, include a table of contents at the top so the agent can see the full scope when previewing the file.

**Use `skills-ref to-prompt`** to preview what the agent actually sees at each disclosure level. This renders the `<available_skills>` XML exactly as the agent receives it — invaluable for debugging description and body effectiveness.

> **Key Takeaway:** Progressive disclosure keeps skills fast: metadata → body → resources, loaded on demand.

---

## 7. Writing Effective Descriptions (Trigger Engineering)

The `description` field is the most critical piece of any skill. It is the **only** content the agent reads during discovery — the moment it decides whether to load the rest of the skill. If the description fails, nothing else matters; the body, scripts, and references will never be seen.

### How Discovery Works

When a user sends a message, the agent reads the `name` and `description` of every installed skill (potentially 50–100+). It semantically matches the user's intent against each description and decides which skills to activate. This is why the description functions as a **semantic trigger** — it must contain the right vocabulary to fire when relevant and stay silent when not.

### Description Structure Formula

Use this three-part structure:

```
<What the skill does — third person, 1 sentence>.
Use when <trigger conditions — 1–2 sentences>.
Triggers on: <keyword list — domain terms and synonyms>.
```

Optionally add anti-triggers:

```
Do not use for: <exclusion conditions>.
```

### Writing Rules

1. **Always write in third person.** The description describes the skill, not the agent or the user.
   - Good: `"Processes Excel spreadsheets to extract structured data."`
   - Bad: `"I can help you process Excel spreadsheets."`
   - Bad: `"You can use this to process spreadsheets."`

2. **Include positive triggers ("Use when…").** Be specific about the conditions that should activate the skill.

3. **Include negative boundaries ("Do not use for…")** when the skill's domain is easily confused with adjacent domains.

4. **List synonyms the user might type.** If the concept has multiple names, include them all: `"model", "domain type", "immutable class", "data class"`.

5. **Use the full 1,024 characters** when needed. Short descriptions miss triggers. But don't pad with filler — every word should improve targeting.

6. **Avoid generic terms** that would false-trigger on unrelated queries: `"code"`, `"help"`, `"fix"`, `"improve"`.

7. **Reference MCP tools** by fully qualified name (`ServerName:tool_name`) if the skill depends on specific MCP tools.

### Description Components Checklist

- [ ] What the skill does (1 sentence, third person)
- [ ] "Use when" trigger conditions (1–2 sentences)
- [ ] "Triggers on:" keyword list (domain terms + synonyms)
- [ ] Optional: "Do not use for:" anti-triggers

### Real-World Examples (Annotated)

**Example 1 — Architecture Patterns**

```yaml
description: >-
  Procedural knowledge for creating Architecture Decision Records (ADRs),
  technical design documents, and file structure documentation. Covers ADR
  templates, document structures, architectural principles, and communication
  style conventions. Use when: creating ADRs, writing technical design
  documents, documenting file structures, applying architectural principles
  to design decisions. Triggers on: 'ADR', 'architecture decision',
  'technical design', 'file structure', 'architectural principles',
  'design document'.
```

Why it works: Opens with a clear capability statement. Lists six specific trigger conditions. Includes seven trigger keywords covering variations (`ADR` and `architecture decision`).

**Example 2 — PHP Docblock Writer**

```yaml
description: >-
  Write PHP docblocks for PHP 8.0+ following modern PHPDoc conventions. Use
  when (1) adding or updating docblocks on PHP classes, methods, or
  properties, (2) annotating ORM models with @property tags, (3) documenting
  service or manager method signatures, (4) generating PHPDoc for controllers,
  form requests, or service classes, or (5) asked to document PHP code.
  Triggers on phrases like "add docblocks", "document this class", "PHPDoc",
  "annotate model", or "type hints".
```

Why it works: Numbered trigger conditions make each scenario explicit. Ends with natural-language trigger phrases the user is likely to type.

**Example 3 — Requirements Gathering**

```yaml
description: >-
  Procedural guide for creating structured requirements questionnaires and
  transforming completed answers into comprehensive requirements documents.
  Use when: gathering requirements, creating questionnaires, writing
  requirements documents, preparing specifications for architects.
  Triggers on: 'requirements', 'questionnaire', 'business analysis',
  'gather requirements', 'specification document'.
```

Why it works: Clearly scoped to two procedures (questionnaire creation and requirements transformation). Domain terms (`business analysis`, `specification document`) widen the trigger net without creating false positives.

**Example 4 — Event Storming**

```yaml
description: >-
  Facilitates Event Storming workshops for exploring complex business domains,
  modeling processes, and designing software architecture. Use when users want
  to perform event storming, map business processes with domain events,
  identify bounded contexts and aggregates, or collaboratively explore a
  domain using DDD (Domain-Driven Design) techniques. Covers Big Picture,
  Process Modeling, and Software Design levels.
```

Why it works: Names all three Event Storming levels. Includes `DDD` as an acronym alongside the spelled-out form. Avoids false-triggering on generic "design" queries by anchoring to specific DDD concepts.

### Common Description Mistakes

| Mistake | Example | Fix |
|---------|---------|-----|
| Too vague | `"Helps with documents"` | `"Processes DOCX files to extract text, apply tracked changes, and generate summaries"` |
| Too broad | `"Useful for any coding task"` | Narrow to a specific domain; generic skills false-trigger on everything |
| First person | `"I help you write tests"` | `"Generates unit tests for PHP classes following PHPUnit conventions"` |
| No trigger keywords | `"A useful skill for the project"` | Add `"Use when…"` and `"Triggers on:"` sections |
| Keyword stuffing | 50 keywords jammed together | Prioritise the 5–10 most discriminating terms |

### Before/After: Rewriting a Description

**Before (v1):**

```yaml
description: >-
  This skill is for helping with database stuff. It can do migrations,
  queries, and schema things. Use it when you need database help.
```

**Problems:** vague ("stuff", "things"), no trigger keywords, doesn't specify which database or ORM, too broad to route accurately.

**After (v2):**

```yaml
description: >-
  Generates and validates Laravel Eloquent migrations for MySQL 8.0+.
  Covers column types, foreign keys, indexes, and rollback strategies.
  Use when: creating database migrations, modifying table schemas,
  adding foreign key constraints, writing rollback logic.
  Triggers on: 'migration', 'schema', 'foreign key', 'add column',
  'alter table', 'rollback'.
```

**Why it works:** specifies the framework (Laravel Eloquent), the database (MySQL 8.0+), what it covers (column types, foreign keys, indexes, rollbacks), and provides explicit `Use when:` and `Triggers on:` sections with discriminating keywords.

> **Key Takeaway:** The description is your skill's resume — it determines whether the agent ever reads your instructions.

---

## 8. Writing Effective Body Content

The body is the procedural core of your skill — the instructions the agent follows once activation occurs. Everything in the body should be actionable, not explanatory.

### Writing Style

- **Use imperative / infinitive form consistently.** Write "Extract the metadata" rather than "The metadata should be extracted" or "You can extract the metadata".
- **Keep under 500 lines** (specification limit). Aim for under 200 for optimal performance. If you exceed this, move detail to `references/`.
- **Include only what the agent doesn't already know.** AI agents understand programming languages, standard libraries, and common patterns. Don't explain how to write a for-loop or what JSON is.

### What to Include

| Content Type | When to Include | Example |
|-------------|-----------------|---------|
| Domain vocabulary | When terminology precision matters | "A *record* is an OAI-PMH entity identified by a unique identifier, a datestamp, and set memberships" |
| Step-by-step procedures | When the sequence matters | Numbered steps: 1. Read schema, 2. Generate migration, 3. Validate, 4. Apply |
| Decision logic | When the procedure branches | Decision table or if/then rules |
| Output format requirements | When output must match a template | File header template, naming convention |
| Validation criteria | When success/failure needs defining | "The migration is valid when `phpstan analyse` returns zero errors" |
| Resource references | When detail lives in `references/` | "For AWS patterns, see [references/aws.md](references/aws.md)" |

### What to Exclude

- Information the agent already knows (well-known concepts, standard patterns).
- "When to Use This Skill" sections — that belongs in the `description` field. By the time the body loads, activation has already occurred.
- Verbose explanations of tools the agent already has access to.
- Redundant copies of information in `references/` files.

### Body Content Patterns

Use these patterns individually or combine them as needed:

#### Pattern 1: Workflow Checklist

A linear sequence with checkpoints and validation gates. Best for processes with clear success criteria.

```markdown
## Generating a Migration

1. Read the current schema from `references/schema.md`.
2. Identify the required changes based on the user's request.
3. Generate the migration file using `scripts/migrate.py --type <alter|create> --table <name>`.
4. Validate the migration: run `vendor/bin/phpstan analyse` and confirm zero errors.
5. Report the file path and a summary of changes.
```

#### Pattern 2: Feedback Loop

A `Run → Check → Fix → Repeat` cycle. Best for tasks requiring iterative correction.

```markdown
## Code Review Cycle

1. Run `vendor/bin/phpcs --standard=PSR12 <file>` to check coding standards.
2. If violations are found, fix them.
3. Re-run the check.
4. Repeat until zero violations remain.
5. Run `vendor/bin/phpstan analyse <file>` at level 8.
6. Fix any reported issues and re-run until clean.
```

#### Pattern 3: Strict Template

An exact output format with placeholders. Best when the output must match precisely.

```markdown
## File Header

Every PHP file must start with this header:

\```php
<?php

/**
 * [Short description]
 *
 * @author    [author] <[email]>
 * @copyright (c) [Year] Paul Slits
 * @license   MIT License
 * @link      https://github.com/pslits/oai-pmh
 * @since     [version from composer.json]
 */
\```

Replace bracketed placeholders with actual values. Check `composer.json` for the current version.
```

#### Pattern 4: Flexible Template

An annotated example with guidelines. Best when output follows conventions but varies by situation.

```markdown
## Test Method Naming

Follow this pattern: `testMethodName_Condition_ExpectedBehavior()`

Examples:
- `testGetValue_ValidInput_ReturnsString()`
- `testConstructor_EmptyValue_ThrowsInvalidArgumentException()`
- `testEquals_SameValue_ReturnsTrue()`

The condition and expected behaviour parts should be specific enough to distinguish the test from other tests in the same class.
```

#### Pattern 5: Input/Output Examples

Concrete pairs showing input → expected output. Best for complex transformations where prose is ambiguous.

```markdown
## Generating Equals Method

Input class with property `$email` of type `string`:
→ Output:
\```php
public function equals(self $otherEmail): bool
{
    return $this->email === $otherEmail->email;
}
\```

Input class with properties `$host` (string) and `$port` (int):
→ Output:
\```php
public function equals(self $otherConnection): bool
{
    return $this->host === $otherConnection->host
        && $this->port === $otherConnection->port;
}
\```
```

#### Pattern 6: Conditional Workflow

Decision tree or `if/then` branching. Best for multi-variant tasks where context determines the path.

```markdown
## Choosing the Validation Strategy

| Input Type | Validation Approach |
|-----------|-------------------|
| URL | Validate format with `filter_var()`, then check HTTP protocol |
| Email | Validate with `filter_var(FILTER_VALIDATE_EMAIL)` |
| Datetime | Parse with `DateTimeImmutable`, validate UTC format |
| Free text | Validate not empty, check max length |

Apply the matching strategy. If the input type is ambiguous, ask the user to clarify.
```

#### Pattern 7: Domain Vocabulary

A glossary of terms the agent must use consistently. Best for specialised domains.

```markdown
## OAI-PMH Vocabulary

Use these terms consistently throughout all generated code and documentation:

- **Record** — a single metadata entry identified by a unique identifier, a datestamp, and zero or more set memberships.
- **Set** — a named grouping of records within a repository.
- **Resumption Token** — a flow-control mechanism for paginating large result sets.
- **Harvester** — the client that requests records from a repository.
- **Repository** — the server that exposes records via the OAI-PMH protocol.
```

### Combining Patterns

Patterns compose naturally. Common combinations:

- **Conditional workflow + Feedback loop:** Branch to the right strategy, then iterate until validation passes.
- **Workflow checklist + Strict template:** Follow the steps, produce output matching the template.
- **Domain vocabulary + Input/Output examples:** Define terms first, then show transformations using those terms.

### Referencing Bundled Resources

When the body references files in `scripts/`, `references/`, or `assets/`, make the purpose explicit:

```markdown
- **Run:** "Execute `scripts/validate.py <file>` to check the output" (agent runs the script).
- **Read:** "See [references/schema.md](references/schema.md) for the full table definitions" (agent reads into context).
- **Copy:** "Copy `assets/template.html` to the output directory" (agent uses the file without reading it).
```

> **Key Takeaway:** Write imperative steps the agent can follow, not explanations of concepts it already knows.

---

## 9. Bundled Resources — Scripts, References, Assets

This section provides detailed guidance for each resource type, building on the overview in §3e.

### 9a. Scripts (`scripts/`)

Scripts provide **deterministic reliability** for tasks the agent would otherwise have to rewrite each time. They are the most token-efficient resource type — the agent executes them without reading their source into context.

#### When to Include Scripts

- The same code is being rewritten repeatedly across sessions.
- Deterministic reliability is required (e.g., PDF rotation, file transformation).
- The task is too complex or fragile for prose instructions.
- "Solve, don't punt" — the skill should actually perform the task, not describe how.

#### Language Choice

- Prefer the project's primary language for project-specific skills.
- Use Python or Bash for universal, cross-project skills.
- Ensure the language runtime is available in the target environment (document in `compatibility` if non-standard).

#### One-Off Commands

For tasks expressible as a single command, don't bundle a script. Instead, instruct the agent to run external tools directly in the SKILL.md body:

```markdown
Run `npx prettier --write <file>` to format the output.
Run `uvx ruff check <file>` to lint the Python code.
Run `pipx run black <file>` to format the Python code.
```

These leverage existing tools without adding files to the skill.

#### Self-Contained Scripts

For complex logic, bundle self-contained scripts with inline dependency declarations. Python scripts should use PEP 723 inline metadata:

```python
# /// script
# dependencies = ["pandas>=2.0", "openpyxl"]
# ///
```

This allows the agent to run `uv run scripts/process.py` without separate install steps. Dependencies are resolved automatically.

#### Designing Scripts for Agentic Use

Scripts invoked by an agent must behave differently from scripts designed for human use:

| Principle | Implementation |
|-----------|----------------|
| **No interactive prompts** | Use command-line arguments, environment variables, or stdin. Never prompt for user input — the agent cannot respond to interactive prompts. |
| **Rich `--help` output** | Include comprehensive help text. This is the agent's API documentation for the script. |
| **Helpful error messages** | Include context, suggest fixes, and show usage examples in error output. The agent uses error messages to self-correct. |
| **Structured output** | Prefer JSON for complex output; plain text for simple results. The agent parses output to determine next steps. |
| **Idempotency** | Running the script twice with the same input produces the same result. No unintended side effects from repeated execution. |
| **Dry-run support** | Include a `--dry-run` flag that shows what would change without making changes. Useful for agent verification before committing. |
| **Meaningful exit codes** | `0` = success, non-zero = failure. Document exit codes in `--help`. The agent checks exit codes to determine success. |
| **Safe defaults** | Destructive operations require explicit `--force` or `--confirm` flags. Prevents accidental data loss. |
| **Predictable output size** | Cap output length. Use pagination or truncation for large results. Unbounded output can overflow the context window. |

#### Testing Scripts

**Test every script by actually running it.** Run each script with representative inputs and verify:

- Output matches expectations.
- Error cases produce helpful messages.
- `--help` output is clear and complete.
- Exit codes are correct (0 for success, non-zero for failure).
- Idempotency holds (running twice produces the same result).

For skills with many similar scripts, test a representative sample to balance thoroughness with speed.

### 9b. References (`references/`)

References are documentation files the agent loads on demand via `read_file`. They extend the skill's knowledge without inflating the SKILL.md body.

#### When to Include References

- Detailed documentation needed during execution (schemas, API docs, checklists).
- Domain-specific knowledge that varies by context (finance terms, cloud provider patterns).
- Information too detailed for the body but too important to omit.

#### Large File Strategy

| File Size | Recommendation |
|-----------|---------------|
| < 100 lines | No special treatment needed |
| 100–500 lines | Include a table of contents at the top |
| 500–10K words | Include TOC + section headers the agent can navigate |
| > 10K words | Include grep search patterns in SKILL.md so the agent can find specific content without reading the entire file |

Example of grep guidance in SKILL.md:

```markdown
## Schema Reference

Full table definitions are in [references/schema.md](references/schema.md).
To find a specific table, search for `## Table: <name>`.
To find column definitions, search for `| column_name |`.
```

#### Avoiding Duplication

Information should live in exactly one place:
- **Body** — core procedural instructions and workflow guidance.
- **References** — detailed reference material, schemas, examples.

If the body summarises content that also exists in a reference file, keep the summary minimal (1–2 sentences + a link) and let the reference file be the canonical source.

### 9c. Assets (`assets/`)

Assets are files used in the skill's output — not loaded into context, but copied, modified, or referenced by the agent during task execution.

#### When to Include Assets

- Templates the agent copies and customises (HTML boilerplate, project scaffolds).
- Images, icons, or fonts used in generated output.
- Sample documents that serve as starting points.
- Configuration file templates.

#### Organisation

```
assets/
├── templates/
│   ├── component.html
│   └── migration.stub
├── images/
│   └── logo.png
└── fonts/
    └── brand-font.ttf
```

Use descriptive filenames and organise in subdirectories by purpose. The agent navigates `assets/` by path, so clear naming reduces errors.

> **Key Takeaway:** Scripts execute without entering context — they're the most token-efficient resource type.

---

## 10. Testing and Validation

Validate your skill's structure (does it conform to the spec?) and behaviour (does it work in practice?) before sharing.

### 10a. Structural Validation

Verify these constraints before any functional testing:

| Check | Requirement |
|-------|------------|
| Name matches directory | `name` field in frontmatter = parent directory name |
| Description length | ≤ 1,024 characters, non-empty |
| Body length | ≤ 500 lines |
| No reserved words | `name` does not contain `anthropic` or `claude` |
| No XML tags | Neither `name` nor `description` contains XML tags |
| No extraneous files | No README.md, CHANGELOG.md, INSTALLATION_GUIDE.md, etc. |
| Name format | Lowercase alphanumeric + hyphens, no leading/trailing/consecutive hyphens, 1–64 chars |

#### Automated Validation with `skills-ref`

The [`skills-ref`](https://github.com/agentskills/agentskills/tree/main/skills-ref) Python CLI automates structural checks:

```bash
# Install
pip install skills-ref

# Validate structure — reports all constraint violations
skills-ref validate .github/skills/my-skill

# Extract frontmatter properties for inspection
skills-ref read-properties .github/skills/my-skill

# Generate the <available_skills> XML as the agent sees it
# Invaluable for debugging description phrasing
skills-ref to-prompt .github/skills/skill-a .github/skills/skill-b
```

#### VS Code Diagnostics View

In VS Code with GitHub Copilot:

1. Open the Chat view.
2. Click the settings gear → **Diagnostics**.
3. View which skills are discovered, loaded, and active in the current session.

Use this to debug "why isn't my skill activating?" issues.

### 10b. Functional Validation

Test the skill's behaviour with real agent interactions:

| Test Type | Procedure | Pass Criteria |
|-----------|-----------|--------------|
| **Trigger test** | Ask the agent something that *should* activate the skill | The skill activates and the agent follows its instructions |
| **Negative trigger test** | Ask something that should *not* activate the skill | The skill stays inactive |
| **Procedure test** | Follow the skill's steps manually and verify the output | Output matches expectations and quality standards |
| **Edge case test** | Try ambiguous inputs, missing context, unusual parameters | The agent handles gracefully or asks for clarification |
| **Multi-model test** | Run the same test on at least two model sizes (see §4d) | Consistent behaviour across models |

### 10c. Integration Validation

Test the skill in context with other active skills and workspace content:

- **Co-activation:** Does the skill work alongside other active skills without conflicts?
- **Context budget:** Does it stay within reasonable context usage? (Check with `skills-ref to-prompt`)
- **Relative paths:** Do references load correctly via relative paths from SKILL.md?
- **Script execution:** Do scripts execute successfully in the target environment?

### Behavioural Observation

During functional testing, watch how the agent interacts with your skill. If it reads unexpected files, ignores sections, follows instructions too rigidly, or misses references — these are signals to iterate. See §18 (Debugging and Troubleshooting) for a detailed diagnostic framework covering these patterns and their fixes.

### Validation Checklist (Copy-Paste Ready)

```markdown
## Skill Validation Checklist

- [ ] `name` matches directory name
- [ ] `description` ≤ 1,024 characters
- [ ] Body ≤ 500 lines
- [ ] No extraneous files (README.md, CHANGELOG.md, etc.)
- [ ] `skills-ref validate` passes (if available)
- [ ] Trigger test: skill activates for relevant query
- [ ] Negative trigger test: skill stays silent for unrelated query
- [ ] Procedure test: output matches expectations
- [ ] Scripts execute successfully with representative inputs
- [ ] References load correctly via relative paths
- [ ] Tested on at least two model sizes
```

> **Key Takeaway:** Validate structure with `skills-ref`, test behaviour with real scenarios on multiple models.

---

## 11. Iteration and Evolution

Skills are living artefacts. They improve through use, observation, and structured feedback — not just initial authoring.

### The Iteration Cycle

```
Use on real tasks
       │
       ▼
Notice struggles or inefficiencies
       │
       ▼
Identify improvements (body, resources, description)
       │
       ▼
Implement changes
       │
       ▼
Test again (§10)
       │
       ▼
Repeat
```

### Iterate with the Agent

As you work with the agent on real tasks, leverage it for skill improvement:

1. **Capture successful approaches.** When the agent handles a task well, ask it to articulate what worked and codify the approach into the skill's instructions or scripts.

2. **Self-reflect on failures.** When the agent goes off track, ask it to analyse what went wrong and suggest skill amendments. The agent can identify gaps in its own instructions.

This discovery-driven process reveals what context the agent *actually* needs, rather than what the author *assumed* it needs.

**Start with evaluation → build skills to address observed gaps** — not the other way around.

### Connecting to the Session Feedback Loop

The [Session Feedback Guide](copilot-session-feedback-guide.md) provides the analysis framework:

- **Lens 3 (Workflow Friction)** surfaces new skill candidates — repeated multi-step workflows that the agent repeatedly struggles with.
- **Lens 1 (Recurring Corrections)** identifies improvements to existing skills — corrections you keep making that should be codified.
- Session transcripts capture specific moments where skills succeeded or failed, providing evidence for targeted improvements.

### Lifecycle Decisions

Skills don't just grow — they sometimes need structural changes:

| Decision | When | Action |
|----------|------|--------|
| **Split** | One skill handles too many unrelated domains | Extract each domain into a focused skill with its own trigger domain |
| **Merge** | Two skills have overlapping procedures and often co-activate | Combine into one skill; deduplicate content |
| **Retire** | The underlying tool changed, the procedure is obsolete, or a better skill exists | Remove the skill; update any skills that referenced it |
| **Fork** | Same procedure, different domain constraints (e.g., same deployment process, different cloud providers) | Create a new skill with shared structure but domain-specific references |

### Version Tracking

Use the `metadata.version` field to track skill versions:

```yaml
metadata:
  version: "1.2.0"
  author: "Your Team"
```

Bump the version when:
- The skill's behaviour changes significantly.
- New resource files are added.
- Script interfaces change (breaking change).
- Description keywords change (affects activation).

Link to the [Maintenance Loop](copilot-session-feedback-guide.md#section-7--the-maintenance-loop) in the session feedback guide for the broader update cadence.

### Migrating Existing Knowledge into Skills

Existing documentation and artefacts can be converted into skills:

| Source Artefact | Migration Strategy |
|----------------|-------------------|
| **Runbooks** | Body = numbered steps from the runbook. Extract repetitive commands into `scripts/`. Strip explanatory prose the agent already knows. |
| **READMEs** | Split: declarative information (architecture, rationale) → `copilot-instructions.md`. Procedural content → skill body. |
| **Wiki pages** | Move to `references/` files. Write a SKILL.md body as the entry point that links to each reference. |
| **Bash aliases / snippets** | Move to `scripts/` directory. Add `--help` output and argument parsing for agentic use. |
| **Cheat sheets** | Evaluate: if it's a reference lookup → `references/`. If it's a procedure → skill body. |

**Migration checklist:**
- [ ] Strip prose the agent already knows (generic programming concepts, standard library usage).
- [ ] Add trigger keywords to the description (§7).
- [ ] Convert passive documentation into imperative instructions.
- [ ] Validate with `skills-ref validate`.
- [ ] Test activation and behaviour (§10).

> **Key Takeaway:** Skills improve through use — observe the agent, capture what works, fix what doesn't.

---

## 12. Anti-Patterns Gallery

Learn from common mistakes. Each anti-pattern has a name, a description of the problem, and a concrete fix.

| # | Anti-Pattern | Problem | Fix |
|---|-------------|---------|-----|
| 1 | **The Encyclopedia** | Body exceeds 500 lines with exhaustive documentation that the agent skips over. | Move reference material to `references/`; keep the body procedural and under 200 lines (§6). |
| 2 | **The Ghost Trigger** | Description is too vague — the skill never activates because the agent can't match it to user intent. | Add "Use when…" conditions and "Triggers on:" keyword lists (§7). |
| 3 | **The False Positive** | Description is too broad — the skill activates for unrelated tasks, wasting context and confusing the agent. | Narrow trigger keywords. Add "Do not use for…" boundaries (§7). |
| 4 | **The Duplication Trap** | Same information exists in both the body and a reference file. Updates to one create drift with the other. | Pick one canonical location. Cross-reference the other with a link. |
| 5 | **The Orphan Resource** | Scripts or references exist in the skill directory but are never referenced from the body. The agent never discovers them. | Either reference them from the body or delete them. |
| 6 | **The Context Hog** | Skill loads massive resources unconditionally, consuming a disproportionate share of the context window. | Apply progressive disclosure (§6). Load resources on demand via references, not inline. |
| 7 | **The README Creep** | Skill directory contains README.md, CHANGELOG.md, INSTALLATION_GUIDE.md, or other human-facing documentation. | Remove. Skills are for the agent, not human documentation. |
| 8 | **The Monolith** | Single skill covers too many unrelated procedures (code review, testing, deployment, documentation all in one). | Split into focused skills with distinct trigger domains (§19). |
| 9 | **The Rules Skill** | Skill contains declarative coding rules ("always use camelCase", "never use var") instead of procedural steps. | Move declarative rules to `copilot-instructions.md` or `*.instructions.md`. Skills are for procedures (§2). |
| 10 | **The Implicit Dependency** | Skill assumes tools, extensions, or runtimes are available without checking or documenting. | Use the `compatibility` field. Add prerequisite checks in the procedure. |
| 11 | **The Windows Path** | Uses backslash paths (`C:\Users\...`) in scripts or references. Breaks on macOS/Linux and confuses path resolution. | Use forward slashes. Use relative paths from the skill root. |
| 12 | **The Option Overload** | Too many configuration options. The agent doesn't know which to choose and stalls or picks randomly. | Provide sensible defaults. Limit choices to 2–3 per decision point. |
| 13 | **The Voodoo Constant** | Magic numbers or threshold values in instructions with no explanation (e.g., "set timeout to 42"). | Document *why* each constant exists and how to adjust it. |
| 14 | **The First-Person Description** | Description says "I can help you…" or "You can use this to…" instead of third-person. | Rewrite in third person: "Processes Excel files to extract structured data" (§7). |
| 15 | **The Stale Reference** | Time-sensitive information (URLs, version numbers, dates) hardcoded in the skill becomes outdated. | Instruct the agent to look up current values instead of hardcoding them (§4e). |

Each anti-pattern maps to guidance elsewhere in this guide. When you spot one in your own skill, follow the Fix column and cross-reference the indicated section for detailed remediation.

> **Key Takeaway:** Every anti-pattern has a name — learn them so you can spot them in your own skills.

---

## 13. Examples and Case Studies

Five worked examples applying the patterns from this guide. Each is annotated with design decisions.

### Example 1: Model Builder Skill

**Purpose:** Generate immutable value objects following project conventions.

**Design decisions:**
- **Freedom level:** Medium — a preferred pattern exists (immutable VO) with some variation per domain type.
- **Progressive disclosure:** Body contains the 4-step workflow. Domain-specific validation patterns go in `references/`.
- **Triggers:** Targets specific phrases like "value object", "immutable class", "create a model".

```yaml
---
name: building-models
description: >-
  Generates immutable value object classes following DDD conventions with
  validation, equality comparison, and string representation. Use when
  creating value objects, domain types, immutable classes, or data classes.
  Triggers on: 'value object', 'VO', 'immutable class', 'domain type',
  'data class', 'create a model'.
---
```

```markdown
# Building Models

## Procedure

1. Identify the value the object wraps (type, constraints, domain meaning).
2. Generate the class:
   - `final` class with private property.
   - Constructor with validation (extract to private `validate*()` methods).
   - Domain-specific getter (e.g., `getEmail()`) + `getValue()` alias.
   - `equals(self $other): bool` for value comparison.
   - `__toString(): string` returning `ClassName(value: <value>)`.
3. Generate the test class following `testMethod_Condition_Expected()` naming.
4. Run `vendor/bin/phpstan analyse` and `vendor/bin/phpcs` to validate.

## Validation Patterns

For complex validation, see [references/validation-patterns.md](references/validation-patterns.md).
```

**Why this works:** The body is ~20 lines — well under the 200-line target. The procedure is concrete and imperative. Validation patterns (which are extensive and domain-specific) live in a reference file loaded only when needed.

---

### Example 2: API Client Generator Skill

**Purpose:** Generate API client code for multiple HTTP libraries.

**Design decisions:**
- **Freedom level:** Medium — the workflow is consistent, but implementation varies by library.
- **Progressive disclosure:** Pattern 2 (domain-specific organisation). Each HTTP library gets its own reference file.
- **Triggers:** Covers multiple synonyms for the same action.

```yaml
---
name: generating-api-clients
description: >-
  Generates typed API client code for REST endpoints using various HTTP
  libraries. Supports fetch, axios, and httpx. Use when creating API clients,
  HTTP wrappers, or service classes that call external APIs. Triggers on:
  'API client', 'HTTP client', 'REST client', 'fetch wrapper', 'axios
  service', 'httpx client', 'generate client'.
---
```

```
generating-api-clients/
├── SKILL.md
└── references/
    ├── fetch.md       (browser Fetch API patterns)
    ├── axios.md       (Axios for Node.js patterns)
    └── httpx.md       (httpx for Python patterns)
```

Body includes library selection logic:

```markdown
## Library Selection

| User's stack | Library | Reference |
|-------------|---------|-----------|
| Browser / React / Vue | Fetch API | [references/fetch.md](references/fetch.md) |
| Node.js / Express | Axios | [references/axios.md](references/axios.md) |
| Python / FastAPI | httpx | [references/httpx.md](references/httpx.md) |

Determine the user's stack from the project context. Load only the matching reference file.
```

**Why this works:** Mutually exclusive reference files (you use fetch OR axios OR httpx, never all three). Loading only the relevant one saves significant context.

---

### Example 3: Database Migration Skill

**Purpose:** Generate and apply database migrations deterministically.

**Design decisions:**
- **Freedom level:** Low — migrations are fragile; consistency is critical.
- **Progressive disclosure:** Scripts handle the deterministic parts. References provide schema documentation.
- **Triggers:** Specific to migration workflows.

```yaml
---
name: generating-migrations
description: >-
  Generates database migration files from schema changes and applies them
  safely with rollback support. Use when creating database migrations,
  altering tables, adding columns, or modifying schema. Triggers on:
  'migration', 'database migration', 'alter table', 'add column',
  'schema change', 'migrate database'.
  Do not use for: query writing or database analysis.
---
```

```
generating-migrations/
├── SKILL.md
├── scripts/
│   ├── migrate.py          (generates migration file from schema diff)
│   └── validate-schema.py  (validates migration against target DB)
└── references/
    └── schema.md           (current table definitions)
```

Body uses the workflow checklist + feedback loop pattern:

```markdown
## Procedure

1. Read [references/schema.md](references/schema.md) for current table definitions.
2. Run `scripts/migrate.py --type <alter|create> --table <name> --dry-run` to preview.
3. Review the preview output. If correct, run without `--dry-run`.
4. Run `scripts/validate-schema.py <migration-file>` to validate.
5. If validation fails, fix the migration and re-validate (repeat steps 3–4).
6. Report the migration file path and a summary of changes.
```

**Why this works:** Low freedom — the agent runs scripts rather than writing migration code from scratch. `--dry-run` ensures safety. The feedback loop catches validation errors.

---

### Example 4: Code Review Skill

**Purpose:** Structured code review following a team's checklist.

**Design decisions:**
- **Freedom level:** High — the reviewer applies judgement; the skill provides the framework.
- **Progressive disclosure:** Body contains the checklist. No references needed for a focused skill.
- **Triggers:** Clear domain boundary (review, not write or fix).

```yaml
---
name: reviewing-code
description: >-
  Performs structured code reviews following a multi-point quality checklist
  covering style, logic, security, performance, and maintainability. Use
  when asked to review, critique, or audit code. Triggers on: 'code review',
  'review this', 'critique', 'audit code', 'PR review'.
  Do not use for: writing code, fixing bugs, or generating tests.
---
```

Body uses the conditional workflow pattern:

```markdown
# Code Review

## Review Checklist

For each file under review, evaluate:

| Category | Check | Severity |
|----------|-------|----------|
| **Style** | Follows project coding standards (PSR-12, naming conventions) | Medium |
| **Logic** | No off-by-one errors, null safety, edge cases handled | High |
| **Security** | Input validation, no SQL injection, no credential exposure | Critical |
| **Performance** | No N+1 queries, appropriate caching, no unnecessary allocations | Medium |
| **Maintainability** | Single responsibility, clear naming, appropriate abstraction | Medium |
| **Testing** | Key paths covered, edge cases tested | Medium |

## Output Format

For each finding, report:
1. File and line number.
2. Category and severity.
3. Description of the issue.
4. Suggested fix (code snippet if applicable).

Order findings by severity (Critical → High → Medium).
```

**Why this works:** High freedom — the checklist guides without constraining. The agent applies its own judgement within the framework. No scripts needed because the task is inherently analytical.

---

### Example 5: Document Processing Skill

**Purpose:** Process various document formats (PDF, DOCX, XLSX) with script-heavy automation.

**Design decisions:**
- **Freedom level:** Low for extraction (deterministic scripts), High for analysis (agent judgement).
- **Progressive disclosure:** Pattern 1 (high-level guide + references). Scripts are the primary tool; references provide format-specific guidance.
- **Scripts use PEP 723 for self-contained dependency management.**

```yaml
---
name: processing-documents
description: >-
  Processes PDF, DOCX, and XLSX files for text extraction, data analysis,
  and format conversion. Supports form filling, tracked changes, and
  spreadsheet formulas. Use when working with document files for extraction,
  analysis, editing, or conversion. Triggers on: 'PDF', 'DOCX', 'XLSX',
  'Word document', 'Excel spreadsheet', 'extract text', 'parse document'.
---
```

```
processing-documents/
├── SKILL.md
├── scripts/
│   ├── extract_pdf.py      (text + form extraction, PEP 723 deps)
│   ├── process_docx.py     (text extraction, tracked changes)
│   └── parse_xlsx.py       (data extraction, formula evaluation)
└── references/
    ├── FORMS.md            (PDF form filling guide)
    ├── REDLINING.md        (DOCX tracked changes guide)
    └── SPREADSHEETS.md     (XLSX formula and pivot table guide)
```

Script example with PEP 723 inline metadata:

```python
#!/usr/bin/env python3
# /// script
# dependencies = ["pdfplumber>=0.10", "PyPDF2>=3.0"]
# ///
"""Extract text and form fields from PDF files."""

import argparse
import json
import sys

def main():
    parser = argparse.ArgumentParser(
        description="Extract text and form fields from PDF files.",
        epilog="Output: JSON with 'text' and 'fields' keys."
    )
    parser.add_argument("input", help="Path to the PDF file")
    parser.add_argument("--pages", help="Page range (e.g., 1-5)", default=None)
    parser.add_argument("--fields-only", action="store_true", help="Extract only form fields")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be extracted")
    # ... implementation
```

**Why this works:** Scripts handle the deterministic extraction work (low freedom). Reference files provide format-specific deep guidance loaded only when needed. PEP 723 makes scripts self-contained — `uv run scripts/extract_pdf.py` installs dependencies automatically.

> **Key Takeaway:** Study real examples to internalize the patterns; annotate design decisions, not just code.

---

## 14. Integration with the Feedback Loop

This guide and the [Session Feedback Guide](copilot-session-feedback-guide.md) form a closed loop. The feedback guide identifies *when* to create a skill; this guide covers *how*. Neither works well alone.

### Skills in the Feedback Lifecycle

Skills are one of six integration surfaces in the feedback model. The lifecycle:

```
Session → Capture → Analyse → Document → Route to Skill → Validate → Use → Iterate
```

### Identifying Skill Candidates from Session Analysis

The feedback guide's diagnostic lenses surface skill opportunities:

| Lens | Signal | Action |
|------|--------|--------|
| **Lens 3 (Workflow Friction)** | You repeatedly explain the same multi-step procedure across sessions | Create a new skill encoding the procedure |
| **Lens 1 (Recurring Corrections)** | You keep correcting the agent on the same domain-specific patterns | Add the correction to an existing skill, or create a new one |
| **Lens 4 (Quality Guardrails)** | Consistent quality issues in a specific domain | Add validation steps or scripts to the relevant skill |

### Using Template 5 as the Starting Skeleton

The feedback guide's [Template 5](copilot-session-feedback-guide.md#template-5-skillmd-skill-definition) provides a minimal SKILL.md template to copy-paste. Use it as the scaffolding, then apply the detailed guidance from this guide (§3–§8) to flesh it out.

### Routing Validation

After writing a skill, re-check the [Routing Decision Tree](copilot-session-feedback-guide.md#section-5--routing-decision-tree) to confirm a skill was the right choice. If it turns out the knowledge is better suited to `copilot-instructions.md` or a `*.prompt.md`, migrate it before investing further.

### Feeding Performance Back into the Loop

When a skill underperforms:

1. Capture the session output (what the agent produced, where it struggled).
2. Apply Lens 3 (Workflow Friction) to identify the specific gap.
3. Iterate on the skill (§11) — refine instructions, add resources, narrow the description.
4. Re-test (§10) and re-deploy.

This keeps the feedback loop turning: sessions reveal gaps → gaps become skill improvements → improved skills produce better sessions.

### Cross-References to the Session Feedback Guide

The following references point to sections in the companion [Session Feedback Guide](copilot-session-feedback-guide.md), not this guide:

| Topic | Location in Session Feedback Guide |
|-------|-----------------------------------|
| Skills surface definition | Feedback Guide §1.5 (Skills) |
| Workflow friction analysis | Feedback Guide §3 Lens 3 |
| SKILL.md template | Feedback Guide §4 Template 5 |
| Routing decision tree | Feedback Guide §5 |
| Maintenance cadence | Feedback Guide §7 Maintenance Loop |
| Validation & troubleshooting | Feedback Guide §9 |

> **Key Takeaway:** The feedback loop connects session analysis to skill creation — neither works well alone.

---

## 15. Naming Conventions

The `name` field appears as the slash command (`/skill-name`) and as the directory name. Choose a name that is readable, discoverable, and unambiguous.

### Specification Rules

All names must comply with these constraints:

- **1–64 characters.**
- **Lowercase alphanumeric + hyphens only** (a–z, 0–9, `-`).
- **No leading, trailing, or consecutive hyphens** (`-my-skill`, `my-skill-`, `my--skill` are all invalid).
- **Must match the parent directory name exactly.**
- **No reserved words:** `anthropic`, `claude`.
- **No XML tags** in the name.

### Recommended Format: Gerund Form

Use a gerund (verb-ing) + noun pattern. It reads naturally as a capability description:

| Name | Reads As |
|------|----------|
| `processing-pdfs` | "The agent is processing PDFs" |
| `analyzing-spreadsheets` | "The agent is analyzing spreadsheets" |
| `generating-migrations` | "The agent is generating migrations" |
| `reviewing-code` | "The agent is reviewing code" |

### Also Acceptable

| Format | Examples |
|--------|----------|
| Noun phrases | `pdf-processor`, `migration-generator` |
| Action-oriented | `review-code`, `deploy-config` |
| Domain-specific | `oai-pmh-validator`, `kubernetes-troubleshooter` |

### What to Avoid

| Problem | Bad Example | Better |
|---------|-------------|--------|
| Vague names | `helper`, `utils`, `tool`, `general` | `formatting-code`, `validating-schemas` |
| Overly long | `comprehensive-end-to-end-pdf-document-processing-skill` | `processing-pdfs` |
| Non-universal abbreviations | `proc-pdfs`, `gen-migs` | `processing-pdfs`, `generating-migrations` |
| Technology prefixes | `python-pdf-tool`, `node-api-builder` | `processing-pdfs` (use `compatibility` for runtime requirements) |
| Trailing descriptors | `pdf-processing-skill`, `code-review-tool` | `processing-pdfs`, `reviewing-code` |

> **Key Takeaway:** Use gerund form (`processing-pdfs`), keep it lowercase with hyphens, 1–64 characters.

---

## 16. Security Considerations

Skills can modify agent behaviour and execute code. This section covers security awareness for both skill authors and consumers.

### Author Perspective

When writing a skill, you are granting the agent new capabilities. Treat this with the same care as shipping production code.

**Script security:**
- Audit all bundled scripts for unintended side effects (file deletion, network calls, credential access).
- Avoid hardcoding credentials, API keys, or tokens in scripts or reference files.
- Include `--dry-run` flags for any destructive operation.
- Validate all inputs in scripts — do not trust the agent's arguments blindly.
- Pin dependency versions in PEP 723 inline metadata to prevent supply chain attacks:
  ```python
  # /// script
  # dependencies = ["pandas==2.1.4", "openpyxl==3.1.2"]
  # ///
  ```

**Metadata security:**
- Document network dependencies in the `compatibility` field so consumers know what connections the skill requires.
- Use the `license` field for redistributable skills.

### Consumer Perspective

When installing skills from external sources:

- **Review bundled scripts before enabling** in production environments. Read the source of every script in `scripts/`.
- **Use `disable-model-invocation: true`** for untrusted skills until you have reviewed them. This prevents auto-loading while you audit.
- **Check the `allowed-tools` field** for unexpected tool access grants.
- **Install from trusted sources only.** Verify the repository or extension publisher.

### Scope Control

- The `allowed-tools` field restricts which tools the skill can invoke (experimental; implementation varies by agent).
- Personal skills can override project skills — be aware of precedence when both exist for the same domain.
- Extension-contributed skills run with the extension's permissions.

> **Key Takeaway:** Audit all bundled scripts and dependencies — a skill runs with the agent's permissions.

---

## 17. Distribution and Discovery

How to share skills beyond a single repository.

### Project Sharing

Commit your skills to `.github/skills/` in your repository. Every team member who clones the repo gets them automatically. This is the simplest and most common distribution method.

### Cross-Project Sharing

Two approaches for skills that span multiple repositories:

**Central skills repository:** Create a dedicated repository for shared skills. Point to it from each project using the VS Code setting:

```json
{
  "chat.agentSkillsLocations": [
    "../shared-skills-repo/.github/skills"
  ]
}
```

**Personal skills:** Place skills in `~/.copilot/skills/` (or `~/.claude/skills/`) for individual workflows that aren't team-shared. These follow you across projects without needing to be committed to any repository.

### Community Sharing

Two major community repositories for discovering and sharing skills:

- **[anthropics/skills](https://github.com/anthropics/skills)** — Anthropic's official example repository. Contains production-quality skills for PDF, DOCX, XLSX processing, and more. Submit PRs to contribute.
- **[github/awesome-copilot](https://github.com/github/awesome-copilot)** — Community collection with an MCP server for browsing, installing, and managing skills.

### Extension Distribution

VS Code extensions can bundle skills via the `chatSkills` contribution point (see §3g). This allows distribution through the VS Code Marketplace — the broadest reach for universal skills.

### Packaging as `.skill` Files

For portable distribution outside of git repositories or VS Code extensions, skills can be packaged as `.skill` files — zip archives containing the full skill directory:

```
my-skill.skill   (a .zip archive)
├── SKILL.md
├── scripts/
│   └── process.py
└── references/
    └── patterns.md
```

The skill-creator skill includes a `scripts/package_skill.py` helper that automates this: it zips the skill directory, excludes development artifacts (e.g., `.git/`, `__pycache__/`), and validates the structure before packaging. Use `.skill` files when sharing skills via email, Slack, or artifact storage where git access is impractical.

### Discovery Aids

- **`llms.txt`** at the repository root helps external agents discover project skills.
- **Clear `description` fields** function as searchable documentation even outside the agent context.
- **`metadata.version`** tracks skill versions. Include version requirements in `compatibility` when breaking changes occur.

> **Key Takeaway:** Share project skills via your repo; share personal skills via `~/.copilot/skills/`.

---

## 18. Debugging and Troubleshooting

Section 10 covers validation *before* shipping. This section covers diagnosis *after* deployment — when the skill is installed but not behaving as expected.

### Common Failure Modes

| Symptom | Likely Cause | Diagnostic Step | Fix |
|---------|-------------|----------------|-----|
| Skill never activates | Description too vague or missing trigger keywords | Check `skills-ref to-prompt` output; review description | Add "Use when…" and "Triggers on:" keywords (§7) |
| Skill activates for wrong tasks | Description too broad | Review VS Code Diagnostics for activation log | Add "Do not use for…" boundaries; narrow keywords |
| Agent ignores parts of the body | Body too long; agent skips verbose sections | Count body lines; check which sections the agent follows | Shorten body; move detail to `references/` (§6) |
| Reference files not loaded | Missing or broken relative path link | Check file exists at the referenced path | Use `[label](references/file.md)` format; verify relative path |
| Scripts fail silently | Missing dependencies or wrong interpreter | Run script manually in the target environment | Add `compatibility` field; test script standalone (§9a) |
| Skill conflicts with another skill | Overlapping trigger domains | Check which skills co-activate in Diagnostics | Narrow descriptions; use `disable-model-invocation` on one |
| Slash command doesn't appear | `user-invokable: false` or `name` mismatch | Check frontmatter; verify directory name matches `name` | Fix `name` field or set `user-invokable: true` |
| Skill loads but agent doesn't follow steps | Instructions too vague or too verbose | Observe agent behaviour on a concrete task | Rewrite body with more specific, imperative steps (§8) |

### Diagnostic Tooling

#### `skills-ref to-prompt`

Generates the `<available_skills>` XML exactly as the agent sees it. Compare the rendered output against your expectations:

```bash
skills-ref to-prompt .github/skills/my-skill .github/skills/other-skill
```

If the description looks different from what you intended, revise it. The XML output is the ground truth.

#### `skills-ref read-properties`

Extracts all frontmatter properties for quick inspection:

```bash
skills-ref read-properties .github/skills/my-skill
```

#### VS Code Diagnostics View

Navigate to: Chat settings gear → Diagnostics. Shows:
- Which skills are **discovered** (found in skill directories).
- Which skills are **loaded** (body read into context for this conversation).
- Which skills are **active** (currently informing the agent's behaviour).

#### Manual Trigger Testing

1. Open a new chat session (clean context).
2. Type a query that should activate the skill. Observe whether it loads.
3. Type a query that should NOT activate the skill. Observe whether it stays silent.
4. If both tests pass, the description is well-calibrated. If not, adjust trigger keywords.

### Thinking from the Agent's Perspective

Monitor how the agent uses your skill in real scenarios. Watch for:

- **Unexpected exploration paths** — the agent reads files you didn't expect. This suggests unclear resource references or an overly broad description.
- **Missed connections** — the agent doesn't find a relevant reference file. The body may not mention it clearly enough.
- **Overreliance** — the agent follows the skill rigidly when the task calls for flexibility. The body may be too prescriptive (reduce the degree of freedom).
- **Ignored content** — the agent skips sections. The body may be too verbose, or those sections may not be relevant to the task at hand.

When you observe any of these, note the specific behaviour and iterate on the skill (§11).

> **Key Takeaway:** Troubleshoot activation failures with VS Code Diagnostics and `skills-ref to-prompt`.

---

## 19. Skill Composition

Skills are designed to be *composed*, not monolithic. The agent can activate multiple skills in a single conversation — each contributing its domain expertise. Design for this.

### The Composability Principle

A well-designed skill library works like a toolkit: each skill covers one domain, and the agent selects the right combination for each task. A "code-review" skill + a "testing" skill + a "deployment" skill compose into a full CI/CD workflow without any single skill needing to know about the others.

This is more effective than one giant "full-stack-development" skill because:
- Only relevant skills load, saving context tokens.
- Each skill can be maintained, tested, and versioned independently.
- New domains are added by writing new skills, not editing existing ones.

### Designing for Composition

#### Non-Overlapping Descriptions

If two skills activate for the same query, their descriptions overlap. The agent may load both (wasting context) or pick the wrong one.

Fix: give each skill a distinct trigger domain. Use "Do not use for…" boundaries when domains are adjacent.

```yaml
# reviewing-code skill
description: >-
  Reviews code for style, logic, and maintainability issues.
  Use when asked to review or critique code.
  Do not use for: writing tests (use testing-code skill instead).

# testing-code skill
description: >-
  Generates unit tests and integration tests for existing code.
  Use when asked to write, add, or generate tests.
  Do not use for: code review (use reviewing-code skill instead).
```

#### Shared Vocabulary

Skills that compose well use consistent terminology. If your "testing" skill refers to "test suites" and your "deployment" skill refers to "test runs" for the same concept, the agent may not connect them.

Establish a shared glossary (or reference it from `copilot-instructions.md`) and use the same terms across all skills.

#### Explicit Handoff Patterns

When a skill's procedure ends at a boundary that another skill handles, mention it:

```markdown
After generating the migration, the deployment skill can apply it to the target database.
```

Frame handoffs as optional enhancements, not hard dependencies. The other skill may not be installed.

#### Complementary with MCP

Skills and MCP servers are complementary:
- **Skills** teach the agent *how* to perform a task (procedures, decisions, domain knowledge).
- **MCP servers** provide *what* the agent needs (external tools, data, API access).

A skill can reference MCP tools by their fully qualified name:

```markdown
Query the database using `DatabaseServer:execute_query` with the SQL from step 3.
```

### Composition Anti-Patterns

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| **The Overlapper** | Two skills both claim to "help with testing" — the agent doesn't know which to load | Give each a distinct trigger domain with explicit boundaries |
| **The Island** | Skill assumes it's the only loaded skill; duplicates setup steps other skills also perform | Move common setup to `copilot-instructions.md` |
| **The Chain** | Skill A says "then use skill B" but doesn't verify skill B exists | Frame as optional: "If the deployment skill is available, use it to apply the migration" |

> **Key Takeaway:** Compose focused skills rather than building monoliths — the agent loads only what's relevant.

---

## 20. Glossary

Consistent vocabulary used throughout this guide and the skill ecosystem. Terms are aligned with the [agentskills.io specification](https://agentskills.io/specification) and the [Session Feedback Guide glossary](copilot-session-feedback-guide.md#glossary-of-key-terms).

| Term | Definition |
|------|-----------|
| **Agent Skill** | An open-standard directory containing a SKILL.md file and optional bundled resources (scripts, references, assets) that teaches an agent how to perform a specific task. Portable across any skills-compatible agent. |
| **Activation** | The moment an agent loads a skill's full SKILL.md body into context, based on semantic matching between the user's intent and the skill's `description` field. Also called "triggering". |
| **Assets** | Files in the `assets/` subdirectory of a skill, used in the skill's output (templates, images, boilerplate). Not loaded into context — the agent copies or modifies them directly. |
| **Body** | The Markdown content below the YAML frontmatter in SKILL.md. Contains procedural instructions loaded only after the skill activates. Maximum 500 lines per the specification. |
| **Bundled Resources** | The optional `scripts/`, `references/`, and `assets/` directories packaged alongside SKILL.md. Each type has a distinct loading behaviour and purpose. |
| **Composability** | The design principle of building multiple focused skills that the agent loads independently, each contributing its domain expertise, rather than one monolithic skill. |
| **Context Window** | The total token budget available to the agent for system prompt, skill content, conversation history, and workspace files. Skills share this finite resource with everything else. |
| **Degrees of Freedom** | The spectrum from high freedom (text-based guidance, many valid approaches) to low freedom (exact scripts, few parameters) that determines how much latitude the agent has when following a skill. |
| **Description** | The `description` field in SKILL.md frontmatter (max 1,024 characters). Serves as the semantic trigger — the agent reads all skill descriptions and decides which to activate based on intent matching. |
| **Discovery** | Level 1 of progressive disclosure. The agent reads only the `name` and `description` of all installed skills to decide which are relevant to the current task. Cost: ~100 tokens per skill. |
| **Frontmatter** | The YAML block at the top of SKILL.md between `---` delimiters. Contains metadata fields (`name`, `description`, and optional fields like `license`, `compatibility`, `metadata`). |
| **Hook** | A deterministic action triggered by a lifecycle event (e.g., pre-commit, session-end). Not a skill — hooks execute unconditionally when their event fires. |
| **MCP (Model Context Protocol)** | A standard for connecting agents to external tools and data sources. Complementary to skills: skills teach *how*, MCP servers provide *what*. |
| **Progressive Disclosure** | The three-level loading strategy: (1) metadata → (2) body → (3) on-demand resources. Designed to minimise context window consumption by loading content only when needed. |
| **References** | Files in the `references/` subdirectory, loaded on demand via `read_file` when the agent determines they are relevant. Does not count against the 500-line body limit. |
| **Scripts** | Executable code in the `scripts/` subdirectory. The most context-efficient resource type — the agent executes them without reading their content into the context window. |
| **Skill Composition** | See *Composability*. |
| **Slash Command** | User-facing invocation mechanism. Type `/skill-name` in chat to manually activate a skill. Availability controlled by the `user-invokable` frontmatter field. |
| **`skills-ref`** | Python reference library and CLI tool from the [agentskills/agentskills](https://github.com/agentskills/agentskills/tree/main/skills-ref) repository. Provides `validate`, `read-properties`, and `to-prompt` commands. |
| **Trigger Engineering** | The practice of crafting the `description` field to reliably activate the skill for relevant tasks while avoiding false positives. Analogous to prompt engineering but for skill discovery. |

> **Key Takeaway:** Key terms defined consistently — use this glossary to align vocabulary across your team.

---

## 21. Quick-Reference Card

A one-page cheat sheet for daily use. Keep this bookmarked.

### Directory Structure

```
.github/skills/<skill-name>/
├── SKILL.md            # Required
├── scripts/            # Optional — executable code
├── references/         # Optional — on-demand docs
└── assets/             # Optional — output resources
```

### Frontmatter Template (All Fields)

```yaml
---
# Spec-standard fields (agentskills.io)
name: my-skill-name                    # Required, 1-64 chars, lowercase + hyphens, must match directory
description: >-                        # Required, 1-1024 chars, no XML tags
  <What — third person>.
  Use when <trigger conditions>.
  Triggers on: <keyword list>.
license: MIT                           # Optional
compatibility: "Requires Python 3.10+" # Optional, max 500 chars
metadata:                              # Optional
  version: "1.0.0"
  author: "Your Name"
allowed-tools: "tool1 tool2"           # Optional, space-delimited (experimental)

# VS Code extension fields (GitHub Copilot-specific)
argument-hint: "Describe the task"     # Optional — shown in chat input
user-invokable: true                   # Optional — show in / menu (default: true)
disable-model-invocation: false        # Optional — prevent auto-load (default: false)
---
```

### Invocation Control Matrix

| `user-invokable` | `disable-model-invocation` | Slash? | Auto? | Use Case |
|---|---|---|---|---|
| true | false | Yes | Yes | General-purpose |
| false | false | No | Yes | Background knowledge |
| true | true | Yes | No | On-demand only |
| false | true | No | No | Disabled |

### Description Formula

```
<What the skill does — third person, 1 sentence>.
Use when <trigger conditions — 1-2 sentences>.
Triggers on: <keyword list>.
Do not use for: <exclusion conditions> (optional).
```

### Naming Rule

Gerund form: `processing-pdfs`, `reviewing-code`, `generating-migrations`
- 1–64 chars, lowercase alphanumeric + hyphens
- No leading/trailing/consecutive hyphens
- Must match directory name

### Body Quick Guide

- Imperative form: "Extract the data", not "The data should be extracted"
- Max 500 lines (aim for < 200)
- Include: procedures, decision logic, resource references
- Exclude: what the agent already knows, "When to Use" (belongs in description)

### Validation Commands

```bash
skills-ref validate .github/skills/my-skill       # Structural check
skills-ref read-properties .github/skills/my-skill # Inspect frontmatter
skills-ref to-prompt .github/skills/my-skill       # See what the agent sees
```

VS Code: Chat settings gear → Diagnostics → view discovered/loaded/active skills.

### Validation Checklist

- [ ] `name` matches directory name
- [ ] `description` ≤ 1,024 characters
- [ ] Body ≤ 500 lines
- [ ] No extraneous files (README.md, CHANGELOG.md)
- [ ] Trigger test passes (skill activates for relevant query)
- [ ] Negative trigger test passes (skill silent for unrelated query)
- [ ] Scripts execute successfully

### Key Links

| Resource | URL |
|----------|-----|
| Agent Skills specification | [agentskills.io/specification](https://agentskills.io/specification) |
| Anthropic best practices | [platform.claude.com/docs/…/best-practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) |
| VS Code Agent Skills docs | [code.visualstudio.com/docs/copilot/customization/agent-skills](https://code.visualstudio.com/docs/copilot/customization/agent-skills) |
| `skills-ref` CLI | [github.com/agentskills/agentskills](https://github.com/agentskills/agentskills/tree/main/skills-ref) |
| Example skills (Anthropic) | [github.com/anthropics/skills](https://github.com/anthropics/skills) |
| Community collection | [github.com/github/awesome-copilot](https://github.com/github/awesome-copilot) |
| Routing Decision Tree | [Session Feedback Guide §5](copilot-session-feedback-guide.md#section-5--routing-decision-tree) |
| SKILL.md Template (Template 5) | [Session Feedback Guide §4](copilot-session-feedback-guide.md#template-5-skillmd-skill-definition) |

> **Key Takeaway:** One page, all essentials — keep this card bookmarked for daily use.

---

*For the full skill-writing process, work through sections 1–21 in order. For the broader feedback lifecycle, see the [Copilot Session-to-Knowledge Feedback Guide](copilot-session-feedback-guide.md).*
