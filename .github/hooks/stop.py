#!/usr/bin/env python3
# stop.py — archive session transcript to sessions/YYYY-MM-DD/<session_id>/
# Assumes CWD == repository root (set automatically by VS Code hook runner).

import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

# Allow sibling hook modules to be imported when running as a standalone script.
sys.path.insert(0, str(Path(__file__).parent))
from _trace import read_trace_id  # noqa: E402


def main() -> None:
    # Read stdin payload first — loop guard field is in the JSON.
    try:
        payload = json.loads(sys.stdin.read())
    except (json.JSONDecodeError, ValueError) as exc:
        print(f"stop.py: failed to parse stdin JSON: {exc}", file=sys.stderr)
        sys.exit(2)

    # Loop guard — must check before doing any work. Prevents infinite Stop hook recursion.
    # stop_hook_active is a boolean in the VS Code hook stdin payload.
    if payload.get("stop_hook_active") is True:
        sys.exit(0)

    session_id: str = payload.get("sessionId", payload.get("session_id", "")).strip()
    transcript_path: str = payload.get("transcript_path", "").strip()

    # Validate required fields.
    if not session_id:
        print("stop.py: stdin missing 'session_id' field", file=sys.stderr)
        sys.exit(2)
    if not transcript_path:
        print("stop.py: stdin missing 'transcript_path' field", file=sys.stderr)
        sys.exit(2)

    src = Path(transcript_path)
    if not src.exists():
        print(
            f"stop.py: transcript_path does not exist: {transcript_path}",
            file=sys.stderr,
        )
        sys.exit(2)

    # Build destination: sessions/YYYY-MM-DD/<session_id>/
    date_str = datetime.now().strftime("%Y-%m-%d")
    dest_dir = Path("sessions") / date_str / session_id
    try:
        dest_dir.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        print(f"stop.py: failed to create {dest_dir}: {exc}", file=sys.stderr)
        sys.exit(2)

    # Copy transcript.
    dest_transcript = dest_dir / "transcript.json"
    try:
        shutil.copy2(src, dest_transcript)
    except OSError as exc:
        print(f"stop.py: failed to copy transcript: {exc}", file=sys.stderr)
        sys.exit(1)

    # Write metadata.
    metadata = {
        "session_id": session_id,
        "trace_id": read_trace_id(),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "size_bytes": dest_transcript.stat().st_size,
        "source": transcript_path,
    }
    try:
        (dest_dir / "metadata.json").write_text(
            json.dumps(metadata, indent=2), encoding="utf-8"
        )
    except OSError as exc:
        print(f"stop.py: failed to write metadata: {exc}", file=sys.stderr)
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
