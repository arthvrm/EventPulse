import pytest
from unittest.mock import Mock
from app.backend.services.service import WebhookService
from app.backend.db.repository import EventRepository


class TestWebhookService:
    def test_process_events_success(self, sample_raw_event_paypal):
        repo = EventRepository()
        service = WebhookService(repo)

        service.process_events(sample_raw_event_paypal)

        assert len(repo._events) == 1
        assert repo._events[0].provider == "paypal"
        assert repo._events[0].event_id == "WH-1234567890"

    def test_process_events_idempotency(self, sample_raw_event_paypal):
        repo = EventRepository()
        service = WebhookService(repo)

        # Process first time
        service.process_events(sample_raw_event_paypal)
        assert len(repo._events) == 1

        # Process second time - should not add duplicate
        service.process_events(sample_raw_event_paypal)
        assert len(repo._events) == 1

    def test_process_events_stripe_success(self, sample_raw_event_stripe):
        repo = EventRepository()
        service = WebhookService(repo)

        service.process_events(sample_raw_event_stripe)

        assert len(repo._events) == 1
        assert repo._events[0].provider == "stripe"
        assert repo._events[0].event_id == "evt_1234567890"

    def test_process_events_unknown_provider(self):
        repo = EventRepository()
        service = WebhookService(repo)

        # Create raw event with unknown provider
        from app.backend.schemas.raw_event import RawEvent
        from datetime import datetime, timezone

        raw_event = RawEvent(
            internal_event_id="req-123",
            provider="unknown",
            raw_body=b'{}',
            headers={},
            request_id="req-123",
            received_at=datetime.now(timezone.utc)
        )

        with pytest.raises(ValueError, match="No normalizer for provider unknown"):
            service.process_events(raw_event)

    def test_normalize_paypal(self, sample_raw_event_paypal):
        repo = EventRepository()
        service = WebhookService(repo)

        result = service.normalize(sample_raw_event_paypal)

        assert result.provider == "paypal"
        assert result.amount == 100.00
        assert result.fee == 3.00
        assert result.net_amount == 97.00

    def test_normalize_stripe(self, sample_raw_event_stripe):
        repo = EventRepository()
        service = WebhookService(repo)

        result = service.normalize(sample_raw_event_stripe)

        assert result.provider == "stripe"
        assert result.amount == 100.00
        assert result.fee == 3.00
        assert result.net_amount == 97.00