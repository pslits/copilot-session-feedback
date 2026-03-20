"""Regression tests for .github/hooks/session-start.py — orientation metadata injection."""

import json
from pathlib import Path

import pytest

from helpers import run_hook


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
        for key in ("project:", "branch:", "commit:", "version:", "session_opened:"):
            assert key in ctx, f"Missing key '{key}' in additionalContext"

    def test_context_within_token_budget(self, tmp_path):
        """additionalContext must stay well under 400 characters (≈ 100 tokens)."""
        result = run_hook("session-start.py", "{}", tmp_path)
        ctx = json.loads(result.stdout)["additionalContext"]
        assert len(ctx) <= 400


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
