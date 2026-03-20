"""Regression tests for .github/hooks/notification.py — external webhook forwarding."""

import json
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

import pytest

from helpers import run_hook

_ERROR_LOG = Path("sessions") / "metrics" / "webhook-errors.log"


# ── Minimal in-process HTTP server for success-path tests ────────────────────

class _CapturingHandler(BaseHTTPRequestHandler):
    """Records the raw request body of each POST received."""

    received_bodies: list[bytes] = []
    received_status_to_return: int = 200

    def do_POST(self) -> None:
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)
        self.__class__.received_bodies.append(body)
        self.send_response(self.__class__.received_status_to_return)
        self.end_headers()

    def log_message(self, *args) -> None:  # noqa: D401
        pass  # Suppress test-noise output.


def _start_server(status: int = 200) -> tuple[HTTPServer, str]:
    """Start a single-request capture server; return (server, url)."""
    _CapturingHandler.received_bodies = []
    _CapturingHandler.received_status_to_return = status
    server = HTTPServer(("127.0.0.1", 0), _CapturingHandler)
    port = server.server_address[1]
    thread = threading.Thread(target=server.handle_request, daemon=True)
    thread.start()
    return server, f"http://127.0.0.1:{port}"


class TestNotificationNoUrl:
    def test_exits_zero_silently_when_no_url(self, tmp_path):
        result = run_hook(
            "notification.py",
            json.dumps({"type": "info", "message": "hello"}),
            tmp_path,
            env_overrides={"COPILOT_WEBHOOK_URL": ""},
        )
        assert result.returncode == 0

    def test_no_stdout_when_no_url(self, tmp_path):
        result = run_hook(
            "notification.py",
            "{}",
            tmp_path,
            env_overrides={"COPILOT_WEBHOOK_URL": ""},
        )
        assert result.stdout == ""

    def test_no_stderr_when_no_url(self, tmp_path):
        result = run_hook(
            "notification.py",
            "{}",
            tmp_path,
            env_overrides={"COPILOT_WEBHOOK_URL": ""},
        )
        assert result.stderr == ""


class TestNotificationWebhookSuccess:
    def test_exits_zero_on_200(self, tmp_path):
        server, url = _start_server(200)
        try:
            result = run_hook(
                "notification.py",
                json.dumps({"type": "info", "message": "hi"}),
                tmp_path,
                env_overrides={"COPILOT_WEBHOOK_URL": url},
            )
        finally:
            server.server_close()
        assert result.returncode == 0

    def test_forwards_full_payload(self, tmp_path):
        server, url = _start_server(200)
        try:
            run_hook(
                "notification.py",
                json.dumps({"type": "alert", "message": "shipped"}),
                tmp_path,
                env_overrides={"COPILOT_WEBHOOK_URL": url},
            )
        finally:
            server.server_close()
        assert len(_CapturingHandler.received_bodies) == 1
        sent = json.loads(_CapturingHandler.received_bodies[0])
        assert sent["message"] == "shipped"
        assert sent["type"] == "alert"


class TestNotificationWebhookFailure:
    def test_exits_zero_on_non_2xx_response(self, tmp_path):
        server, url = _start_server(500)
        try:
            result = run_hook(
                "notification.py",
                "{}",
                tmp_path,
                env_overrides={"COPILOT_WEBHOOK_URL": url},
            )
        finally:
            server.server_close()
        assert result.returncode == 0

    def test_logs_non_2xx_to_error_file(self, tmp_path):
        server, url = _start_server(500)
        try:
            run_hook(
                "notification.py",
                "{}",
                tmp_path,
                env_overrides={"COPILOT_WEBHOOK_URL": url},
            )
        finally:
            server.server_close()
        log = tmp_path / _ERROR_LOG
        assert log.exists()
        assert "500" in log.read_text()

    def test_exits_zero_on_connection_refused(self, tmp_path):
        """Port with no listener — must log and exit 0, not raise."""
        result = run_hook(
            "notification.py",
            "{}",
            tmp_path,
            env_overrides={"COPILOT_WEBHOOK_URL": "http://127.0.0.1:19998/no-server"},
        )
        assert result.returncode == 0

    def test_logs_connection_error_to_file(self, tmp_path):
        run_hook(
            "notification.py",
            "{}",
            tmp_path,
            env_overrides={"COPILOT_WEBHOOK_URL": "http://127.0.0.1:19998/no-server"},
        )
        log = tmp_path / _ERROR_LOG
        assert log.exists()

    def test_malformed_json_stdin_exits_zero(self, tmp_path):
        """Even with a valid URL, bad stdin must degrade gracefully."""
        result = run_hook(
            "notification.py",
            "{{not json}}",
            tmp_path,
            env_overrides={"COPILOT_WEBHOOK_URL": "http://127.0.0.1:19998/no-server"},
        )
        assert result.returncode == 0
