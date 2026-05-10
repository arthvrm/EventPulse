from typing import Set
from schemas.processed_event import ProcessedEvent


class EventRepository:
    def __init__(self) -> None:
        self._events: list[ProcessedEvent] = []
        self._processed_ids: Set[str] = set()

    def is_processed(self, event_id: str) -> bool:
        return event_id in self._processed_ids

    def save(self, event: ProcessedEvent) -> None:
        if not self.is_processed(event.event_id):
            self._events.append(event)
            self._processed_ids.add(event.event_id)
