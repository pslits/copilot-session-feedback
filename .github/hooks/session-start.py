#!/usr/bin/env python3
# session-start.py — inject project metadata (name, branch, commit, version) into session context

import json
import os
import subprocess
import sys
from datetime import datetime, timezone


def run_git(args: list[str]) -> str:
    """Run a git command and return stdout, or 'unknown' on any failure."""
    try:
        result = subprocess.run(
            args,
            capture_output=True,
            text=True,
            timeout=2,
        )
        return result.stdout.strip() if result.returncode == 0 else "unknown"
    except Exception:
        return "unknown"


def read_package_version() -> str:
    """Read version from package.json, or 'n/a' if absent or missing the field."""
    try:
        with open("package.json", encoding="utf-8") as f:
            return json.load(f).get("version", "n/a")
    except Exception:
        return "n/a"


def main() -> None:
    # Read stdin (ignore contents — SessionStart payload may be empty)
    try:
        raw = sys.stdin.read()
        _ = json.loads(raw) if raw.strip() else {}
    except Exception:
        pass  # Graceful degradation: continue even if stdin is malformed

    # Collect orientation metadata — each field degrades individually on failure
    project = os.path.basename(os.getcwd())
    branch = run_git(["git", "rev-parse", "--abbrev-ref", "HEAD"])
    commit_sha = run_git(["git", "log", "-1", "--format=%H"])
    version = read_package_version()
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    # Build additionalContext — aim for ≤ 100 tokens (≈ 400 characters)
    context_lines = [
        f"project: {project}",
        f"branch: {branch}",
        f"commit: {commit_sha[:12] if commit_sha != 'unknown' else 'unknown'}",
        f"version: {version}",
        f"session_opened: {timestamp}",
    ]
    additional_context = "\n".join(context_lines)

    output = {"additionalContext": additional_context}
    print(json.dumps(output))
    sys.exit(0)  # Always exit 0 — SessionStart must never block session opening


if __name__ == "__main__":
    main()
