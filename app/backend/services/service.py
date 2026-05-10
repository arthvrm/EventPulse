import logging

from pathlib import Path

from ..schemas.raw_event import RawEvent
from ..schemas.processed_event import ProcessedEvent
from ..db.repository import EventRepository


logger = logging.getLogger(str(Path(__name__)))

class WebhookService:
    def __init__(self, repo: EventRepository) -> None:
        self.repo = repo

    def process_events(self, payload: RawEvent) -> None:
        logger.info(f"Processing event {payload.event_id}")
        
        # Idempotency
        if self.repo.is_processed(payload.event_id):
            logger.info(f"Event already processed {payload.event_id}")
            return

        # Normalize
        event = self.normalize(payload)
        logger.info("Payload normalized", extra={"event_id": event.event_id})    # extra for json logger output

        # Save
        self.repo.save(event)
        logger.info(f"Event saved {payload.event_id}")

        # Analytics (поки просто лог)
        self._send_to_analytics(event)
    
    def normalize(self, event: RawEvent) -> ProcessedEvent:
        logger.info("Normalizing payload", extra={"event_id": event.event_id})
        return ProcessedEvent(
            id=event.event_id,
            type=event.event_type,
            payload=event.data,
        )
    
    def _send_to_analytics(self, event: ProcessedEvent) -> None:
        print(f"[ANALYTICS] Event processed: {event.type}")
        logger.info(f"Event send to analytics {event.id}")
