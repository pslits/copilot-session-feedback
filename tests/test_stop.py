"""Regression tests for .github/hooks/stop.py — session transcript archival."""

import json
from datetime import datetime
from pathlib import Path

import pytest

from helpers import run_hook


class TestStopHookLoopGuard:
    """The stop_hook_active guard must prevent all side effects."""

    def test_exits_zero_on_loop_guard(self, tmp_path):
        payload = json.dumps(
            {"stop_hook_active": True, "session_id": "s1", "transcript_path": "/nonexistent"}
        )
        result = run_hook("stop.py", payload, tmp_path)
        assert result.returncode == 0

    def test_no_files_written_on_loop_guard(self, tmp_path):
        payload = json.dumps(
            {"stop_hook_active": True, "session_id": "s1", "transcript_path": "/nonexistent"}
        )
        run_hook("stop.py", payload, tmp_path)
        assert not (tmp_path / "sessions").exists()


class TestStopHookHappyPath:
    """Valid payload: transcript is archived and metadata written."""

    def _payload(self, tmp_path: Path, session_id: str = "abc123") -> str:
        transcript = tmp_path / "transcript.json"
        transcript.write_text('{"messages": []}')
        return json.dumps(
            {
                "session_id": session_id,
                "transcript_path": str(transcript),
                "stop_hook_active": False,
            }
        )

    def test_exits_zero(self, tmp_path):
        result = run_hook("stop.py", self._payload(tmp_path), tmp_path)
        assert result.returncode == 0

    def test_creates_transcript_file(self, tmp_path):
        run_hook("stop.py", self._payload(tmp_path), tmp_path)
        date_str = datetime.now().strftime("%Y-%m-%d")
        dest = tmp_path / "sessions" / date_str / "abc123" / "transcript.json"
        assert dest.exists()

    def test_creates_metadata_file(self, tmp_path):
        run_hook("stop.py", self._payload(tmp_path), tmp_path)
        date_str = datetime.now().strftime("%Y-%m-%d")
        meta_path = tmp_path / "sessions" / date_str / "abc123" / "metadata.json"
        assert meta_path.exists()
        meta = json.loads(meta_path.read_text())
        assert meta["session_id"] == "abc123"
        assert "timestamp" in meta
        assert meta["size_bytes"] > 0

    def test_accepts_sessionid_camelcase(self, tmp_path):
        """Hook must accept both ``sessionId`` (VS Code) and ``session_id``."""
        transcript = tmp_path / "t.json"
        transcript.write_text("{}")
        payload = json.dumps(
            {
                "sessionId": "camel-id",
                "transcript_path": str(transcript),
                "stop_hook_active": False,
            }
        )
        result = run_hook("stop.py", payload, tmp_path)
        assert result.returncode == 0
        date_str = datetime.now().strftime("%Y-%m-%d")
        assert (tmp_path / "sessions" / date_str / "camel-id" / "transcript.json").exists()


class TestStopHookErrorPaths:
    """Malformed or incomplete input must exit 2 (soft block) or be handled gracefully."""

    def test_missing_session_id_exits_2(self, tmp_path):
        transcript = tmp_path / "t.json"
        transcript.write_text("{}")
        payload = json.dumps({"transcript_path": str(transcript), "stop_hook_active": False})
        result = run_hook("stop.py", payload, tmp_path)
        assert result.returncode == 2
        assert "session_id" in result.stderr

    def test_missing_transcript_path_exits_2(self, tmp_path):
        payload = json.dumps({"session_id": "s1", "stop_hook_active": False})
        result = run_hook("stop.py", payload, tmp_path)
        assert result.returncode == 2

    def test_nonexistent_transcript_exits_2(self, tmp_path):
        payload = json.dumps(
            {
                "session_id": "s1",
                "transcript_path": str(tmp_path / "missing.json"),
                "stop_hook_active": False,
            }
        )
        result = run_hook("stop.py", payload, tmp_path)
        assert result.returncode == 2

    def test_malformed_json_exits_2(self, tmp_path):
        result = run_hook("stop.py", "{not json}", tmp_path)
        assert result.returncode == 2
