#!/usr/bin/env python3
# pre-tool-use.py — security gate: block protected file deletion and dangerous terminal commands

import json
import os
import sys
from pathlib import Path


PATTERNS_FILE = Path(".github/security-patterns.json")

# Tools that operate on files.
FILE_TOOLS = {"write_file", "edit_file", "delete_file", "rename_file", "move_file"}

# Tools that run shell/terminal commands.
TERMINAL_TOOLS = {"run_terminal", "run_in_terminal", "bash", "powershell"}


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


def check_file_operation(tool_input: dict, patterns: dict) -> str | None:
    """Return a block reason string if the file operation matches a protected pattern."""
    protected: list[str] = patterns.get("protected_files", [])
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
    for protected_pattern in protected:
        norm_pattern = normalise(protected_pattern)
        if norm_path == norm_pattern or norm_path.startswith(norm_pattern.rstrip("/") + "/"):
            return f"path '{path_str}' matches protected pattern '{protected_pattern}'"

    return None


def check_terminal_command(tool_input: dict, patterns: dict) -> str | None:
    """Return a block reason string if the command matches a dangerous pattern."""
    dangerous: list[str] = patterns.get("dangerous_terminal", [])
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
    for pattern in dangerous:
        if normalise(pattern) in norm_cmd:
            return f"command matches dangerous pattern '{pattern}'"

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

    block_reason: str | None = None

    if tool_name in FILE_TOOLS:
        block_reason = check_file_operation(tool_input, patterns)
    elif tool_name in TERMINAL_TOOLS:
        block_reason = check_terminal_command(tool_input, patterns)

    if block_reason:
        print(
            f"BLOCKED by pre-tool-use security gate: {block_reason}.\n"
            f"If this is intentional, run the command manually in your terminal.",
            file=sys.stderr,
        )
        sys.exit(2)

    sys.exit(0)


if __name__ == "__main__":
    main()
