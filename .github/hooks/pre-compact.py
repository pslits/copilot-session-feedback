#!/usr/bin/env python3
# pre-compact.py — export full context snapshot to sessions/precompact/ before compression
# Assumes CWD == repository root (set automatically by VS Code hook runner).

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

# Allow sibling hook modules to be imported when running as a standalone script.
sys.path.insert(0, str(Path(__file__).parent))
from _trace import read_trace_id  # noqa: E402


def main() -> None:
    # Read the full stdin payload without asserting specific fields
    raw = sys.stdin.read()
    try:
        payload = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        # Malformed stdin — write the raw string wrapped in a JSON object
        payload = {"raw": raw}

    # Derive session_id from payload or fall back to a timestamp-based ID
    session_id = payload.get("session_id") or f"session-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')}"

    # Build a timestamped filename — idempotent across multiple compressions per session
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    dest_dir = Path("sessions") / "precompact"
    filename = dest_dir / f"{session_id}-{timestamp}.json"

    # Create destination directory (exist_ok=True — safe if already present)
    try:
        dest_dir.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        print(f"pre-compact: could not create {dest_dir}: {exc}", file=sys.stderr)
        sys.exit(2)

    # Write the snapshot — include the raw payload plus capture timestamp and trace ID
    snapshot = {
        "captured_at": timestamp,
        "session_id": session_id,
        "trace_id": read_trace_id(),
        "payload": payload,
    }

    try:
        filename.write_text(json.dumps(snapshot, indent=2), encoding="utf-8")
    except OSError as exc:
        print(f"pre-compact: could not write snapshot to {filename}: {exc}", file=sys.stderr)
        sys.exit(2)

    sys.exit(0)


if __name__ == "__main__":
    main()
