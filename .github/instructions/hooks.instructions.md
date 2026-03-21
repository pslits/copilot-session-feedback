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

## Timeout Budget

Every hook script must complete within **5000ms** (measured from hook invocation to process exit).
Reason: a hanging hook blocks the VS Code agent indefinitely — the 5000ms ceiling prevents
indefinite hangs while accommodating the slowest legitimate operation (formatter subprocess).

### Per-hook budget breakdown

| Hook | External calls | Typical runtime | Budget headroom |
|---|---|---|---|
| `stop.py` | Local FS only (file copy + metadata write) | < 50ms | Large |
| `session-end.py` | Local FS only (append one JSONL line) | < 10ms | Large |
| `post-compact.py` | Local FS only (read one file) | < 10ms | Large |
| `pre-compact.py` | Local FS only (read one file) | < 10ms | Large |
| `session-start.py` | Local FS only | < 10ms | Large |
| `pre-tool-use.py` | Local FS only (read patterns file) | < 10ms | Large |
| `notification.py` | HTTP via `urllib` with `timeout=2` | < 2500ms | Comfortable |
| `post-tool-use.py` | Subprocess (`npx prettier` / `black`) with `timeout=5` | < 5000ms | At limit |

### Soft-fail contract

When any hook script exceeds the budget or encounters an unrecoverable error, exit with code **2**
(soft block). Exit code 2 informs the VS Code agent of the failure without hard-blocking the
session.
Reason: exit 2 allows the agent to log and surface the issue without preventing session
continuation — hook failures are advisory, not fatal.

### Rules for external calls in hooks

- All network calls must carry an explicit timeout of ≤ 5000ms total.
  Reason: unbounded network calls are the primary hang source in hook scripts.
- All subprocess invocations must use `timeout=` (Python) or `timeout <seconds>` (shell).
  Reason: a formatter or tool left running indefinitely will consume the entire budget.
- Hook scripts must not make remote `git` calls (fetch, push, pull).
  Reason: remote git operations can block on network or authentication and have no bounded runtime.
