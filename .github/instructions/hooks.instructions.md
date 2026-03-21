---
applyTo: ".github/hooks/stop.json,.github/hooks/pre-tool-use.json,.github/hooks/post-tool-use.json,.github/hooks/session-start.json,.github/hooks/pre-compact.json,.github/hooks/post-compact.json"
---

# Hook JSON Format Rules

## Required Schema

Structure every hook JSON file with `hooks` as an **object** keyed by the PascalCase event name, where each value is an array of command objects.
Reason: VS Code rejects flat structures and array-wrapped variants — only the object-keyed format is loaded.

```json
{
  "hooks": {
    "EventName": [
      { "type": "command", "command": "python .github/hooks/<script>.py" }
    ]
  }
}
```

Valid event names: `Stop`, `PreToolUse`, `PostToolUse`, `SessionStart`, `PreCompact`, `PostCompact`.

## Required Fields

Include both `"type": "command"` and `"command": "..."` in every entry inside the event array.
Reason: omitting `"type"` causes VS Code to silently skip the hook entry even when the event name and command are correct.

## Escalation Message Schema for Soft-Blocks (Exit Code 2)

Every PreToolUse soft-block (exit code 2) must write a 3-field escalation message to stderr.
Reason: Ch. 8 (Agent Calls Human) requires escalation messages to be actionable — the developer must understand what was blocked, why it is protected, and how to proceed. Missing fields cause confusion and may lead to the hook being disabled.

### Required Format

```
BLOCKED: <action attempted in one line>
REASON:  <why this action is protected — policy or risk>
NEXT:    <what the developer should do instead, or how to override>
```

### Example — Protected File

```
BLOCKED: Attempted file operation on protected path '.github/copilot-instructions.md'
REASON:  This file contains the workspace-wide Copilot instruction set. Deleting it removes all agent guidance.
NEXT:    Edit the file content instead of deleting it, or delete it manually in your terminal if you are certain.
```

### Example — Dangerous Terminal Command

```
BLOCKED: Attempted to run a command matching dangerous pattern 'rm -rf'
REASON:  Recursive force-delete is irreversible and may remove files outside the intended scope.
NEXT:    Run the command manually in your terminal after confirming the target path is correct.
```

### Providing Pattern-Level Messages

Add `reason` and `next` fields to each entry in `security-patterns.json` to supply pattern-specific escalation text.
Reason: pattern-specific messages give the developer more actionable context than a generic fallback.

```json
{
  "dangerous_terminal": [
    {
      "pattern": "git push --force",
      "reason": "Force-push rewrites remote history and cannot be undone by other collaborators.",
      "next": "Use 'git push --force-with-lease' for a safer alternative, or run manually if you are certain."
    }
  ]
}
```
