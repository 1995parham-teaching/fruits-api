# CLAUDE.md

Guidance for working in this repository.

## Project

**Fruits API** — a small, containerized CRUD service for fruits. Three fruit endpoints
(list / get / add) plus a `/health` probe, with data persisted to SQLite.

## Stack

- **Python 3.14** (pinned via `.python-version`), managed by **uv**.
- **FastAPI + Uvicorn** — the web framework; OpenAPI/Swagger docs are served at `/docs`.
- **SQLAlchemy 2.0 + SQLite** — persistence. The database URL is read from the
  `DATABASE_URL` env var (defaults to `sqlite:///./data/fruits.db`).
- **pytest** for tests, **ruff** for lint + format.

## Common commands

```bash
uv sync                  # install deps (creates .venv, manages Python 3.14)
uv run fruits-api        # run the API on http://localhost:8000
uv run pytest            # run the test suite
uv run ruff check .      # lint
uv run ruff format .     # auto-format

docker build -t fruits-api .            # build the image
kubectl apply -k k8s/                   # deploy to Kubernetes
```

## Layout

```
src/fruits_api/
  main.py       FastAPI app + route handlers (the only place HTTP lives)
  models.py     SQLAlchemy ORM model (Fruit)
  schemas.py    Pydantic request/response schemas (FruitCreate, FruitRead)
  database.py   engine, SessionLocal, init_db(), get_session() dependency
  config.py     env-based Settings (DATABASE_URL)
  __main__.py   uvicorn entrypoint (`python -m fruits_api` / `fruits-api`)
tests/          pytest suite; conftest.py provides an in-memory DB client fixture
k8s/            Deployment, Service, PVC, Kustomization
.github/workflows/ci.yml   lint+test, then build & publish image to GHCR
```

## Conventions

- **Keep HTTP in `main.py`.** Models, schemas, and DB session wiring stay in their own
  modules; routes depend on `get_session` via FastAPI's `Depends`.
- **Schemas vs. models:** never return ORM objects directly — map through a `FruitRead`
  schema (`response_model=...`). Request bodies are validated by `FruitCreate`.
- **Persistence is swappable.** Read storage config only through `config.Settings` /
  `DATABASE_URL`; don't hardcode paths. Pointing at PostgreSQL should be a config change.
- **Tests must stay hermetic.** They use an in-memory SQLite DB via the `client` fixture and
  must not touch the filesystem or require a running server.

## Before committing

Run `uv run ruff check . && uv run ruff format --check . && uv run pytest` — CI enforces all
three. The CI workflow also builds the Docker image and publishes it to
`ghcr.io/<owner>/<repo>` on pushes to `main`.
