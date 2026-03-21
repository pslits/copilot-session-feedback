"""Regression tests for .github/hooks/session-end.py — session metrics JSONL append."""

import json
from datetime import datetime
from pathlib import Path

import pytest

from helpers import run_hook

_JSONL_PATH = Path("sessions") / "metrics" / "sessions.jsonl"
_TRACE_ID_PATH = Path("sessions") / ".current_trace_id"


def _read_records(tmp_path: Path) -> list[dict]:
    path = tmp_path / _JSONL_PATH
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


class TestSessionEndHappyPath:
    def test_exits_zero(self, tmp_path):
        payload = json.dumps({"session_id": "s1", "start_ts": "2026-03-20T10:00:00Z"})
        result = run_hook("session-end.py", payload, tmp_path)
        assert result.returncode == 0

    def test_creates_jsonl_file(self, tmp_path):
        payload = json.dumps({"session_id": "s1"})
        run_hook("session-end.py", payload, tmp_path)
        assert (tmp_path / _JSONL_PATH).exists()

    def test_record_contains_required_fields(self, tmp_path):
        payload = json.dumps({"session_id": "s1", "start_ts": "2026-03-20T10:00:00Z", "turn_count": 7})
        run_hook("session-end.py", payload, tmp_path)
        records = _read_records(tmp_path)
        r = records[0]
        assert r["session_id"] == "s1"
        assert r["turn_count"] == 7
        assert r["end_ts"] is not None
        assert r["duration_seconds"] is not None
        assert "trace_id" in r, "record must contain trace_id field"

    def test_record_trace_id_from_file(self, tmp_path):
        """When sessions/.current_trace_id exists, its value is used as the record's trace_id."""
        trace_id = "11111111-2222-4333-a444-555555555555"
        trace_file = tmp_path / _TRACE_ID_PATH
        trace_file.parent.mkdir(parents=True, exist_ok=True)
        trace_file.write_text(trace_id)
        payload = json.dumps({"session_id": "s1"})
        run_hook("session-end.py", payload, tmp_path)
        records = _read_records(tmp_path)
        assert records[0]["trace_id"] == trace_id

    def test_record_trace_id_fallback_when_no_file(self, tmp_path):
        """Without sessions/.current_trace_id the hook must not crash; trace_id starts 'unknown-'."""
        payload = json.dumps({"session_id": "s-no-trace"})
        run_hook("session-end.py", payload, tmp_path)
        records = _read_records(tmp_path)
        assert records[0]["trace_id"].startswith("unknown-")

    def test_end_ts_is_valid_iso_format(self, tmp_path):
        payload = json.dumps({"session_id": "s2"})
        run_hook("session-end.py", payload, tmp_path)
        records = _read_records(tmp_path)
        datetime.fromisoformat(records[0]["end_ts"])  # Raises ValueError on bad format.

    def test_appends_multiple_records(self, tmp_path):
        for i in range(3):
            payload = json.dumps({"session_id": f"s{i}", "start_ts": "2026-03-20T10:00:00Z"})
            run_hook("session-end.py", payload, tmp_path)
        records = _read_records(tmp_path)
        assert len(records) == 3

    def test_each_appended_record_is_valid_json(self, tmp_path):
        for i in range(3):
            run_hook("session-end.py", json.dumps({"session_id": f"s{i}"}), tmp_path)
        # If any line is invalid JSON, json.loads will raise — that's the assertion.
        _read_records(tmp_path)

    def test_duration_calculated_from_start_ts(self, tmp_path):
        payload = json.dumps({"session_id": "s3", "start_ts": "2026-03-20T10:00:00Z"})
        run_hook("session-end.py", payload, tmp_path)
        records = _read_records(tmp_path)
        # Duration should be non-negative (hook ran after start_ts).
        assert records[0]["duration_seconds"] >= 0


class TestSessionEndEdgeCases:
    def test_null_duration_when_no_start_ts(self, tmp_path):
        payload = json.dumps({"session_id": "s4"})
        run_hook("session-end.py", payload, tmp_path)
        records = _read_records(tmp_path)
        assert records[0]["duration_seconds"] is None

    def test_duration_from_persisted_start_ts_when_missing_in_payload(self, tmp_path):
        """session-end.py must compute duration from sessions/.current_start_ts when
        the SessionEnd payload does not contain start_ts (the normal VS Code case)."""
        start_ts_file = tmp_path / Path("sessions") / ".current_start_ts"
        start_ts_file.parent.mkdir(parents=True, exist_ok=True)
        start_ts_file.write_text("2026-03-20T10:00:00Z", encoding="utf-8")
        # Payload has no start_ts — simulates VS Code SessionEnd event
        payload = json.dumps({"session_id": "s-fallback"})
        run_hook("session-end.py", payload, tmp_path)
        records = _read_records(tmp_path)
        assert records[0]["duration_seconds"] is not None
        assert records[0]["duration_seconds"] >= 0

    def test_always_exits_zero_on_bad_json(self, tmp_path):
        result = run_hook("session-end.py", "{{bad json", tmp_path)
        assert result.returncode == 0

    def test_always_exits_zero_on_empty_stdin(self, tmp_path):
        result = run_hook("session-end.py", "", tmp_path)
        assert result.returncode == 0

    def test_accepts_sessionid_camelcase(self, tmp_path):
        """Must accept both ``sessionId`` and ``session_id``."""
        payload = json.dumps({"sessionId": "camel-s1"})
        run_hook("session-end.py", payload, tmp_path)
        records = _read_records(tmp_path)
        assert records[0]["session_id"] == "camel-s1"
