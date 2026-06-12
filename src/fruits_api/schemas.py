"""Pydantic schemas for request and response payloads."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class FruitCreate(BaseModel):
    """Payload for creating a fruit."""

    fruit: str = Field(..., min_length=1, examples=["apple"])
    color: str = Field(..., min_length=1, examples=["red"])


class FruitRead(BaseModel):
    """Representation of a fruit returned by the API."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    fruit: str
    color: str
