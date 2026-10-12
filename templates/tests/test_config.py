import pytest

from example_app.config import ConfigError, Settings


def test_defaults() -> None:
    assert Settings.from_env({}) == Settings(
        host="127.0.0.1", port=8000, log_level="INFO"
    )


def test_reads_environment() -> None:
    env = {"HOST": "0.0.0.0", "PORT": "9000", "LOG_LEVEL": "debug"}  # noqa: S104
    assert Settings.from_env(env) == Settings(
        host="0.0.0.0",  # noqa: S104
        port=9000,
        log_level="DEBUG",
    )


@pytest.mark.parametrize("port", ["eighty", "0", "65536"])
def test_rejects_bad_port(port: str) -> None:
    with pytest.raises(ConfigError, match="PORT"):
        Settings.from_env({"PORT": port})


def test_rejects_bad_log_level() -> None:
    with pytest.raises(ConfigError, match="LOG_LEVEL"):
        Settings.from_env({"LOG_LEVEL": "loud"})
