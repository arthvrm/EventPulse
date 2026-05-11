import pytest
from datetime import datetime, timezone
from fastapi.testclient import TestClient
from fastapi import FastAPI
from app.backend.main import app
from app.backend.schemas.raw_event import RawEvent
from app.backend.schemas.processed_event import ProcessedEvent


@pytest.fixture
def sample_paypal_payload():
    return {
        "id": "WH-1234567890",
        "event_type": "PAYMENT.CAPTURE.COMPLETED",
        "resource_type": "capture",
        "create_time": "2026-05-10T10:00:00.000Z",
        "resource": {
            "id": "capture-123",
            "status": "COMPLETED",
            "amount": {"currency_code": "USD", "value": "100.00"},
            "create_time": "2026-05-10T09:59:00.000Z",
            "update_time": "2026-05-10T10:00:00.000Z",
            "custom_id": "order-123",
            "invoice_id": "inv-123",
            "payer": {"email_address": "test@example.com", "payer_id": "PAYER-123"},
            "seller_receivable_breakdown": {
                "gross_amount": {"currency_code": "USD", "value": "100.00"},
                "paypal_fee": {"currency_code": "USD", "value": "3.00"},
                "net_amount": {"currency_code": "USD", "value": "97.00"}
            }
        }
    }


@pytest.fixture
def sample_stripe_payload():
    return {
        "id": "evt_1234567890",
        "object": "event",
        "type": "payment_intent.succeeded",
        "created": 1715337600,  # 2026-05-10T10:00:00Z
        "data": {
            "object": {
                "id": "pi_1234567890",
                "object": "payment_intent",
                "status": "succeeded",
                "amount": 10000,  # $100.00 in cents
                "currency": "usd",
                "created": 1715337540,  # 2026-05-10T09:59:00Z
                "metadata": {"order_id": "order-123"},
                "charges": {
                    "data": [{
                        "id": "ch_1234567890",
                        "object": "charge",
                        "amount": 10000,
                        "currency": "usd",
                        "status": "succeeded",
                        "paid": True,
                        "refunded": False,
                        "receipt_email": "test@example.com",
                        "created": 1715337540
                    }]
                },
                "application_fee_amount": 300  # $3.00 in cents
            }
        }
    }


@pytest.fixture
def sample_raw_event_paypal(sample_paypal_payload):
    return RawEvent(
        internal_event_id="req-123",
        provider="paypal",
        external_event_id="WH-1234567890",
        event_type="PAYMENT.CAPTURE.COMPLETED",
        raw_body=b'{"test": "data"}',
        headers={"x-signature": "test-sig"},
        signature="test-sig",
        signature_verified=True,
        request_id="req-123",
        payload=sample_paypal_payload,
        received_at=datetime.now(timezone.utc)
    )


@pytest.fixture
def sample_raw_event_stripe(sample_stripe_payload):
    return RawEvent(
        internal_event_id="req-456",
        provider="stripe",
        external_event_id="evt_1234567890",
        event_type="payment_intent.succeeded",
        raw_body=b'{"test": "data"}',
        headers={"x-signature": "test-sig"},
        signature="test-sig",
        signature_verified=True,
        request_id="req-456",
        payload=sample_stripe_payload,
        received_at=datetime.now(timezone.utc)
    )


@pytest.fixture
def sample_processed_event_paypal():
    return ProcessedEvent(
        provider="paypal",
        payment_id="capture-123",
        event_id="WH-1234567890",
        event_type="PAYMENT.CAPTURE.COMPLETED",
        status="COMPLETED",
        amount=100.00,
        currency="USD",
        fee=3.00,
        net_amount=97.00,
        order_id="order-123",
        customer_id="PAYER-123",
        provider_created_at=datetime(2026, 5, 10, 10, 0, 0, tzinfo=timezone.utc),
        received_at=datetime(2026, 5, 10, 10, 0, 1, tzinfo=timezone.utc),
        processed_at=datetime(2026, 5, 10, 10, 0, 2, tzinfo=timezone.utc),
        latency_ms=1000
    )


@pytest.fixture
def sample_processed_event_stripe():
    return ProcessedEvent(
        provider="stripe",
        payment_id="pi_1234567890",
        event_id="evt_1234567890",
        event_type="payment_intent.succeeded",
        status="succeeded",
        amount=100.00,
        currency="USD",
        fee=3.00,
        net_amount=97.00,
        order_id="order-123",
        customer_id="test@example.com",
        provider_created_at=datetime(2026, 5, 10, 10, 0, 0, tzinfo=timezone.utc),
        received_at=datetime(2026, 5, 10, 10, 0, 1, tzinfo=timezone.utc),
        processed_at=datetime(2026, 5, 10, 10, 0, 2, tzinfo=timezone.utc),
        latency_ms=1000
    )


@pytest.fixture
def client():
    return TestClient(app)
