#!/usr/bin/env python3
# notification.py — forward agent notifications to an external webhook.
#
# Usage:
#   echo '<json>' | python .github/hooks/notification.py
#
# Requirements: Python 3.8+; stdlib only. Set COPILOT_WEBHOOK_URL in the
#   environment to enable forwarding; if absent the hook exits 0 silently.
# Assumes CWD == repository root (set automatically by VS Code hook runner).

import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


_TIMEOUT_SECONDS = 2


def _log_error(message: str) -> None:
    """Append an error line to sessions/metrics/webhook-errors.log (best-effort)."""
    log_dir = Path("sessions") / "metrics"
    try:
        log_dir.mkdir(parents=True, exist_ok=True)
        with (log_dir / "webhook-errors.log").open("a", encoding="utf-8") as fh:
            ts = datetime.now(timezone.utc).isoformat()
            fh.write(f"[{ts}] {message}\n")
    except OSError:
        pass  # Log write failure is non-fatal.


def main() -> None:
    webhook_url = os.environ.get("COPILOT_WEBHOOK_URL", "").strip()
    if not webhook_url:
        # Opt-in not configured — exit silently.
        sys.exit(0)

    try:
        raw = sys.stdin.read()
        payload = json.loads(raw)
    except (json.JSONDecodeError, ValueError) as exc:
        _log_error(f"failed to parse stdin JSON: {exc}")
        sys.exit(0)

    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        webhook_url,
        data=body,
        method="POST",
        headers={"Content-Type": "application/json"},
    )

    try:
        with urllib.request.urlopen(req, timeout=_TIMEOUT_SECONDS) as resp:
            status = resp.status
            if status < 200 or status >= 300:
                _log_error(f"webhook returned HTTP {status} for URL {webhook_url}")
    except urllib.error.HTTPError as exc:
        _log_error(f"webhook HTTP error {exc.code} for URL {webhook_url}")
    except urllib.error.URLError as exc:
        _log_error(f"webhook connection error for URL {webhook_url}: {exc.reason}")
    except OSError as exc:
        _log_error(f"webhook request failed: {exc}")

    # Notification forwarding is best-effort — never block the session.
    sys.exit(0)


if __name__ == "__main__":
    main()
