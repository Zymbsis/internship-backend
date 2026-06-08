# Internship Backend

Backend API built with FastAPI.

## Requirements

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) - package and project manager

## Getting Started

### 1. Install dependencies

Clone the repository and install all dependencies (including dev tools):

```bash
uv sync --group dev
```

### 2. Environment variables

Copy the sample environment file. No variables are required for the initial setup, but this keeps
the workflow ready for future configuration:

```bash
cp .env.sample .env
```

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
