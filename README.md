# ⚡ EventPulse

> Reliable webhook ingestion, normalization, and payment event processing platform.

EventPulse is an asynchronous backend system built with FastAPI for receiving, validating, normalizing, and tracking webhook events from external providers such as Stripe and PayPal.

The platform focuses on reliability, security, observability, and integration stability while providing a unified event model for downstream processing and analytics.

To simplify local development and integration testing, EventPulse includes a built-in mock provider capable of generating and signing realistic webhook events.

---

## ✨ Features

* 🔐 HMAC SHA256 webhook signature verification
* ♻️ Idempotent event processing
* 🔄 Provider-independent event normalization
* ⚡ Fully asynchronous architecture
* 🗄 PostgreSQL persistence with SQLAlchemy Async
* 📊 Analytics-ready data model
* 📜 Structured logging with request tracing
* 🧪 Unit and integration testing
* 🚀 Built-in webhook simulator
* 🐳 Dockerized development environment

---

## 🏗 Architecture

            ┌──────────────────────┐
            │ Provider             │
            │ (Stripe / PayPal)    │
            └─────────┬────────────┘
                      │
                      ▼
            ┌──────────────────────┐
            │ FastAPI Webhook API  │
            └─────────┬────────────┘
                      │
                      ▼
            ┌──────────────────────┐
            │ Signature Verification│
            └─────────┬────────────┘
                      │
                      ▼
            ┌──────────────────────┐
            │ Provider Detection   │
            └─────────┬────────────┘
                      │
                      ▼
            ┌──────────────────────┐
            │ Idempotency          │
            └─────────┬────────────┘
                      │
                      ▼
            ┌──────────────────────┐
            │ Event Normalization  │
            └─────────┬────────────┘
                      │
                      ▼
            ┌──────────────────────┐
            │ Persistence          │
            └─────────┬────────────┘
                      │
                      ▼
            ┌──────────────────────┐
            │ Analytics Pipeline   │
            └──────────────────────┘

### Components

#### Backend (`app.backend`)

Responsible for:

* Receiving webhook requests
* Verifying signatures
* Validating payloads
* Detecting providers
* Normalizing events
* Persisting data
* Tracking payment states
* Producing structured logs

#### Mock Provider (`app.mock_provider`)

Provides:

* Interactive CLI
* PayPal and Stripe event generation
* HMAC request signing
* End-to-end webhook testing
* Invalid event simulation for error scenarios

---

## 🔄 Event Processing Flow

1. Provider sends a signed webhook request.
2. EventPulse verifies the HMAC SHA256 signature.
3. The payload is parsed and validated.
4. Provider type is detected.
5. Event idempotency is checked.
6. Data is normalized into a unified schema.
7. Raw and processed events are stored.
8. Payment state is updated.
9. Logs and metrics are recorded.
10. A response is returned to the sender.

---

## 📌 Supported Providers

| Provider | Status      |
| -------- | ----------- |
| Stripe   | ✅ Supported |
| PayPal   | ✅ Supported |
| Wise     | 🚧 Planned  |
| Square   | 🚧 Planned  |

---

## 🛠 Tech Stack

| Category         | Technology             |
| ---------------- | ---------------------- |
| Language         | Python 3.12            |
| API              | FastAPI                |
| ORM              | SQLAlchemy 2.0 Async   |
| Database         | PostgreSQL             |
| Database Driver  | asyncpg                |
| Validation       | Pydantic               |
| Migrations       | Alembic                |
| HTTP Client      | httpx                  |
| Testing          | pytest, pytest-asyncio |
| Containerization | Docker, Docker Compose |

---

## 🚀 Quick Start

### Requirements

* Python 3.12+
* PostgreSQL
* uv package manager

### Installation

```bash
git clone <repository-url>
cd eventpulse

uv sync
```

Create environment configuration:

```bash
copy .env.example .env
```

Configure:

```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost/eventpulse
WEBHOOK_SECRET=your-secret-key
```

Apply migrations:

```bash
alembic upgrade head
```

Start the backend:

```bash
python -m app.backend.main --local
```

Swagger documentation:

```text
http://localhost:8000/docs
```

