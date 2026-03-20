---
name: template-library
description: "Provides validated templates for all six GitHub Copilot integration surfaces. Use when creating a new rule, instruction file, prompt, agent, skill, or hook — the template encodes all required fields and exit-code contracts so nothing is missed. Triggers on: 'create rule', 'write instruction', 'new instruction', 'write prompt', 'create prompt', 'create agent', 'write agent', 'write skill', 'create skill', 'configure hook', 'new hook', 'scaffold', 'template'."
metadata:
  version: "1.0.0"
---

# Template Library

Validated scaffold templates for all six GitHub Copilot knowledge surfaces.

## When to Use

Load this skill whenever you are creating or scaffolding one of the six surfaces. Apply the
template **before** writing the artifact. Fill every `# REQUIRED` field. `# OPTIONAL` fields
may be omitted if not applicable.

| Surface | Template | Trigger phrases |
|---------|----------|-----------------|
| Global rule | T1 | "create rule", "add rule to copilot-instructions.md" |
| Scoped instruction | T2 | "write instruction", "new instructions file" |
| Prompt file | T3 | "write prompt", "create prompt", "slash command" |
| Agent file | T4 | "create agent", "write agent", "new agent" |
| Skill file | T5 | "write skill", "create skill", "new skill" |
| Hook | T6 | "configure hook", "new hook", "write hook" |

---

## T1 — `copilot-instructions.md` Rule

A single rule entry for the global always-on instruction file.

```markdown
Rule: <Imperative sentence stating what the agent should do.>
Reason: <Why this rule was created — the triggering observation or recurring problem.>
```

**Validation checklist (apply before adding):**
- [ ] Positive framing — says what TO do, not what to avoid
- [ ] Includes `Reason:` clause with concrete justification
- [ ] Specific — agent can apply without asking a follow-up question
- [ ] Scoped correctly — belongs in global instructions (affects every file/session)
- [ ] Non-contradictory — does not conflict with any existing rule
- [ ] Tested — confirmed to produce intended behaviour in ≥ 1 session

**Cap check:** `copilot-instructions.md` must stay ≤ 200 lines. If adding this rule would
exceed the cap, split domain rules into a scoped `*.instructions.md` instead.

---

## T2 — `*.instructions.md` Scoped Instruction File

A conditional instruction file that activates only for files matching `applyTo`.

```markdown
---                              # REQUIRED
name: <slug>                     # REQUIRED — matches filename (minus .instructions.md)
description: "<one sentence>"    # REQUIRED — what this instruction does and when it applies
applyTo: "<glob>"                # REQUIRED — e.g. "sessions/**", "**/*.ts", "docs/**"
---

# <Title>

<One-sentence summary of this instruction's domain.>

Rule: <First rule statement.>
Reason: <Why this rule was created.>

Rule: <Second rule statement.>
Reason: <Why this rule was created.>
```

**Required fields:** `name`, `description`, `applyTo`, at least one `Rule:` + `Reason:` pair.
**Cap check:** ≤ 100 lines per file. If exceeded, create a second scoped file for the same domain.

---

## T3 — `*.prompt.md` Prompt File

A slash-command prompt file placed in `.github/prompts/`.

```markdown
---                                      # REQUIRED
description: "<Trigger description.>"   # REQUIRED — what invokes this prompt
mode: ask | agent | edit                # REQUIRED — select one
tools:                                  # OPTIONAL — omit for mode default
  - read/readFile
  - search/codebase
model: <model-name>                     # OPTIONAL — omit to use user's selected model
---

## Instructions

1. <First instruction step.>
2. <Second instruction step.>

## Output Format

<Describe the expected output structure.>
```

**Required fields:** `description`, `mode`.
**Cap check:** ≤ 150 lines body. If exceeded, extract reusable sections into a skill reference.
**Mode guide:**
- `ask` — read-only, conversational response; use for analysis, verification, audits
- `agent` — autonomous with tools; use for multi-step workflows that need file access
- `edit` — targeted file edits in focused context; use for code transformation tasks

---

## T4 — `*.agent.md` Agent File

A custom agent placed in `.github/agents/`.

