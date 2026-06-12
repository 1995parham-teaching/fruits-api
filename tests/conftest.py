"""Pytest fixtures providing an isolated, in-memory API client."""

from __future__ import annotations

import os

# Ensure the app's module-level engine never touches the filesystem during tests.
os.environ.setdefault("DATABASE_URL", "sqlite://")

from collections.abc import Iterator  # noqa: E402

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402
from sqlalchemy import StaticPool, create_engine  # noqa: E402
from sqlalchemy.orm import sessionmaker  # noqa: E402

from fruits_api.database import get_session  # noqa: E402
from fruits_api.main import app  # noqa: E402
from fruits_api.models import Base  # noqa: E402


@pytest.fixture
def client() -> Iterator[TestClient]:
    """Yield a TestClient backed by a fresh in-memory SQLite database.

    A shared-cache in-memory engine (via ``StaticPool``) gives each test a
    clean, isolated database without touching the filesystem.
    """
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    testing_session = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)

    def override_get_session() -> Iterator:
        session = testing_session()
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_session] = override_get_session
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)
