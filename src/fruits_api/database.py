"""Database engine, session management, and initialization."""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from .config import get_settings
from .models import Base


def _make_engine(database_url: str) -> Engine:
    """Create an Engine, ensuring a local SQLite directory exists.

    ``check_same_thread`` is disabled because FastAPI may use a session from a
    different thread than the one that created the connection.
    """
    connect_args: dict[str, object] = {}
    if database_url.startswith("sqlite"):
        connect_args["check_same_thread"] = False
        # Ensure the parent directory for a file-based SQLite DB exists.
        prefix = "sqlite:///"
        if database_url.startswith(prefix):
            db_path = Path(database_url[len(prefix) :])
            if db_path.parent and str(db_path.parent) not in ("", "."):
                db_path.parent.mkdir(parents=True, exist_ok=True)
    return create_engine(database_url, connect_args=connect_args)


engine: Engine = _make_engine(get_settings().database_url)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


def init_db() -> None:
    """Create database tables if they do not already exist."""
    Base.metadata.create_all(bind=engine)


def get_session() -> Iterator[Session]:
    """FastAPI dependency that yields a database session per request."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