```markdown
---                                                    # REQUIRED
name: <agent-name>                                     # REQUIRED — must match filename
description: "<One-line role + specialisation.>"       # REQUIRED
tools:                                                 # OPTIONAL — omit for all tools
  - read/readFile                                      #   use category/name format
  - search/listDirectory
  - search/textSearch
  - search/codebase
handoffs:                                              # OPTIONAL — for RPI chains
  - label: <Button text>
    agent: <target-agent-name>
    prompt: <Pre-filled message for the next agent.>
    send: false
user-invokable: true                                   # OPTIONAL — false = subagent only
---

You are a <role>. Your job is to <one sentence of core purpose>. You never <boundary>.

## Procedure

1. <Step 1 — concrete action.>
2. <Step 2 — concrete action.>
3. <Step 3 — concrete action.>

## Output Format

| Column A | Column B |
|----------|----------|
| ...      | ...      |

## Rules

- <Hard constraint 1.>
- <Hard constraint 2.>
- Never edit files (if read-only agent).
```

**Required fields:** `name`, `description`, persona statement, at least one procedure step,
at least one rule.
**Tool IDs:** Use `read/readFile`, `edit/editFiles`, `search/listDirectory`,
`search/textSearch`, `search/codebase`, `search/fileSearch`, `execute/runInTerminal`, `todo`.
**Cap check:** body ≤ 150 lines. If exceeded, the agent is doing too much — split.

---

## T5 — `SKILL.md` Skill File

A skill file in `.github/skills/<skill-name>/SKILL.md`.

```markdown
---                                            # REQUIRED
name: <skill-name>                             # REQUIRED — matches directory name
description: "<Trigger-engineered summary.>"  # REQUIRED — include trigger phrases
metadata:                                      # OPTIONAL
  version: "1.0.0"
---

# <Skill Title>

## When to Use

<1-3 sentences: what problem this skill solves and when to invoke it.>

## Procedure

1. <Step 1.>
2. <Step 2.>
3. <Step 3.>

## Output Format

<Describe the expected output.>
```

**Required fields:** `name`, `description`, body with When to Use and Procedure sections.
**Cap check:** ≤ 500 lines. If exceeded, split into core `SKILL.md` + `references/` documents.
**Description tip:** Include trigger phrases in the description — the model uses these to
activate the skill. Be specific: "apply four diagnostic lenses" beats "analyze sessions".

---

## T6 — Hook JSON + Python Script

A lifecycle hook consisting of a JSON config and a Python script.

**JSON config** (`.github/hooks/<event-kebab>.json`):

```json
{
    "hooks": {
        "<EventName>": [
            {
                "type": "command",
                "command": "python .github/hooks/<script-name>.py"
            }
        ]
    }
}
```

Valid `<EventName>` values: `SessionStart`, `SessionEnd`, `PreToolUse`, `PostToolUse`,
`PreCompact`, `PostCompact`, `Stop`, `Notification`.

**Python script** (`.github/hooks/<script-name>.py`):

```python
#!/usr/bin/env python3                # REQUIRED — shebang line
# <script-name>.py — <one-sentence description>  # REQUIRED — file header convention

import json
import sys
# Add stdlib imports as needed (pathlib, subprocess, shutil, os, datetime)
# NO third-party packages — stdlib only


def main() -> None:
    # === STOP HOOK ONLY: loop guard must be line 1 of main logic ===
    # import os
    # if os.environ.get("STOP_HOOK_ACTIVE") == "1":
    #     sys.exit(0)

    # Read stdin (hook payload)
    raw = sys.stdin.read()
    data = json.loads(raw) if raw.strip() else {}

    # --- Hook logic here ---

    # Exit code contract:           # REQUIRED
    # sys.exit(0)  — success
    # sys.exit(2)  — soft block (provide explanation on stderr; developer can override)
    # sys.exit(1)  — hard fail (only for unrecoverable errors; avoid for safety hooks)

    # Optional: output JSON for additionalContext injection
    # print(json.dumps({"additionalContext": "<content>"}))

    sys.exit(0)


if __name__ == "__main__":
    main()
```

**Required fields:** shebang, file header comment (`# filename — description`), `main()`
function, exit code contract.
**Stop hook:** MUST include `stop_hook_active` loop guard as the first conditional check
inside `main()`. Omitting it causes an infinite loop.
**Execution budget:** < 500ms. Scripts calling `subprocess` must use `timeout=` parameter.
**Context injection:** Only inject `additionalContext` from hooks that fire early in the
session (SessionStart, PostCompact). Late hooks (Stop) should not inject context.
