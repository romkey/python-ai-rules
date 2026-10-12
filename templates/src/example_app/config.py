"""Settings, read once at startup from environment variables.

Every variable is documented in docs/configuration.md and listed, with a
safe example value, in .env.example.
"""

import logging
import os
from collections.abc import Mapping
from dataclasses import dataclass


class ConfigError(ValueError):
    """An environment variable is set to something unusable."""


@dataclass(frozen=True)
class Settings:
    host: str = "127.0.0.1"
    port: int = 8000
    log_level: str = "INFO"

    @classmethod
    def from_env(cls, env: Mapping[str, str] = os.environ) -> Settings:
        port_text = env.get("PORT", str(cls.port))
        try:
            port = int(port_text)
        except ValueError:
            raise ConfigError(f"PORT must be a number, not {port_text!r}") from None
        if not 0 < port < 65536:
            raise ConfigError(f"PORT must be 1-65535, not {port}")

        log_level = env.get("LOG_LEVEL", cls.log_level).upper()
        if log_level not in logging.getLevelNamesMapping():
            raise ConfigError(f"LOG_LEVEL {log_level!r} is not a logging level")

        return cls(host=env.get("HOST", cls.host), port=port, log_level=log_level)
