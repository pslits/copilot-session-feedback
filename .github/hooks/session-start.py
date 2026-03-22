#!/usr/bin/env python3
# session-start.py — inject project metadata (name, branch, commit, version) into session context

import json
import os
import subprocess
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _trace import TRACE_ID_PATH, START_TS_PATH  # noqa: E402


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


def generate_trace_id() -> str:
    """Generate a UUID v4 trace ID for this session."""
    return str(uuid.uuid4())


def persist_trace_id(trace_id: str) -> None:
    """Write the trace ID to disk so all downstream hooks can read it."""
    try:
        TRACE_ID_PATH.parent.mkdir(parents=True, exist_ok=True)
        TRACE_ID_PATH.write_text(trace_id, encoding="utf-8")
    except OSError as exc:
        print(
            f"session-start.py: could not persist trace ID: {exc}. "
            "Downstream hooks will fall back to a synthetic 'unknown-<timestamp>' ID; "
            "trace correlation for this session will be unavailable.",
            file=sys.stderr,
        )


def persist_start_ts(timestamp: str) -> None:
    """Write the session start timestamp to disk so session-end.py can compute duration."""
    try:
        START_TS_PATH.parent.mkdir(parents=True, exist_ok=True)
        START_TS_PATH.write_text(timestamp, encoding="utf-8")
    except OSError as exc:
        print(
            f"session-start.py: could not persist start timestamp: {exc}. "
            "Session duration will be unavailable.",
            file=sys.stderr,
        )


def main() -> None:
    # Read stdin (ignore contents — SessionStart payload may be empty)
    try:
        raw = sys.stdin.read()
        _ = json.loads(raw) if raw.strip() else {}
    except Exception:
        pass  # Graceful degradation: continue even if stdin is malformed

    # Generate and persist the session trace ID — must happen before metadata collection
    trace_id = generate_trace_id()
    persist_trace_id(trace_id)

    # Collect orientation metadata — each field degrades individually on failure
    project = os.path.basename(os.getcwd())
    branch = run_git(["git", "rev-parse", "--abbrev-ref", "HEAD"])
    commit_sha = run_git(["git", "log", "-1", "--format=%H"])
    version = read_package_version()
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    # Persist start timestamp so session-end.py can compute duration even when VS Code
    # does not include start_ts in the SessionEnd payload.
    persist_start_ts(timestamp)

    # Build additionalContext — aim for ≤ 100 tokens (≈ 400 characters)
    context_lines = [
        f"project: {project}",
        f"branch: {branch}",
        f"commit: {commit_sha[:12] if commit_sha != 'unknown' else 'unknown'}",
        f"version: {version}",
        f"session_opened: {timestamp}",
        f"trace_id: {trace_id}",
    ]
    additional_context = "\n".join(context_lines)

    output = {"additionalContext": additional_context}
    print(json.dumps(output))
    sys.exit(0)  # Always exit 0 — SessionStart must never block session opening


if __name__ == "__main__":
    main()
