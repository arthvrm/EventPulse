import pytest
from app.backend.db.repository import EventRepository


class TestEventRepository:
    def test_repository_initialization(self):
        repo = EventRepository()
        assert len(repo._events) == 0
        assert len(repo._processed_ids) == 0

    def test_save_event(self, sample_processed_event_paypal):
        repo = EventRepository()
        repo.save(sample_processed_event_paypal)

        assert len(repo._events) == 1
        assert repo._events[0] == sample_processed_event_paypal
        assert sample_processed_event_paypal.event_id in repo._processed_ids

    def test_is_processed_true(self, sample_processed_event_paypal):
        repo = EventRepository()
        repo.save(sample_processed_event_paypal)

        assert repo.is_processed(sample_processed_event_paypal.event_id) is True

    def test_is_processed_false(self):
        repo = EventRepository()
        assert repo.is_processed("nonexistent-id") is False

    def test_save_multiple_events(self, sample_processed_event_paypal, sample_processed_event_stripe):
        repo = EventRepository()
        repo.save(sample_processed_event_paypal)
        repo.save(sample_processed_event_stripe)

        assert len(repo._events) == 2
        assert len(repo._processed_ids) == 2
        assert sample_processed_event_paypal.event_id in repo._processed_ids
        assert sample_processed_event_stripe.event_id in repo._processed_ids

    def test_save_duplicate_event(self, sample_processed_event_paypal):
        repo = EventRepository()
        repo.save(sample_processed_event_paypal)
        repo.save(sample_processed_event_paypal)  # Try to save again

        # Should still have only one event
        assert len(repo._events) == 1
        assert len(repo._processed_ids) == 1