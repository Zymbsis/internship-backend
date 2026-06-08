# Internship Backend

Backend API built with FastAPI.

## Requirements

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) - package and project manager
- [Docker](https://docs.docker.com/) - required for deployment; optional for local development

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

| Variable       | Description                                | Default |
| -------------- | ------------------------------------------ | ------- |
| `PORT`         | Host port when running with Docker Compose | `8000`  |
| `CORS_ORIGINS` | Allowed browser origins (JSON array)       | `[]`    |

## Running the Application

The app runs on [Uvicorn](https://www.uvicorn.org/) (ASGI server). The FastAPI CLI wraps it for
local and production use.

### Development

Auto-reload on file changes:

```bash
uv run fastapi dev
```

### Production

```bash
uv run fastapi run
```

### Docker

Build the image once (or after changing `Dockerfile`, `pyproject.toml`, or `uv.lock`):

```bash
docker compose build
```

Production-like run (uses `fastapi run` from the Dockerfile):

```bash
docker compose up
```

Local development in a container with auto-reload (code changes are picked up via volume mount, no
rebuild needed):

```bash
docker compose --profile dev up
```

The container listens on port `8000` internally. The host port is taken from `PORT` in `.env`
(defaults to `8000`).

To build and run the image without Compose:

```bash
docker build -t internship-backend .
docker run --rm -p 8000:8000 --env-file .env internship-backend
```

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
├── main.py              # Application entry point
├── config.py            # Settings and environment configuration
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
- [pytest](https://docs.pytest.org/) - testing
- [ruff](https://docs.astral.sh/ruff/) - linting and formatting
- [mypy](https://mypy-lang.org/) - static type checking
- [pre-commit](https://pre-commit.com/) - Git hooks
- [Docker](https://docs.docker.com/) - containerized deployment
