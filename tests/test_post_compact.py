"""Regression tests for .github/hooks/post-compact.py — rule re-injection."""

import json
from pathlib import Path

import pytest

from helpers import run_hook

_INSTRUCTIONS = Path(".github") / "copilot-instructions.md"
_MARKER = "# PRIORITY: HIGH"
_TRACE_ID_PATH = Path("sessions") / ".current_trace_id"


def _write_instructions(tmp_path: Path, lines: list[str]) -> None:
    gh = tmp_path / ".github"
    gh.mkdir(exist_ok=True)
    (gh / "copilot-instructions.md").write_text("\n".join(lines))


class TestPostCompactOutput:
    def test_exits_zero_always(self, tmp_path):
        result = run_hook("post-compact.py", "{}", tmp_path)
        assert result.returncode == 0

    def test_outputs_valid_json(self, tmp_path):
        result = run_hook("post-compact.py", "{}", tmp_path)
        data = json.loads(result.stdout)
        assert "additionalContext" in data

    def test_bad_stdin_still_exits_zero(self, tmp_path):
        result = run_hook("post-compact.py", "not json at all", tmp_path)
        assert result.returncode == 0

    def test_empty_stdin_still_exits_zero(self, tmp_path):
        result = run_hook("post-compact.py", "", tmp_path)
        assert result.returncode == 0

    def test_context_contains_trace_id(self, tmp_path):
        """additionalContext must include a trace_id line for session correlation."""
        result = run_hook("post-compact.py", "{}", tmp_path)
        ctx = json.loads(result.stdout)["additionalContext"]
        assert "trace_id:" in ctx

    def test_context_trace_id_from_file(self, tmp_path):
        """When sessions/.current_trace_id exists, its value must appear in additionalContext."""
        trace_id = "fedcba98-7654-4321-abcd-ef0123456789"
        trace_file = tmp_path / _TRACE_ID_PATH
        trace_file.parent.mkdir(parents=True, exist_ok=True)
        trace_file.write_text(trace_id)
        result = run_hook("post-compact.py", "{}", tmp_path)
        ctx = json.loads(result.stdout)["additionalContext"]
        assert trace_id in ctx

    def test_context_trace_id_fallback_when_no_file(self, tmp_path):
        """Without sessions/.current_trace_id the hook must not crash; trace_id starts 'unknown-'."""
        result = run_hook("post-compact.py", "{}", tmp_path)
        ctx = json.loads(result.stdout)["additionalContext"]
        for line in ctx.splitlines():
            if line.startswith("trace_id:"):
                assert line.split(":", 1)[1].strip().startswith("unknown-")
                return
        pytest.fail("trace_id line not found in additionalContext")


class TestPostCompactFallback:
    def test_fallback_when_no_instructions_file(self, tmp_path):
        result = run_hook("post-compact.py", "{}", tmp_path)
        data = json.loads(result.stdout)
        # Fallback must point developer to the instructions file.
        assert "copilot-instructions.md" in data["additionalContext"]

    def test_fallback_when_no_priority_lines(self, tmp_path):
        _write_instructions(tmp_path, ["Normal rule one.", "Normal rule two."])
        result = run_hook("post-compact.py", "{}", tmp_path)
        data = json.loads(result.stdout)
        assert "copilot-instructions.md" in data["additionalContext"]


class TestPostCompactPriorityInjection:
    def test_injects_priority_line(self, tmp_path):
        _write_instructions(tmp_path, ["Important rule.  # PRIORITY: HIGH", "Other rule."])
        result = run_hook("post-compact.py", "{}", tmp_path)
        data = json.loads(result.stdout)
        assert "Important rule" in data["additionalContext"]

    def test_non_priority_lines_not_injected(self, tmp_path):
        _write_instructions(
            tmp_path,
            ["Keep this hidden.", "Inject me.  # PRIORITY: HIGH"],
        )
        result = run_hook("post-compact.py", "{}", tmp_path)
        data = json.loads(result.stdout)
        assert "Keep this hidden" not in data["additionalContext"]

    def test_max_five_priority_lines_injected(self, tmp_path):
        lines = [f"Rule {i}.  # PRIORITY: HIGH" for i in range(10)]
        _write_instructions(tmp_path, lines)
        result = run_hook("post-compact.py", "{}", tmp_path)
        data = json.loads(result.stdout)
        bullet_count = data["additionalContext"].count("- Rule")
        assert bullet_count <= 5

    def test_context_within_char_budget(self, tmp_path):
        """additionalContext must not exceed 800 chars (≈ 200 tokens)."""
        lines = [f"Rule {i}.  # PRIORITY: HIGH" for i in range(5)]
        _write_instructions(tmp_path, lines)
        result = run_hook("post-compact.py", "{}", tmp_path)
        data = json.loads(result.stdout)
        assert len(data["additionalContext"]) <= 800
