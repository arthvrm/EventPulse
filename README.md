# ⚡ EventPulse

> Reliable webhook processing, normalization, and integration monitoring platform.

EventPulse is a backend system designed to receive, verify, normalize, process, and analyze webhook events from external services (including payment providers).
It focuses on reliability, observability, and integration stability, and includes a built-in mock provider for testing webhook flows.

---

## 🚀 Features

* 🔐 HMAC SHA256 signature verification
* ♻ Idempotent event processing
* � Database persistence (async SQLAlchemy + Alembic migrations)
* 📊 Analytics-ready data model
* 📜 Structured logging
* 🧪 Testing support with pytest + asyncio
* 🧪 Mock provider for generating webhook events
* 🔀 Event normalization across provider formats (PayPal, Stripe)

---

## 🏗 Architecture Overview

EventPulse consists of two main components:

### Backend (`app.backend`)

* FastAPI-based async webhook receiver
* Webhook signature verification (HMAC SHA256)
* Payload parsing and validation
* Event normalization layer (PayPal, Stripe)
* Persistence layer (async SQLAlchemy)
* Processing pipeline with event tracking
* Structured logging with request context
* Database models supporting analytics data collection

### Mock Provider (`app.mock_provider`)

* Interactive CLI for selecting and testing webhook providers
* Generates realistic mock payloads for PayPal and Stripe
* Signs requests with HMAC SHA256 using the shared secret
* Sends signed webhook requests to the backend
* Useful for local development, integration testing, and validating webhook flows

### Supporting Infrastructure

* **PostgreSQL** with async driver (asyncpg)
* **Alembic** for database version control and migrations
* **Environment-based configuration** (.env)
* **Structured logging** with request context tracking

---

## 📡 How It Works

1. External service (or mock provider) sends a signed webhook request
2. EventPulse receives the request and extracts the payload
3. HMAC SHA256 signature is verified against the shared secret
4. Payload is parsed and validated
5. Provider type is detected (PayPal, Stripe, or unknown)
6. Event ID is checked for idempotency
7. Event is normalized into a unified schema and stored in the database
8. Processing pipeline extracts payment metadata and updates payment records
9. Metrics and logs are recorded for observability
10. Response is returned to the webhook sender

---

## 📊 Analytics Capabilities

Database models are designed to support:

* Total events per day / provider
* Success / failure rates and error patterns
* Processing latency metrics
* Provider-level performance breakdown
* Customer and order aggregation
* Fee and net amount analysis

_Full analytics and reporting endpoints are planned for future releases._

---

## 🛠 Tech Stack

* Python 3.12+
* FastAPI (async)
* Async SQLAlchemy + asyncpg
* Alembic (migrations)
* Pydantic
* pytest + pytest-asyncio
* httpx (async HTTP client)
* Structured logging

---

## 🔒 Security

* **HMAC SHA256 verification** — All incoming webhooks must be signed with the shared secret
* **Signature validation** — Requests without valid signatures are rejected with 401 Unauthorized
* **Idempotency** — Event IDs are checked to prevent duplicate processing
* **Payload validation** — Pydantic schemas validate all incoming data
* **Secret-based webhook signing** — Mock provider signs requests using `WEBHOOK_SECRET`

---

## ⚙️ Configuration

All sensitive configuration is stored in `.env`. A sample configuration file is available as `.env.example`.

### Required variables:

* `DATABASE_URL` — async PostgreSQL connection string (e.g., `postgresql+asyncpg://user:password@localhost/dbname`)
* `WEBHOOK_SECRET` — shared secret for webhook signing/verification and HMAC validation

### Optional variables:

* `ALEMBIC_DATABASE_URL` — database URL used by migrations (defaults to `DATABASE_URL` if not set)

---

## 🚀 Getting Started

Run all commands from the project root.

### Prerequisites

* Python 3.12+
* PostgreSQL database
* `uv` package manager (or pip with virtual environment)

### Local Development

0. **Venv**
```powershell
# Create .venv from pyproject.toml
uv sync
```

2. **Clone and setup environment:**
```powershell
# Create .env file with your configuration
cp .env.example .env
# Update DATABASE_URL and WEBHOOK_SECRET in .env
```

2. **Run database migrations:**
```powershell
alembic upgrade head
```

3. **Run Backend:**
```powershell
uv run uvicorn app.backend.main:app --host 0.0.0.0 --port 8000 --reload
```
FastAPI documentation will be available at: `http://localhost:8000/docs`

4. **Run Mock Provider (in another terminal):**
```powershell
uv run -m app.mock_provider.main
```
This starts an interactive CLI to generate and send test webhook events.

---

## 🗄 Database Migrations

Alembic is used for schema version control and migrations.

### Apply existing migrations:

```powershell
alembic upgrade head
```

### Create a new migration after model changes:

```powershell
alembic revision --autogenerate -m "your migration description"
alembic upgrade head
```

### Configuration:

Alembic reads the database URL from:
* `DATABASE_URL` or `ALEMBIC_DATABASE_URL` in `.env` (environment variables have priority)
* fallback: `alembic.ini`

---

## 🧪 Testing

* Tests are located in the `tests/` directory
* Framework: pytest + pytest-asyncio for async testing
* Test coverage includes API, normalization, repository, and security modules

### Run tests:

```bash
pytest                                # Run all tests
pytest -v                            # Verbose output
pytest tests/test_api.py            # Run specific test file
pytest -k test_webhook              # Run tests matching a pattern
```

---

## 📁 Project Structure

* `app/backend/api` — FastAPI routes (webhook receiver)
* `app/backend/db` — SQLAlchemy models, database setup, and repository layer
* `app/backend/normalizers` — Event normalization adapters (PayPal, Stripe)
* `app/backend/schemas` — Pydantic models for validation (raw events, processed events)
* `app/backend/services` — Business logic and processing pipeline
* `app/backend/etc` — Configuration, logging, middleware, security utilities, dependencies
* `app/mock_provider` — Interactive webhook provider simulator
  * `event_generators` — Mock event payload generators
  * `providers` — Provider implementations (PayPal, Stripe, broken)
  * `services` — HMAC signing and webhook sending services
  * `factory` — Factory for creating provider instances
* `tests` — Unit and integration tests
* `alembic` — Database migrations and version control

---

## 🎯 Project Goals

EventPulse was built to explore and implement:

* Event-driven architecture
* Reliable webhook ingestion
* Integration resilience patterns
* Observability and monitoring design
* Data normalization across external providers
* Backend reliability engineering

---

## 📌 Future Improvements

* Retry mechanism with exponential backoff for failed events
* Message queue integration (RabbitMQ / Redis)
* Admin API for manual event management and reprocessing
* Prometheus metrics exporter
* Analytics dashboard and reporting endpoints
* Web dashboard UI
* Support for additional payment providers
* Horizontal scaling and worker separation
* Webhook event replay functionality
* Custom transformation rules engine

---

## 👤 Author

Arthur Mykhailyshyn
Backend Developer (Python / FastAPI)
