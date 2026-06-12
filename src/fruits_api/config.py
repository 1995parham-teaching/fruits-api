"""Application configuration, sourced from environment variables."""

from __future__ import annotations

import os
from functools import lru_cache


class Settings:
    """Runtime settings.

    Values are read once from the environment. The database URL defaults to a
    local SQLite file so the service works out of the box, while production
    deployments (e.g. Kubernetes) can point ``DATABASE_URL`` at a mounted
    volume or an external database.
    """

    def __init__(self) -> None:
        self.database_url: str = os.environ.get("DATABASE_URL", "sqlite:///./data/fruits.db")


@lru_cache
def get_settings() -> Settings:
    """Return a cached Settings instance."""
    return Settings()
