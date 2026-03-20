#!/usr/bin/env python3
# session-end.py — append one session metrics record to sessions/metrics/sessions.jsonl.
#
# Usage:
#   echo '<json>' | python .github/hooks/session-end.py
#
# Requirements: Python 3.8+; stdlib only.

import json
import sys
from datetime import datetime, timezone
from pathlib import Path


def main() -> None:
    try:
        payload = json.loads(sys.stdin.read())
    except (json.JSONDecodeError, ValueError) as exc:
        # Metrics collection failure must never block session close.
        print(f"session-end.py: failed to parse stdin JSON: {exc}", file=sys.stderr)
        sys.exit(0)

    session_id: str = payload.get("sessionId", payload.get("session_id", "")).strip()
    start_ts: str = payload.get("start_ts", "")
    turn_count = payload.get("turn_count", None)

    end_ts = datetime.now(timezone.utc).isoformat()

    duration_seconds = None
    if start_ts:
        try:
            start_dt = datetime.fromisoformat(start_ts.replace("Z", "+00:00"))
            end_dt = datetime.fromisoformat(end_ts)
            duration_seconds = round((end_dt - start_dt).total_seconds())
        except ValueError:
            pass  # Non-fatal: log null duration rather than blocking.

    record = {
        "session_id": session_id or None,
        "start_ts": start_ts or None,
        "end_ts": end_ts,
        "duration_seconds": duration_seconds,
        "turn_count": turn_count,
    }

    metrics_dir = Path("sessions") / "metrics"
    try:
        metrics_dir.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        print(f"session-end.py: failed to create {metrics_dir}: {exc}", file=sys.stderr)
        sys.exit(0)

    jsonl_path = metrics_dir / "sessions.jsonl"
    try:
        with jsonl_path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(record) + "\n")
    except OSError as exc:
        print(f"session-end.py: failed to write {jsonl_path}: {exc}", file=sys.stderr)
        sys.exit(0)

    sys.exit(0)


if __name__ == "__main__":
    main()
