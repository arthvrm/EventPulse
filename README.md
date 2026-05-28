# EventPulse

EventPulse is a lightweight Python project designed to receive, normalize, and persist webhook events from payment providers. It also includes a standalone mock provider for generating and delivering simulated webhook payloads.

## Overview

The project is organized into two main components:

- `app.backend` — the backend service with API endpoints, data persistence, and application logic.
- `app.mock_provider` — a mock event generator used to simulate webhook deliveries from payment platforms.

## Key Features

- Webhook intake and event processing
- Payment event normalization across provider formats
- Database-backed event persistence
- Mock provider for reproducible webhook testing
- Planned support for database analytics and reporting

## Getting Started

Run all commands from the project root.

### Run Backend

```powershell
uv run uvicorn app.backend.main:app --host 0.0.0.0 --port 8000 --reload
```

### Run Mock Provider

```powershell
uv run -m app.mock_provider.main
```

### Database Migrations

Alembic is configured for the async SQLAlchemy backend.

```powershell
alembic revision --autogenerate -m "create initial schema"
alembic upgrade head
```

Alembic reads the migration database URL from `ALEMBIC_DATABASE_URL` in `.env` if provided; otherwise, it falls back to the value stored in `alembic.ini`.

## Project Structure

- `app/backend` — backend API, database models, repository logic, dependency management, middleware, and event normalization.
- `app/mock_provider` — mock event providers, generators, and webhook sender services.
- `tests` — test modules covering selected backend and mock provider components.
- `alembic` — database migration configuration and versioning.

## Configuration

Sensitive configuration values are stored in `.env`. A sample file is available as `.env.example`.

Required variables:

- `DATABASE_URL` — async database connection string for the backend
- `WEBHOOK_SECRET` — shared HMAC secret for incoming webhook verification and mock provider signing
- `ALEMBIC_DATABASE_URL` — Alembic-only database URL for migrations

## Data Analysis Note

The project is prepared for future database analytics and reporting capabilities. This includes deriving insights from persisted events and extending the backend with query-driven data analysis.

## Testing

The project is not fully covered by tests yet. Existing tests validate key areas, but additional coverage is recommended before major changes.

## Notes

- The startup commands assume the `uv` tool is installed and available in your shell environment.
- Always execute the commands from the root of the project repository.
