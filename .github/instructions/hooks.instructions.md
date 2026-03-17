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
