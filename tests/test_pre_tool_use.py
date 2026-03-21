"""Regression tests for .github/hooks/pre-tool-use.py — security gate."""

import json
from pathlib import Path

import pytest

from helpers import run_hook

_PATTERNS_PATH = Path(".github") / "security-patterns.json"


def _write_patterns(tmp_path: Path, patterns: dict) -> None:
    gh = tmp_path / ".github"
    gh.mkdir(exist_ok=True)
    (gh / "security-patterns.json").write_text(json.dumps(patterns))


class TestPreToolUseAllowPaths:
    def test_no_patterns_file_allows_all(self, tmp_path):
        payload = json.dumps(
            {"tool_name": "delete_file", "tool_input": {"path": ".github/copilot-instructions.md"}}
        )
        result = run_hook("pre-tool-use.py", payload, tmp_path)
        assert result.returncode == 0

    def test_non_file_non_terminal_tool_allowed(self, tmp_path):
        payload = json.dumps({"tool_name": "semantic_search", "tool_input": {"query": "hello"}})
        result = run_hook("pre-tool-use.py", payload, tmp_path)
        assert result.returncode == 0

    def test_non_matching_file_allowed(self, tmp_path):
        _write_patterns(tmp_path, {"protected_files": [".github/copilot-instructions.md"], "dangerous_terminal": []})
        payload = json.dumps(
            {"tool_name": "write_file", "tool_input": {"path": "src/main.py"}}
        )
        result = run_hook("pre-tool-use.py", payload, tmp_path)
        assert result.returncode == 0

    def test_non_matching_command_allowed(self, tmp_path):
        _write_patterns(tmp_path, {"protected_files": [], "dangerous_terminal": ["rm -rf"]})
        payload = json.dumps({"tool_name": "bash", "tool_input": {"command": "echo hello"}})
        result = run_hook("pre-tool-use.py", payload, tmp_path)
        assert result.returncode == 0

    def test_malformed_json_fails_open(self, tmp_path):
        """Unparseable stdin must allow the tool call to proceed (fail open)."""
        result = run_hook("pre-tool-use.py", "{{broken", tmp_path)
        assert result.returncode == 0


class TestPreToolUseBlockPaths:
    def test_protected_file_blocked(self, tmp_path):
        _write_patterns(
            tmp_path,
            {"protected_files": [".github/copilot-instructions.md"], "dangerous_terminal": []},
        )
        payload = json.dumps(
            {"tool_name": "delete_file", "tool_input": {"path": ".github/copilot-instructions.md"}}
        )
        result = run_hook("pre-tool-use.py", payload, tmp_path)
        assert result.returncode == 2
        assert "BLOCKED" in result.stderr

    def test_protected_directory_prefix_blocked(self, tmp_path):
        _write_patterns(tmp_path, {"protected_files": [".github/"], "dangerous_terminal": []})
        payload = json.dumps(
            {"tool_name": "write_file", "tool_input": {"filePath": ".github/hooks/stop.py"}}
        )
        result = run_hook("pre-tool-use.py", payload, tmp_path)
        assert result.returncode == 2

    def test_dangerous_terminal_command_blocked(self, tmp_path):
        _write_patterns(tmp_path, {"protected_files": [], "dangerous_terminal": ["rm -rf"]})
        payload = json.dumps({"tool_name": "bash", "tool_input": {"command": "rm -rf /important"}})
        result = run_hook("pre-tool-use.py", payload, tmp_path)
        assert result.returncode == 2

    def test_block_message_has_three_field_schema(self, tmp_path):
        """Stderr must contain all three escalation fields: BLOCKED, REASON, NEXT."""
        _write_patterns(tmp_path, {"protected_files": [".github/copilot-instructions.md"], "dangerous_terminal": []})
        payload = json.dumps(
            {"tool_name": "delete_file", "tool_input": {"path": ".github/copilot-instructions.md"}}
        )
        result = run_hook("pre-tool-use.py", payload, tmp_path)
        assert "BLOCKED" in result.stderr
        assert "REASON" in result.stderr
        assert "NEXT" in result.stderr

    def test_block_message_uses_pattern_specific_reason_and_next(self, tmp_path):
        """When the pattern entry has reason/next fields, they appear verbatim in stderr."""
        patterns = {
            "protected_files": [
                {
                    "pattern": ".github/copilot-instructions.md",
                    "reason": "Custom reason text.",
                    "next": "Custom next-step text.",
                }
            ],
            "dangerous_terminal": [],
        }
        _write_patterns(tmp_path, patterns)
        payload = json.dumps(
            {"tool_name": "delete_file", "tool_input": {"path": ".github/copilot-instructions.md"}}
        )
        result = run_hook("pre-tool-use.py", payload, tmp_path)
        assert result.returncode == 2
        assert "Custom reason text." in result.stderr
        assert "Custom next-step text." in result.stderr

    def test_terminal_block_message_has_three_field_schema(self, tmp_path):
        """Terminal command soft-blocks must also emit the 3-field schema."""
        _write_patterns(tmp_path, {"protected_files": [], "dangerous_terminal": ["rm -rf"]})
        payload = json.dumps({"tool_name": "bash", "tool_input": {"command": "rm -rf /important"}})
        result = run_hook("pre-tool-use.py", payload, tmp_path)
        assert result.returncode == 2
        assert "BLOCKED" in result.stderr
        assert "REASON" in result.stderr
        assert "NEXT" in result.stderr

    def test_case_insensitive_path_match(self, tmp_path):
        """Path matching should be case-insensitive."""
        _write_patterns(
            tmp_path,
            {"protected_files": [".github/Copilot-Instructions.md"], "dangerous_terminal": []},
        )
        payload = json.dumps(
            {"tool_name": "delete_file", "tool_input": {"path": ".github/copilot-instructions.md"}}
        )
        result = run_hook("pre-tool-use.py", payload, tmp_path)
        assert result.returncode == 2

    def test_powershell_tool_name_recognised(self, tmp_path):
        _write_patterns(tmp_path, {"protected_files": [], "dangerous_terminal": ["format c:"]})
        payload = json.dumps({"tool_name": "powershell", "tool_input": {"command": "format c: /quick"}})
        result = run_hook("pre-tool-use.py", payload, tmp_path)
        assert result.returncode == 2
