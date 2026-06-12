"""SQLAlchemy ORM models."""

from __future__ import annotations

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Declarative base for all ORM models."""


class Fruit(Base):
    """A fruit record persisted in the database."""

    __tablename__ = "fruits"

    id: Mapped[int] = mapped_column(primary_key=True)
    fruit: Mapped[str] = mapped_column(index=True)
    color: Mapped[str]