Start the mock provider in a separate terminal:

```bash
python -m app.mock_provider.main
```

---

## 🐳 Running with Docker

Start the entire stack:

```bash
docker-compose up --build
```

This will:

* Start PostgreSQL
* Apply Alembic migrations
* Launch the FastAPI application
* Expose the API on `http://localhost:8000`

---

## ⚙️ Configuration

### Required Environment Variables

| Variable         | Description                                      |
| ---------------- | ------------------------------------------------ |
| `DATABASE_URL`   | PostgreSQL connection string                     |
| `WEBHOOK_SECRET` | Secret used for webhook signing and verification |

Example:

```env
DATABASE_URL=postgresql+asyncpg://eventpulse_admin:password@localhost:5432/eventpulse
WEBHOOK_SECRET=your-super-secret-key
```

---

## 🔒 Security

EventPulse implements several reliability and security mechanisms:

### Webhook Authentication

Incoming requests are protected using HMAC SHA256 signatures.

```text
signature = HMAC_SHA256(secret_key, payload)
```

Requests with invalid signatures are rejected with:

```http
401 Unauthorized
```

### Idempotent Processing

Duplicate webhook deliveries are prevented through:

* Event-level idempotency checks
* Database uniqueness constraints
* Provider event identifiers

### Payload Validation

All incoming data is validated using Pydantic models before entering the processing pipeline.

### Additional Safeguards

* Timing-safe signature comparison
* Structured error handling
* SQL injection protection through SQLAlchemy ORM
* Decimal-based monetary calculations
* Timezone-aware timestamps

---

## 📊 Data Model

The platform stores three categories of information:

### Raw Events

Original webhook payloads are preserved for:

* Auditing
* Debugging
* Event replay
* Incident investigation

### Processed Events

Provider-specific events are transformed into a unified schema suitable for:

* Analytics
* Reporting
* Monitoring
* Business workflows

### Payment State

A denormalized payment view maintains the latest known state of each payment for fast access.

---

## 🧪 Testing

Run all tests:

```bash
pytest
```

Verbose output:

```bash
pytest -v
```

Run a specific file:

```bash
pytest tests/test_api.py
```

Run matching tests:

```bash
pytest -k webhook
```

Current test coverage includes:

* Webhook API behavior
* HMAC verification
* Event normalization
* Error handling
* Provider detection

---

## 🎯 Engineering Highlights

This project demonstrates several production-oriented backend engineering practices.

### Reliable Webhook Processing

Duplicate webhook deliveries are handled through event idempotency checks and database-level uniqueness constraints.

### Provider Abstraction

The normalization layer uses the Strategy pattern, allowing new providers to be integrated with minimal changes to the processing pipeline.

### Security First

Webhook requests are protected using HMAC SHA256 verification and timing-safe signature comparison.

### Full Async Stack

The entire platform is asynchronous, using:

* FastAPI
* SQLAlchemy Async
* asyncpg
* httpx

This enables efficient handling of high-concurrency webhook workloads.

### Observability

Structured logging and request tracing provide visibility across the entire processing pipeline.

### Testability

Repository abstraction, dependency injection, and isolated normalization logic make the system easy to test and maintain.

---

## 📁 Project Structure

```text
app/
├── backend/
│   ├── api/
│   ├── db/
│   ├── normalizers/
│   ├── schemas/
│   ├── services/
│   └── etc/
│
├── mock_provider/
│   ├── event_generators/
│   ├── providers/
│   ├── services/
│   └── factory/
│
tests/
alembic/
```

---

## 🚧 Roadmap

* Retry mechanism with exponential backoff
* Event replay functionality
* RabbitMQ / Redis integration
* Prometheus metrics exporter
* Analytics API
* Administrative dashboard
* Additional provider integrations
* Horizontal scaling support
* Custom transformation rules

---

## 👨‍💻 Author

**Arthur Mykhailyshyn**

Python Backend Developer

---

### Key Concepts Demonstrated

* Event-Driven Architecture
* Async Backend Development
* Webhook Processing
* Payment Integrations
* Security Best Practices
* Database Design
* Design Patterns
* Observability
* Dockerized Infrastructure
