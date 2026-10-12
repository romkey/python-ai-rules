"""Command line: `example-app` or `python -m example_app`."""

import argparse
import contextlib
import logging
import signal
import sys
import threading
from collections.abc import Sequence
from types import FrameType

from example_app import __version__
from example_app.config import ConfigError, Settings
from example_app.server import make_server

logger = logging.getLogger("example_app")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="example-app", description=__doc__)
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )
    parser.parse_args(argv)

    try:
        settings = Settings.from_env()
    except ConfigError as e:
        parser.exit(2, f"example-app: {e}\n")

    logging.basicConfig(
        level=settings.log_level,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    server = make_server(settings.host, settings.port)

    # `docker stop` sends SIGTERM. Shut down cleanly instead of being killed;
    # shutdown() blocks until serve_forever() returns, so call it elsewhere.
    def stop(signum: int, frame: FrameType | None) -> None:
        logger.info("received signal %d, shutting down", signum)
        threading.Thread(target=server.shutdown).start()

    signal.signal(signal.SIGTERM, stop)

    logger.info(
        "example-app %s listening on %s:%d",
        __version__,
        settings.host,
        server.server_port,
    )
    with server, contextlib.suppress(KeyboardInterrupt):
        server.serve_forever()
    logger.info("stopped")
    return 0


if __name__ == "__main__":
    sys.exit(main())
