"""Regression tests for .github/hooks/session-start.py — orientation metadata injection."""

import json
from datetime import datetime
from pathlib import Path

import pytest

from helpers import UUID4_RE, run_hook

_TRACE_ID_PATH = Path("sessions") / ".current_trace_id"
_START_TS_PATH = Path("sessions") / ".current_start_ts"


class TestSessionStartOutput:
    def test_exits_zero_always(self, tmp_path):
        result = run_hook("session-start.py", "{}", tmp_path)
        assert result.returncode == 0

    def test_outputs_valid_json(self, tmp_path):
        result = run_hook("session-start.py", "{}", tmp_path)
        data = json.loads(result.stdout)
        assert "additionalContext" in data

    def test_context_contains_required_keys(self, tmp_path):
        result = run_hook("session-start.py", "{}", tmp_path)
        ctx = json.loads(result.stdout)["additionalContext"]
        for key in ("project:", "branch:", "commit:", "version:", "session_opened:", "trace_id:"):
            assert key in ctx, f"Missing key '{key}' in additionalContext"

    def test_context_within_token_budget(self, tmp_path):
        """additionalContext must stay well under 400 characters (≈ 100 tokens)."""
        result = run_hook("session-start.py", "{}", tmp_path)
        ctx = json.loads(result.stdout)["additionalContext"]
        assert len(ctx) <= 400

    def test_trace_id_is_uuid4(self, tmp_path):
        """trace_id value in additionalContext must be a valid UUID v4."""
        result = run_hook("session-start.py", "{}", tmp_path)
        ctx = json.loads(result.stdout)["additionalContext"]
        for line in ctx.splitlines():
            if line.startswith("trace_id: "):
                trace_id = line.split(": ", 1)[1].strip()
                assert UUID4_RE.match(trace_id), f"trace_id '{trace_id}' is not a UUID v4"
                return
        pytest.fail("trace_id line not found in additionalContext")

    def test_trace_id_file_created(self, tmp_path):
        """session-start.py must persist the trace ID to sessions/.current_trace_id."""
        run_hook("session-start.py", "{}", tmp_path)
        trace_id_file = tmp_path / _TRACE_ID_PATH
        assert trace_id_file.exists(), "sessions/.current_trace_id was not created"
        content = trace_id_file.read_text().strip()
        assert UUID4_RE.match(content), f"persisted trace ID '{content}' is not a UUID v4"

    def test_trace_id_matches_context(self, tmp_path):
        """The trace ID in additionalContext must equal the one persisted to disk."""
        result = run_hook("session-start.py", "{}", tmp_path)
        ctx = json.loads(result.stdout)["additionalContext"]
        ctx_trace_id = None
        for line in ctx.splitlines():
            if line.startswith("trace_id: "):
                ctx_trace_id = line.split(": ", 1)[1].strip()
        assert ctx_trace_id is not None
        file_trace_id = (tmp_path / _TRACE_ID_PATH).read_text().strip()
        assert ctx_trace_id == file_trace_id

    def test_start_ts_file_created(self, tmp_path):
        """session-start.py must persist the start timestamp to sessions/.current_start_ts."""
        run_hook("session-start.py", "{}", tmp_path)
        start_ts_file = tmp_path / _START_TS_PATH
        assert start_ts_file.exists(), "sessions/.current_start_ts was not created"

    def test_start_ts_is_valid_iso8601(self, tmp_path):
        """The persisted start timestamp must be a valid ISO 8601 string."""
        run_hook("session-start.py", "{}", tmp_path)
        content = (tmp_path / _START_TS_PATH).read_text().strip()
        # Should parse without error
        datetime.fromisoformat(content.replace("Z", "+00:00"))

    def test_start_ts_matches_context(self, tmp_path):
        """The session_opened value in additionalContext must equal the persisted start_ts."""
        result = run_hook("session-start.py", "{}", tmp_path)
        ctx = json.loads(result.stdout)["additionalContext"]
        ctx_ts = None
        for line in ctx.splitlines():
            if line.startswith("session_opened: "):
                ctx_ts = line.split(": ", 1)[1].strip()
        assert ctx_ts is not None
        file_ts = (tmp_path / _START_TS_PATH).read_text().strip()
        assert ctx_ts == file_ts


class TestSessionStartGracefulDegradation:
    def test_bad_stdin_exits_zero(self, tmp_path):
        result = run_hook("session-start.py", "{{broken", tmp_path)
        assert result.returncode == 0

    def test_empty_stdin_exits_zero(self, tmp_path):
        result = run_hook("session-start.py", "", tmp_path)
        assert result.returncode == 0

    def test_version_fallback_without_package_json(self, tmp_path):
        """No package.json in cwd — version field must be 'n/a', not an exception."""
        result = run_hook("session-start.py", "{}", tmp_path)
        assert result.returncode == 0
        ctx = json.loads(result.stdout)["additionalContext"]
        assert "version: n/a" in ctx

    def test_reads_package_json_version(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({"version": "4.5.6", "name": "test"}))
        result = run_hook("session-start.py", "{}", tmp_path)
        assert result.returncode == 0
        ctx = json.loads(result.stdout)["additionalContext"]
        assert "version: 4.5.6" in ctx

    def test_git_unavailable_falls_back_to_unknown(self, tmp_path):
        """Running from a non-git directory — branch and commit must be 'unknown', not an error."""
        result = run_hook("session-start.py", "{}", tmp_path)
        assert result.returncode == 0
        ctx = json.loads(result.stdout)["additionalContext"]
        # Either a real branch OR 'unknown' is acceptable — not an exception.
        assert "branch:" in ctx
        assert "commit:" in ctx
