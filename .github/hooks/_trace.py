#!/usr/bin/env python3
# _trace.py — shared trace ID helpers for all lifecycle hook scripts
# Assumes CWD == repository root (set automatically by VS Code hook runner).

from datetime import datetime, timezone
from pathlib import Path

TRACE_ID_PATH = Path("sessions") / ".current_trace_id"
START_TS_PATH = Path("sessions") / ".current_start_ts"
TURN_COUNT_PATH = Path("sessions") / ".current_turn_count"
CORRECTIONS_PATH = Path("sessions") / ".current_corrections"


def read_trace_id() -> str:
    """Read the session trace ID written by session-start.py.

    Returns the UUID v4 string from ``sessions/.current_trace_id``.
    Falls back to ``'unknown-<timestamp>'`` if the file is missing or
    unreadable, ensuring downstream records are still written (albeit
    without a real session correlation key).
    """
    try:
        return TRACE_ID_PATH.read_text(encoding="utf-8").strip()
    except OSError:
        fallback_ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        return f"unknown-{fallback_ts}"


def read_start_ts() -> str | None:
    """Read the session start timestamp written by session-start.py.

    Returns the ISO 8601 string from ``sessions/.current_start_ts``,
    or ``None`` if the file is missing or unreadable.
    """
    try:
        value = START_TS_PATH.read_text(encoding="utf-8").strip()
        return value if value else None
    except OSError:
        return None


def read_turn_count() -> int | None:
    """Read the tool-call counter written by post-tool-use.py.

    Returns the integer count, or ``None`` if the file is missing or unreadable.
    """
    try:
        return int(TURN_COUNT_PATH.read_text(encoding="utf-8").strip())
    except (OSError, ValueError):
        return None


def increment_turn_count() -> None:
    """Atomically increment the per-session tool-call counter.

    Called by post-tool-use.py on every tool-use event.  Non-fatal on any
    OS error so it never blocks the agent.
    """
    try:
        TURN_COUNT_PATH.parent.mkdir(parents=True, exist_ok=True)
        current = 0
        if TURN_COUNT_PATH.exists():
            try:
                current = int(TURN_COUNT_PATH.read_text(encoding="utf-8").strip())
            except (OSError, ValueError):
                pass
        TURN_COUNT_PATH.write_text(str(current + 1), encoding="utf-8")
    except OSError:
        pass  # Non-fatal — loss of turn count is acceptable


def reset_turn_count() -> None:
    """Delete the turn-count file to start a fresh count for the next session.

    Called by session-start.py at session open and by session-end.py after
    the count has been recorded.
    """
    try:
        if TURN_COUNT_PATH.exists():
            TURN_COUNT_PATH.unlink()
    except OSError:
        pass  # Non-fatal


def read_corrections() -> list:
    """Read structured correction records written to sessions/.current_corrections.

    Each record is a JSON object with fields:
      - lens (int 1–4)
      - mistake (str): what the agent did wrong
      - rule_change (str): what rule was added or changed
      - rule_ref (str | null): path to the artifact affected

    Returns an empty list if the file is missing, empty, or malformed.
    """
    import json as _json
    try:
        raw = CORRECTIONS_PATH.read_text(encoding="utf-8").strip()
        if not raw:
            return []
        parsed = _json.loads(raw)
        if isinstance(parsed, list):
            return parsed
        return []
    except (OSError, ValueError):
        return []


def reset_corrections() -> None:
    """Delete the corrections file to start fresh for the next session.

    Called by session-end.py after the corrections have been recorded.
    """
    try:
        if CORRECTIONS_PATH.exists():
            CORRECTIONS_PATH.unlink()
    except OSError:
        pass  # Non-fatal
