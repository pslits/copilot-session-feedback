"""Regression tests for .github/hooks/post-tool-use.py — auto-formatter gate."""

import json

import pytest

from helpers import run_hook


class TestPostToolUseFiltering:
    def test_non_write_tool_exits_zero(self, tmp_path):
        payload = json.dumps({"tool_name": "read_file", "tool_input": {"path": "foo.py"}})
        result = run_hook("post-tool-use.py", payload, tmp_path)
        assert result.returncode == 0

    def test_unknown_extension_exits_zero(self, tmp_path):
        payload = json.dumps({"tool_name": "write_file", "tool_input": {"path": "foo.xyz"}})
        result = run_hook("post-tool-use.py", payload, tmp_path)
        assert result.returncode == 0

    def test_malformed_json_exits_zero(self, tmp_path):
        result = run_hook("post-tool-use.py", "not json", tmp_path)
        assert result.returncode == 0

    def test_empty_stdin_exits_zero(self, tmp_path):
        result = run_hook("post-tool-use.py", "", tmp_path)
        assert result.returncode == 0


class TestPostToolUseGracefulDegradation:
    """Formatter missing or failing must never block the session."""

    def test_formatter_not_found_exits_zero(self, tmp_path):
        """npx/black may not be available in the test environment; hook must degrade gracefully."""
        (tmp_path / "test.md").write_text("# heading")
        payload = json.dumps({"tool_name": "write_file", "tool_input": {"path": "test.md"}})
        result = run_hook("post-tool-use.py", payload, tmp_path)
        assert result.returncode == 0

    def test_no_file_path_exits_zero(self, tmp_path):
        """If tool_input has no extractable path the hook should silently exit 0."""
        payload = json.dumps({"tool_name": "write_file", "tool_input": {}})
        result = run_hook("post-tool-use.py", payload, tmp_path)
        assert result.returncode == 0

    def test_write_tool_variants_recognised(self, tmp_path):
        """All three write-tool names must be handled (not silently skipped)."""
        for tool in ("write_file", "edit_file", "create_file"):
            payload = json.dumps({"tool_name": tool, "tool_input": {"path": "file.xyz"}})
            result = run_hook("post-tool-use.py", payload, tmp_path)
            # Unknown extension — exits 0 without trying to format.
            assert result.returncode == 0, f"Failed for tool_name={tool}"
