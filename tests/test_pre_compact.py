"""Regression tests for .github/hooks/pre-compact.py — context snapshot export."""

import json
import time
from pathlib import Path

import pytest

from helpers import run_hook

_PRECOMPACT_DIR = Path("sessions") / "precompact"


class TestPreCompactHappyPath:
    def test_exits_zero(self, tmp_path):
        payload = json.dumps({"session_id": "sess-1", "messages": [{"role": "user"}]})
        result = run_hook("pre-compact.py", payload, tmp_path)
        assert result.returncode == 0

    def test_creates_timestamped_snapshot(self, tmp_path):
        payload = json.dumps({"session_id": "sess-1"})
        run_hook("pre-compact.py", payload, tmp_path)
        snapshots = list((tmp_path / _PRECOMPACT_DIR).glob("sess-1-*.json"))
        assert len(snapshots) == 1

    def test_snapshot_contains_session_id(self, tmp_path):
        payload = json.dumps({"session_id": "sess-2"})
        run_hook("pre-compact.py", payload, tmp_path)
        snapshots = list((tmp_path / _PRECOMPACT_DIR).glob("sess-2-*.json"))
        data = json.loads(snapshots[0].read_text())
        assert data["session_id"] == "sess-2"

    def test_snapshot_contains_captured_at(self, tmp_path):
        payload = json.dumps({"session_id": "sess-3"})
        run_hook("pre-compact.py", payload, tmp_path)
        snapshots = list((tmp_path / _PRECOMPACT_DIR).glob("sess-3-*.json"))
        data = json.loads(snapshots[0].read_text())
        assert "captured_at" in data

    def test_snapshot_payload_preserved(self, tmp_path):
        payload = json.dumps({"session_id": "sess-4", "messages": [{"role": "user", "content": "hi"}]})
        run_hook("pre-compact.py", payload, tmp_path)
        snapshots = list((tmp_path / _PRECOMPACT_DIR).glob("sess-4-*.json"))
        data = json.loads(snapshots[0].read_text())
        assert data["payload"]["messages"][0]["content"] == "hi"


class TestPreCompactEdgeCases:
    def test_empty_stdin_creates_fallback_snapshot(self, tmp_path):
        result = run_hook("pre-compact.py", "", tmp_path)
        assert result.returncode == 0
        snapshots = list((tmp_path / _PRECOMPACT_DIR).glob("*.json"))
        assert len(snapshots) == 1

    def test_malformed_json_still_creates_snapshot(self, tmp_path):
        result = run_hook("pre-compact.py", "{bad json!!}", tmp_path)
        assert result.returncode == 0
        snapshots = list((tmp_path / _PRECOMPACT_DIR).glob("*.json"))
        assert len(snapshots) == 1

    def test_multiple_runs_produce_separate_files(self, tmp_path):
        """Idempotency: each invocation creates a new file, not an overwrite."""
        payload = json.dumps({"session_id": "sess-5"})
        run_hook("pre-compact.py", payload, tmp_path)
        time.sleep(1.1)  # Timestamps in filenames are second-granular.
        run_hook("pre-compact.py", payload, tmp_path)
        snapshots = list((tmp_path / _PRECOMPACT_DIR).glob("sess-5-*.json"))
        assert len(snapshots) == 2
