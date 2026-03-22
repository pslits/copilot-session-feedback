#!/usr/bin/env python3
# post-tool-use.py — auto-format written files using the project formatter

import json
import subprocess
import sys
from pathlib import Path

# Only act on these tool names — all others are non-file-write events.
WRITE_TOOLS = {"write_file", "edit_file", "create_file"}

# Map file extension → formatter argv (file path appended as last arg).
FORMATTER_MAP = {
    ".md": ["npx", "prettier", "--write"],
    ".json": ["npx", "prettier", "--write"],
    ".yaml": ["npx", "prettier", "--write"],
    ".yml": ["npx", "prettier", "--write"],
    ".ts": ["npx", "prettier", "--write"],
    ".tsx": ["npx", "prettier", "--write"],
    ".js": ["npx", "prettier", "--write"],
    ".jsx": ["npx", "prettier", "--write"],
    ".css": ["npx", "prettier", "--write"],
    ".py": ["black"],
}


def get_file_path(tool_input: dict) -> str:
    """Extract the file path from the tool input dict (key name varies by tool)."""
    return (
        tool_input.get("filePath")
        or tool_input.get("path")
        or tool_input.get("file_path")
        or tool_input.get("target_file")
        or ""
    )


def run_formatter(cmd: list[str], file_path: str) -> None:
    """Invoke the formatter subprocess; degrade gracefully on any failure."""
    full_cmd = cmd + [file_path]
    try:
        result = subprocess.run(
            full_cmd,
            timeout=5,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            print(
                f"post-tool-use.py: formatter exited {result.returncode} for {file_path}",
                file=sys.stderr,
            )
            if result.stderr:
                print(result.stderr.strip(), file=sys.stderr)
    except FileNotFoundError:
        # Formatter not installed — degrade silently.
        cmd_name = full_cmd[0]
        print(
            f"post-tool-use.py: formatter '{cmd_name}' not found; skipping {file_path}",
            file=sys.stderr,
        )
    except subprocess.TimeoutExpired:
        print(
            f"post-tool-use.py: formatter timed out for {file_path}; skipping",
            file=sys.stderr,
        )


def main() -> None:
    # Read stdin payload.
    try:
        payload = json.loads(sys.stdin.read())
    except (json.JSONDecodeError, ValueError):
        sys.exit(0)

    tool_name: str = payload.get("tool_name", "").strip().lower()

    # Only act on file-write tools.
    if tool_name not in WRITE_TOOLS:
        sys.exit(0)

    tool_input: dict = payload.get("tool_input", {})
    if not isinstance(tool_input, dict):
        sys.exit(0)

    file_path = get_file_path(tool_input)
    if not file_path:
        sys.exit(0)

    # Look up formatter by extension.
    ext = Path(file_path).suffix.lower()
    formatter_cmd = FORMATTER_MAP.get(ext)
    if not formatter_cmd:
        # No formatter registered for this extension — nothing to do.
        sys.exit(0)

    run_formatter(formatter_cmd, file_path)
    sys.exit(0)


if __name__ == "__main__":
    main()
