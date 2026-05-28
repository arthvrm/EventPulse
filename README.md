# ⚡ EventPulse

> Reliable webhook processing, normalization, and integration monitoring platform.

EventPulse is a backend system designed to receive, verify, normalize, process, and analyze webhook events from external services (including payment providers).
It focuses on reliability, observability, and integration stability, and includes a built-in mock provider for testing webhook flows.

---

## 🚀 Features

* 🔐 HMAC SHA256 signature verification
* ♻ Idempotent event processing
* 🔄 Retry mechanism with exponential backoff
* 🗄 Database persistence (async SQLAlchemy + migrations via Alembic)
* 📊 Analytics and reporting-ready architecture
* 📜 Structured logging
* 🛠 Admin API for manual event control
* 🧪 Testing support with pytest
* 🐳 Dockerized setup
* 🧪 Mock provider for generating webhook events
* 🔀 Event normalization across provider formats

---

## 🏗 Architecture Overview

EventPulse consists of two main components:

### Backend (`app.backend`)

* FastAPI-based async webhook receiver
* Event validation and normalization layer
* Persistence layer (async SQLAlchemy)
* Retry & processing pipeline
* Admin API
* Analytics-ready data model

### Mock Provider (`app.mock_provider`)

* Simulates external payment/webhook providers
* Generates reproducible webhook payloads
* Sends signed webhook requests (HMAC)
* Useful for local development and testing

### Supporting Infrastructure

* PostgreSQL / async database
* Alembic migrations system
* Environment-based configuration (.env)

---

## 📡 How It Works

1. External service (or mock provider) sends a webhook event
2. EventPulse verifies HMAC signature
3. Payload is normalized into a unified event schema
4. Event ID is checked for idempotency
5. Event is stored in the database
6. Processing pipeline handles business logic
7. Metrics and logs are updated
8. Failed events are retried with exponential backoff

---

## 📊 Analytics Capabilities (Planned / In Progress)

* Total events per day
* Success / failure rates
* Retry statistics
* Average processing time
* Provider-level performance breakdown
* Database-driven reporting layer

---

## 🛠 Tech Stack

* Python 3.11+
* FastAPI (async)
* Async SQLAlchemy
* Alembic (migrations)
* Pydantic
* pytest
* Docker
* Structured logging

---

## 🔒 Security

* HMAC SHA256 verification
* Replay attack protection (idempotency keys)
* Payload validation
* Secret-based webhook signing (`WEBHOOK_SECRET`)

---

## ⚙️ Configuration

All sensitive configuration is stored in `.env`.

### Required variables:

* `DATABASE_URL` — async database connection string
* `WEBHOOK_SECRET` — shared secret for webhook signing/verification
* `ALEMBIC_DATABASE_URL` — database URL used by migrations

A sample configuration file is available as `.env.example`.

---

## 🚀 Getting Started

Run all commands from the project root.

### Option 1: Docker (recommended)

```bash
docker-compose up --build
```

API documentation will be available at:

```
http://localhost:8000/docs
```

---

### Option 2: Local Development

#### Run Backend

```powershell
uv run uvicorn app.backend.main:app --host 0.0.0.0 --port 8000 --reload
```

#### Run Mock Provider

```powershell
uv run -m app.mock_provider.main
```

---

## 🗄 Database Migrations

Alembic is used for schema migrations.

```powershell
alembic revision --autogenerate -m "create initial schema"
alembic upgrade head
```

Alembic reads the database URL from:

* `ALEMBIC_DATABASE_URL` in `.env` (preferred)
* fallback: `alembic.ini`

---

## 🧪 Testing

* Tests are located in the `tests/` directory
* Coverage is partial but expanding
* Run tests with:

```bash
pytest
```

---

## 📁 Project Structure

* `app/backend` — API layer, database models, repositories, middleware, event normalization, processing pipeline
* `app/mock_provider` — mock webhook generators and sender services
* `tests` — backend and mock provider tests
* `alembic` — database migrations and version control

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

* Message queue integration (RabbitMQ / Redis)
* Prometheus metrics exporter
* Web dashboard UI
* AI-powered error summarization
* Horizontal scaling and worker separation
* Advanced analytics and reporting layer

---

## 👤 Author

Arthur Mykhailyshyn
Backend Developer (Python / FastAPI)
