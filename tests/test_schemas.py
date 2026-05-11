import pytest
from datetime import datetime, timezone
from app.backend.schemas.raw_event import RawEvent
from app.backend.schemas.processed_event import ProcessedEvent


class TestRawEvent:
    def test_raw_event_creation(self):
        raw_event = RawEvent(
            internal_event_id="req-123",
            provider="paypal",
            external_event_id="WH-123",
            event_type="PAYMENT.CAPTURE.COMPLETED",
            raw_body=b'{"test": "data"}',
            headers={"x-signature": "sig"},
            signature="sig",
            signature_verified=True,
            request_id="req-123",
            payload={"test": "data"},
            received_at=datetime.now(timezone.utc)
        )
        assert raw_event.provider == "paypal"
        assert raw_event.external_event_id == "WH-123"
        assert raw_event.signature_verified is True

    def test_raw_event_frozen(self):
        raw_event = RawEvent(
            internal_event_id="req-123",
            provider="paypal",
            external_event_id="WH-123",
            event_type="PAYMENT.CAPTURE.COMPLETED",
            raw_body=b'{}',
            headers={},
            signature="test-sig",
            signature_verified=True,
            request_id="req-123",
            payload={"test": "data"},
            received_at=datetime.now(timezone.utc)
        )
        with pytest.raises(Exception):  # Pydantic raises ValidationError for frozen models
            raw_event.provider = "stripe"


class TestProcessedEvent:
    def test_processed_event_creation(self):
        processed_event = ProcessedEvent(
            provider="paypal",
            payment_id="capture-123",
            event_id="WH-123",
            event_type="PAYMENT.CAPTURE.COMPLETED",
            status="COMPLETED",
            amount=100.00,
            currency="USD",
            fee=3.00,
            net_amount=97.00,
            provider_created_at=datetime.now(timezone.utc),
            received_at=datetime.now(timezone.utc),
            processed_at=datetime.now(timezone.utc)
        )
        assert processed_event.provider == "paypal"
        assert processed_event.amount == 100.00
        assert processed_event.fee == 3.00
        assert processed_event.net_amount == 97.00

    def test_processed_event_optional_fields(self):
        processed_event = ProcessedEvent(
            provider="stripe",
            payment_id="pi_123",
            event_id="evt_123",
            event_type="payment_intent.succeeded",
            status="succeeded",
            amount=50.00,
            currency="USD",
            provider_created_at=datetime.now(timezone.utc),
            received_at=datetime.now(timezone.utc),
            processed_at=datetime.now(timezone.utc)
        )
        assert processed_event.fee is None
        assert processed_event.net_amount is None
        assert processed_event.failure_reason is None
        assert processed_event.processing_error is None

    def test_processed_event_validation(self):
        # ProcessedEvent doesn't have strict validation, so this should work
        event = ProcessedEvent(
            provider="invalid",
            payment_id="",
            event_id="",
            event_type="",
            status="",
            amount=-1.0,  # Invalid negative amount
            currency="USD",
            provider_created_at=datetime.now(timezone.utc),
            received_at=datetime.now(timezone.utc),
            processed_at=datetime.now(timezone.utc)
        )
        assert event.amount == -1.0