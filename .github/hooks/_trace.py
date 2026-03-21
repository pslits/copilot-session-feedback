#!/usr/bin/env python3
# _trace.py — shared trace ID helpers for all lifecycle hook scripts

from datetime import datetime, timezone
from pathlib import Path

TRACE_ID_PATH = Path("sessions") / ".current_trace_id"
START_TS_PATH = Path("sessions") / ".current_start_ts"


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
