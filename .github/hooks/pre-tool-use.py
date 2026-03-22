#!/usr/bin/env python3
# pre-tool-use.py — security gate: block protected file deletion and dangerous terminal commands
# Assumes CWD == repository root (set automatically by VS Code hook runner).

import json
import os
import sys
from pathlib import Path


PATTERNS_FILE = Path(".github/security-patterns.json")

# Tools that operate on files (write/delete/rename).
FILE_TOOLS = {"write_file", "edit_file", "delete_file", "rename_file", "move_file", "create_file"}

# Tools that run shell/terminal commands.
TERMINAL_TOOLS = {"run_terminal", "run_in_terminal", "bash", "powershell"}

# Tools that read file content — checked against credential_access patterns.
CREDENTIAL_ACCESS_TOOLS = {"read_file", "open_file", "view_file", "cat"}

# MCP git tools that bypass the terminal security gate — always blocked.
MCP_GIT_TOOLS = {"mcp_gitkraken_git_add_or_commit", "mcp_gitkraken_git_push"}


def load_patterns() -> dict:
    """Load blocked patterns from the project-local config file.

    Returns an empty dict if the file is missing — no patterns means no blocks.
    """
    if not PATTERNS_FILE.exists():
        return {}
    try:
        return json.loads(PATTERNS_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


def normalise(value: str) -> str:
    return value.lower().replace("\\", "/")


_DEFAULT_REASON = "This operation is blocked by the security gate policy."
_DEFAULT_NEXT = "Run the operation manually in your terminal if this is intentional."


def _entry_fields(entry: "str | dict") -> tuple[str, str, str]:
    """Return (pattern, reason, next_steps) from a string or dict entry."""
    if isinstance(entry, str):
        return entry, _DEFAULT_REASON, _DEFAULT_NEXT
    pattern = entry.get("pattern", "")
    reason = entry.get("reason", _DEFAULT_REASON)
    next_steps = entry.get("next", _DEFAULT_NEXT)
    return pattern, reason, next_steps


def check_file_operation(tool_input: dict, patterns: dict) -> dict | None:
    """Return a 3-field block message dict if the file operation matches a protected pattern."""
    protected: list = patterns.get("protected_files", [])
    if not protected:
        return None

    # VS Code uses camelCase for tool_input properties; fall back to snake_case for
    # compatibility with Claude Code / Copilot CLI hook scripts.
    path_str: str = (
        tool_input.get("filePath")
        or tool_input.get("path")
        or tool_input.get("file_path")
        or tool_input.get("target")
        or ""
    )
    if not path_str:
        return None

    norm_path = normalise(path_str)
    for entry in protected:
        pattern, reason, next_steps = _entry_fields(entry)
        norm_pattern = normalise(pattern)
        if norm_path == norm_pattern or norm_path.startswith(norm_pattern.rstrip("/") + "/"):
            return {
                "blocked": f"Attempted file operation on protected path '{path_str}'",
                "reason": reason,
                "next": next_steps,
            }

    return None


def check_terminal_command(tool_input: dict, patterns: dict) -> dict | None:
    """Return a 3-field block message dict if the command matches a dangerous pattern."""
    dangerous: list = patterns.get("dangerous_terminal", [])
    if not dangerous:
        return None

    command: str = (
        tool_input.get("command")
        or tool_input.get("cmd")
        or tool_input.get("input")
        or ""
    )
    if not command:
        return None

    norm_cmd = normalise(command)
    for entry in dangerous:
        pattern, reason, next_steps = _entry_fields(entry)
        if normalise(pattern) in norm_cmd:
            return {
                "blocked": f"Attempted to run a command matching dangerous pattern '{pattern}'",
                "reason": reason,
                "next": next_steps,
            }

    return None


def check_mcp_git_operation(tool_name: str, patterns: dict) -> dict | None:
    """Return a block message if the MCP git tool is in the blocked list.

    MCP git tools bypass the terminal security gate entirely; they must be
    hard-blocked here so the agent is redirected to terminal git, where
    dangerous_terminal patterns (e.g. push-to-main guards) can fire.
    """
    blocked: list = patterns.get("blocked_mcp_tools", [])
    for entry in blocked:
        pattern, reason, next_steps = _entry_fields(entry)
        if tool_name == pattern.lower():
            return {
                "blocked": f"Attempted to use blocked MCP git tool '{tool_name}'",
                "reason": reason,
                "next": next_steps,
            }
    return None


def check_credential_access(tool_input: dict, patterns: dict) -> dict | None:
    """Return a 3-field block message dict if the file path matches a credential access pattern."""
    credential_patterns: list = patterns.get("credential_access", [])
    if not credential_patterns:
        return None

    path_str: str = (
        tool_input.get("filePath")
        or tool_input.get("path")
        or tool_input.get("file_path")
        or tool_input.get("target")
        or ""
    )
    if not path_str:
        return None

    norm_path = normalise(path_str)
    for entry in credential_patterns:
        pattern, reason, next_steps = _entry_fields(entry)
        if normalise(pattern) in norm_path or norm_path == normalise(pattern):
            return {
                "blocked": f"Attempted to access credential file '{path_str}'",
                "reason": reason,
                "next": next_steps,
            }

    return None


def main() -> None:
    # Read stdin payload.
    try:
        payload = json.loads(sys.stdin.read())
    except (json.JSONDecodeError, ValueError):
        # Cannot parse — allow the tool call to proceed (fail open).
        sys.exit(0)

    tool_name: str = payload.get("tool_name", "").strip().lower()
    tool_input: dict = payload.get("tool_input", {})
    if not isinstance(tool_input, dict):
        tool_input = {}

    patterns = load_patterns()

    block_msg: dict | None = None

    if tool_name in FILE_TOOLS:
        block_msg = check_file_operation(tool_input, patterns)
        if not block_msg:
            block_msg = check_credential_access(tool_input, patterns)
    elif tool_name in TERMINAL_TOOLS:
        block_msg = check_terminal_command(tool_input, patterns)
    elif tool_name in CREDENTIAL_ACCESS_TOOLS:
        block_msg = check_credential_access(tool_input, patterns)
    elif tool_name in MCP_GIT_TOOLS:
        block_msg = check_mcp_git_operation(tool_name, patterns)

    if block_msg:
        print(
            f"BLOCKED: {block_msg['blocked']}\n"
            f"REASON:  {block_msg['reason']}\n"
            f"NEXT:    {block_msg['next']}",
            file=sys.stderr,
        )
        sys.exit(2)

    sys.exit(0)


if __name__ == "__main__":
    main()
