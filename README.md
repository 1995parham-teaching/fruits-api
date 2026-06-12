# Fruits API

A simple, containerized **Fruits API** built with [FastAPI](https://fastapi.tiangolo.com/),
SQLAlchemy, and SQLite. It exposes three endpoints to list, fetch, and add fruits, with data
persisted across requests.

This repository was produced as a take-home assignment.

---

## Features

- **FastAPI** application with automatic, interactive API documentation.
- **Persistent storage** via SQLite (a file on disk / a mounted volume in Kubernetes).
- **Tests** with `pytest` against an isolated in-memory database.
- **Linting & formatting** with `ruff`.
- **Containerized** with a small, multi-stage Docker image.
- **CI/CD** with GitHub Actions: run tests → build image → publish to GitHub Container Registry (GHCR).
- **Kubernetes manifests** for deploying the service with a persistent volume.

## Tech stack & design choices

| Concern            | Choice                     | Why                                                                 |
| ------------------ | -------------------------- | ------------------------------------------------------------------- |
| Language / runtime | Python 3.14                | Latest stable Python (3.15 is still in alpha at time of writing).   |
| Packaging          | [uv](https://docs.astral.sh/uv/) | Fast, reproducible dependency management and locking.         |
| Web framework      | FastAPI + Uvicorn          | Minimal boilerplate and **free OpenAPI/Swagger docs** at `/docs`.   |
| Persistence        | SQLAlchemy 2.0 + SQLite    | Zero external services; a single file satisfies "persistent data".  |
| Tests              | pytest + FastAPI TestClient| Fast, hermetic functional tests over the real ASGI app.             |

> **Why SQLite?** The assignment only requires that data persist across requests. SQLite gives
> us real persistence with no extra infrastructure. The database URL is configurable via the
> `DATABASE_URL` environment variable, so swapping in PostgreSQL later is a one-line change.

---

## Requirements

- [uv](https://docs.astral.sh/uv/getting-started/installation/) (manages Python 3.14 for you)
- Docker (optional, for containerized runs)

## Running locally

```bash
# Install dependencies into a virtual environment (uv manages Python 3.14)
uv sync

# Start the API (listens on http://localhost:8000)
uv run fruits-api
```

Then open the interactive docs at **http://localhost:8000/docs**.

By default the database is written to `./data/fruits.db`. Override with `DATABASE_URL`:

```bash
DATABASE_URL="sqlite:///./data/fruits.db" uv run fruits-api
```

## API usage

The service exposes three fruit endpoints plus a health check.

### List all fruits — `GET /fruits`

```bash
curl http://localhost:8000/fruits
```

```json
[
  { "id": 1, "fruit": "apple", "color": "red" }
]
```

### Get a specific fruit — `GET /fruits/{id}`

```bash
curl http://localhost:8000/fruits/1
```

```json
{ "id": 1, "fruit": "apple", "color": "red" }
```

Returns `404` if the fruit does not exist.

### Add a fruit — `POST /fruits`

```bash
curl -X POST http://localhost:8000/fruits \
  -H "Content-Type: application/json" \
  -d '{"fruit": "banana", "color": "yellow"}'
```

```json
{ "id": 2, "fruit": "banana", "color": "yellow" }
```

Returns `201 Created`. The `id` is assigned by the server; `fruit` and `color` are required
non-empty strings (a missing/invalid body yields `422`).

### Health — `GET /health`

```bash
curl http://localhost:8000/health
# {"status": "ok"}
```

---

## Testing & linting

```bash
uv run pytest          # run the test suite
uv run ruff check .    # lint
uv run ruff format .   # auto-format
```

---

## Docker

```bash
# Build
docker build -t fruits-api .

# Run (persist the SQLite DB to a host directory)
docker run --rm -p 8000:8000 \
  -e DATABASE_URL="sqlite:////data/fruits.db" \
  -v "$(pwd)/data:/data" \
  fruits-api
```

Prebuilt images are published by CI to GHCR:

```bash
docker pull ghcr.io/<owner>/<repo>:latest
```

---

## Kubernetes

Manifests live in [`k8s/`](./k8s) and include a `Deployment`, `Service`, and a
`PersistentVolumeClaim` so the SQLite database survives pod restarts.

```bash
# Update the image reference in k8s/deployment.yaml to your GHCR image, then:
kubectl apply -k k8s/

# Port-forward to try it out
kubectl port-forward svc/fruits-api 8000:80
```

See [`k8s/README.md`](./k8s/README.md) for details.

---

## CI/CD

[`.github/workflows/ci.yml`](.github/workflows/ci.yml) runs on every push and pull request:

1. **Test** — `ruff` lint + `pytest`.
2. **Build & publish** — on pushes to `main` (and tags), builds the Docker image and pushes it
   to `ghcr.io/<owner>/<repo>`. Uses the built-in `GITHUB_TOKEN`; no extra secrets required.

## Project layout

```
.
├── src/fruits_api/      # application package
│   ├── main.py          # FastAPI app & routes
│   ├── models.py        # SQLAlchemy ORM model
│   ├── schemas.py       # Pydantic request/response schemas
│   ├── database.py      # engine & session management
│   ├── config.py        # env-based settings
│   └── __main__.py      # `python -m fruits_api` / `fruits-api` entrypoint
├── tests/               # pytest suite
├── k8s/                 # Kubernetes manifests
├── Dockerfile
├── .github/workflows/ci.yml
└── pyproject.toml
```
