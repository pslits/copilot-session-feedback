"""Shared test helpers for hook regression tests."""

import os
import subprocess
import sys
from pathlib import Path

# Absolute path to the hooks directory — used by all test modules.
HOOKS_DIR = Path(__file__).parent.parent / ".github" / "hooks"


def run_hook(
    script: str,
    stdin: str,
    cwd: Path,
    env_overrides: dict[str, str] | None = None,
) -> subprocess.CompletedProcess:
    """Run a hook Python script as a subprocess.

    Args:
        script:        Filename of the script inside HOOKS_DIR (e.g. ``"stop.py"``).
        stdin:         String piped to the script's stdin.
        cwd:           Working directory for the process (use ``tmp_path``).
        env_overrides: Optional dict of env-var overrides; merged on top of
                       ``os.environ`` so the process inherits the full parent env.

    Returns:
        The completed subprocess result.
    """
    env = os.environ.copy()
    if env_overrides:
        env.update(env_overrides)
    return subprocess.run(
        [sys.executable, str(HOOKS_DIR / script)],
        input=stdin,
        capture_output=True,
        text=True,
        cwd=str(cwd),
        env=env,
    )
