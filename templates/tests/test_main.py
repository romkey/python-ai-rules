import signal
import threading
from collections.abc import Callable
from types import TracebackType
from typing import Any

import pytest

from example_app import __main__ as cli
from example_app import __version__


def test_version(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as exit_info:
        cli.main(["--version"])
    assert exit_info.value.code == 0
    assert capsys.readouterr().out == f"example-app {__version__}\n"


def test_bad_config_exits_2(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setenv("PORT", "eighty")
    with pytest.raises(SystemExit) as exit_info:
        cli.main([])
    assert exit_info.value.code == 2
    assert "PORT must be a number" in capsys.readouterr().err


class InlineThread:
    """Runs its target when started, so the test needn't wait for it."""

    def __init__(self, target: Callable[[], None]) -> None:
        self.target = target

    def start(self) -> None:
        self.target()


class FakeServer:
    """Stands in for the HTTP server: serves until 'interrupted'."""

    server_port = 1234

    def __init__(self) -> None:
        self.shut_down = False

    def __enter__(self) -> FakeServer:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        pass

    def serve_forever(self) -> None:
        raise KeyboardInterrupt

    def shutdown(self) -> None:
        self.shut_down = True


def test_serves_until_interrupted_and_handles_sigterm(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    server = FakeServer()
    handlers: dict[int, Callable[..., Any]] = {}
    monkeypatch.setattr(cli, "make_server", lambda host, port: server)
    monkeypatch.setattr(signal, "signal", handlers.__setitem__)
    monkeypatch.setattr(threading, "Thread", InlineThread)

    assert cli.main([]) == 0

    handlers[signal.SIGTERM](signal.SIGTERM, None)
    assert server.shut_down
