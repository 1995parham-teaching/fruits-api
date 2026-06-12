"""FastAPI application exposing the Fruits API."""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from . import __version__
from .database import get_session, init_db
from .models import Fruit
from .schemas import FruitCreate, FruitRead


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize the database schema on startup."""
    init_db()
    yield


app = FastAPI(
    title="Fruits API",
    version=__version__,
    summary="A simple service to store and retrieve fruits.",
    description=(
        "A minimal CRUD API for fruits. Interactive documentation is available "
        "at `/docs` (Swagger UI) and `/redoc`."
    ),
    lifespan=lifespan,
)

SessionDep = Annotated[Session, Depends(get_session)]


@app.get("/health", tags=["meta"], summary="Liveness/readiness probe")
def health() -> dict[str, str]:
    """Return a simple health status, used by Kubernetes probes."""
    return {"status": "ok"}


@app.get("/fruits", response_model=list[FruitRead], tags=["fruits"], summary="List all fruits")
def list_fruits(session: SessionDep) -> list[Fruit]:
    """Return every fruit stored in the database."""
    return list(session.scalars(select(Fruit).order_by(Fruit.id)).all())


@app.get(
    "/fruits/{fruit_id}",
    response_model=FruitRead,
    tags=["fruits"],
    summary="Get a specific fruit",
    responses={404: {"description": "Fruit not found"}},
)
def get_fruit(fruit_id: int, session: SessionDep) -> Fruit:
    """Return a single fruit by its ID, or 404 if it does not exist."""
    fruit = session.get(Fruit, fruit_id)
    if fruit is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Fruit with id {fruit_id} not found",
        )
    return fruit


@app.post(
    "/fruits",
    response_model=FruitRead,
    status_code=status.HTTP_201_CREATED,
    tags=["fruits"],
    summary="Add a new fruit",
)
def create_fruit(payload: FruitCreate, session: SessionDep) -> Fruit:
    """Create a new fruit from a JSON payload and return the stored record."""
    fruit = Fruit(fruit=payload.fruit, color=payload.color)
    session.add(fruit)
    session.commit()
    session.refresh(fruit)
    return fruit
