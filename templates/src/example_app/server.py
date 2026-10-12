"""HTTP server. GET /healthz reports that the app is up, and its version."""

import json
import logging
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from example_app import __version__

logger = logging.getLogger(__name__)


class Handler(BaseHTTPRequestHandler):
    server_version = f"example-app/{__version__}"

    def do_GET(self) -> None:
        if self.path == "/healthz":
            self.send_json(HTTPStatus.OK, {"status": "ok", "version": __version__})
        else:
            self.send_json(HTTPStatus.NOT_FOUND, {"error": "not found"})

    def send_json(self, status: HTTPStatus, body: dict[str, str]) -> None:
        data = json.dumps(body).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, format: str, *args: object) -> None:
        # http.server writes to stderr; route it through logging instead.
        logger.info("%s %s", self.address_string(), format % args)


def make_server(host: str, port: int) -> ThreadingHTTPServer:
    """A server bound to host:port (port 0 picks a free one)."""
    return ThreadingHTTPServer((host, port), Handler)
