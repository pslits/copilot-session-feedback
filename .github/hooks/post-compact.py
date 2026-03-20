#!/usr/bin/env python3
# post-compact.py — re-inject critical rules into context after compression

import json
import sys
from pathlib import Path

INSTRUCTIONS_PATH = Path(".github/copilot-instructions.md")
PRIORITY_MARKER = "# PRIORITY: HIGH"
MAX_CHARS = 800  # Conservative ceiling ≈ 200 tokens
MAX_RULES = 5
FALLBACK_MESSAGE = (
    "IMPORTANT: Your context was just compressed. "
    "Review .github/copilot-instructions.md before proceeding — "
    "it contains the project's essential coding rules and conventions."
)


def extract_priority_lines(path: Path) -> list[str]:
    """Return up to MAX_RULES lines from path that contain PRIORITY_MARKER."""
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return []

    priority_lines = [line.rstrip() for line in lines if PRIORITY_MARKER in line]
    return priority_lines[:MAX_RULES]


def build_context(priority_lines: list[str]) -> str:
    """Build the additionalContext string, truncated to MAX_CHARS."""
    if not priority_lines:
        return FALLBACK_MESSAGE

    header = "Critical project rules (re-injected after compaction):"
    body = "\n".join(f"- {line.replace(PRIORITY_MARKER, '').strip()}" for line in priority_lines)
    full = f"{header}\n{body}"

    # Truncate to MAX_CHARS if needed (rare, but safety-net)
    if len(full) > MAX_CHARS:
        full = full[:MAX_CHARS].rsplit("\n", 1)[0] + "\n[truncated — see copilot-instructions.md]"

    return full


def main() -> None:
    # Read stdin — PostCompact payload; we don't assert specific fields
    try:
        raw = sys.stdin.read()
        _ = json.loads(raw) if raw.strip() else {}
    except Exception:
        pass  # Graceful degradation — stdin format doesn't affect injection

    priority_lines = extract_priority_lines(INSTRUCTIONS_PATH)
    additional_context = build_context(priority_lines)

    output = {"additionalContext": additional_context}
    print(json.dumps(output))
    sys.exit(0)  # Always exit 0 — a failed PostCompact degrades quality but must not block


if __name__ == "__main__":
    main()
