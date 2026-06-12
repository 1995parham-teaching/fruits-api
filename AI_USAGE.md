# AI Usage

The assignment explicitly encourages the use of AI tools and asks that their use be documented.
This file describes where and how AI was used in this project.

## Tooling

- **Claude Code** (Anthropic) was used as a pair-programming assistant to scaffold the project,
  write boilerplate, and draft documentation.

## Where AI was used

- **Project scaffolding** — generating the initial directory layout, `pyproject.toml`, and the
  FastAPI application skeleton (routes, models, schemas, session management).
- **Tests** — drafting the `pytest` suite, including the in-memory-database fixture used to keep
  tests hermetic.
- **Dockerfile** — writing the multi-stage, non-root, `uv`-based build.
- **Kubernetes manifests** — Deployment, Service, PVC, and Kustomization, plus the rationale for
  running a single replica with SQLite.
- **CI/CD** — the GitHub Actions workflow that lints, tests, builds, and publishes to GHCR.
- **Documentation** — this file and the README.

## Human decisions & oversight

The following choices were made/confirmed by me, with AI assisting the implementation:

- **Stack: FastAPI + SQLAlchemy + SQLite.** FastAPI gives free OpenAPI/Swagger documentation
  (directly satisfying the "API documentation" requirement); SQLite satisfies "persistent data"
  with no extra infrastructure while remaining swappable via `DATABASE_URL`.
- **Python 3.14** — the latest stable release (3.15 was still in alpha), managed by `uv`.
- **Persistence in Kubernetes** via a `PersistentVolumeClaim`, with the trade-off (single writer,
  single replica) called out explicitly rather than hidden.

All generated code was reviewed, run, and tested locally (`ruff` + `pytest` pass) before commit.
