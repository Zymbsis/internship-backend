# Internship Backend

Backend API built with FastAPI.

## Requirements

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) - package and project manager
- [Docker](https://docs.docker.com/) - required for deployment; recommended for running PostgreSQL
  and Redis locally
- PostgreSQL 17+ and Redis 7+ - required at application startup (can be run via Docker Compose)

## Getting Started

### 1. Install dependencies

Clone the repository and install all dependencies (including dev tools):

```bash
uv sync --group dev
```

### 2. Environment variables

Copy the sample environment file:

```bash
cp .env.sample .env
```

| Variable             | Description                                | Default     |
| -------------------- | ------------------------------------------ | ----------- |
| `ENVIRONMENT`        | Runtime mode (`dev` or `prod`)             | `dev`       |
| `PORT`               | Host port when running with Docker Compose | `8000`      |
| `CORS_ORIGINS`       | Allowed browser origins (JSON array)       | `[]`        |
| `POSTGRES__HOST`     | PostgreSQL host                            | `localhost` |
| `POSTGRES__PORT`     | PostgreSQL port                            | `5432`      |
| `POSTGRES__USER`     | PostgreSQL user                            | `postgres`  |
| `POSTGRES__PASSWORD` | PostgreSQL password                        | `password`  |
| `POSTGRES__DB`       | PostgreSQL database name                   | `postgres`  |
| `REDIS__HOST`        | Redis host                                 | `localhost` |
| `REDIS__PORT`        | Redis port                                 | `6379`      |

Nested settings use the `__` delimiter (for example, `POSTGRES__HOST` maps to `postgres.host` in
`app/config.py`).

Keep `POSTGRES__HOST=localhost` and `REDIS__HOST=localhost` in `.env` for running the API on the
host with `uv run`. Docker Compose overrides these to `postgres` and `redis` for the `api` and
`api-dev` services automatically.

## Running the Application

The app runs on [Uvicorn](https://www.uvicorn.org/) (ASGI server). The FastAPI CLI wraps it for
local and production use.

### Development

Start PostgreSQL and Redis (if not already running):

```bash
docker compose up postgres redis -d
```

Auto-reload on file changes:

```bash
uv run fastapi dev
```

### Production

Start PostgreSQL and Redis (if not already running):

```bash
docker compose up postgres redis -d
```

```bash
uv run fastapi run
```

### Docker

Compose runs PostgreSQL (`postgres:17-alpine`) and Redis (`redis:7-alpine`) alongside the API. Data
is persisted in named volumes (`postgres_data`, `redis_data`).

Rebuild the API image after changing `Dockerfile`, `pyproject.toml`, or `uv.lock`. The `api` and
`api-dev` services require a profile and share the same `Dockerfile`, so either command below is
enough; `postgres` and `redis` use pre-built images:

```bash
docker compose --profile prod build
docker compose --profile dev build
```

`docker compose --profile prod up` and `docker compose --profile dev up` also build the image
automatically when it is missing; use `build` only when you need to force a rebuild.

Start only the databases (useful when running the API locally with `uv run`):

```bash
docker compose up postgres redis -d
```

Production-like run (uses `fastapi run` from the Dockerfile):

```bash
docker compose --profile prod up
```

Local development in a container with auto-reload (code changes are picked up via volume mount, no
rebuild needed):

```bash
docker compose --profile dev up
```

Running `docker compose up` without a profile starts PostgreSQL and Redis only; the API services
require the `prod` or `dev` profile.

The container listens on port `8000` internally. The host port is taken from `PORT` in `.env`
(defaults to `8000`).

To build and run the image without the Compose `api` service, join the Compose network so the
container can reach the database services by name:

```bash
docker compose up postgres redis -d

docker build -t internship-backend .
docker run --rm -p 8000:8000 \
  --env-file .env \
  -e POSTGRES__HOST=postgres \
  -e REDIS__HOST=redis \
  --network internship-backend_default \
  internship-backend
```

`localhost` in `.env` does not work inside a standalone container — override the hosts as shown
above, or use `docker compose --profile prod up` instead.

The API will be available at:

| Resource   | URL                         |
| ---------- | --------------------------- |
| API base   | http://127.0.0.1:8000/api/  |
| Swagger UI | http://127.0.0.1:8000/docs  |
| ReDoc      | http://127.0.0.1:8000/redoc |

### Health Check

```bash
curl http://127.0.0.1:8000/api/
```

Expected response:

```json
{
  "status_code": 200,
  "detail": "ok",
  "result": "working"
}
```

## Project Structure

```
app/
├── main.py              # Application entry point and lifespan (DB connect/disconnect)
├── config.py            # Settings and environment configuration
├── db/                  # PostgreSQL and Redis connection setup and dependencies
├── routers/             # API route handlers
├── services/            # Business logic
├── repositories/        # Data access layer
├── schemas/             # Pydantic request/response models
├── exceptions/          # Custom exceptions and handlers
├── core/                # Shared core utilities
├── utils/               # Helper utilities
└── tests/               # Test suite
```

## Code Quality

### Pre-commit hooks

Install pre-commit hooks once after cloning:

```bash
uv run pre-commit install
```

On every `git commit`, the following checks run automatically:

- **ruff** - linting
- **mypy** - static type checking
- **pytest** - test suite

To run all hooks manually without committing:

```bash
uv run pre-commit run --all-files
```

### Running checks separately

If you need to run a specific check on its own:

```bash
uv run ruff check .
uv run mypy .
uv run pytest
```

## Tech Stack

- [FastAPI](https://fastapi.tiangolo.com/) - web framework
- [Uvicorn](https://www.uvicorn.org/) - ASGI server
- [Pydantic](https://docs.pydantic.dev/) - data validation
- [SQLAlchemy](https://www.sqlalchemy.org/) - async ORM (PostgreSQL)
- [asyncpg](https://github.com/MagicStack/asyncpg) - PostgreSQL async driver
- [Redis](https://redis.io/) - in-memory data store
- [pytest](https://docs.pytest.org/) - testing
- [ruff](https://docs.astral.sh/ruff/) - linting and formatting
- [mypy](https://mypy-lang.org/) - static type checking
- [pre-commit](https://pre-commit.com/) - Git hooks
- [Docker](https://docs.docker.com/) - containerized deployment
