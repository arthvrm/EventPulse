from abc import ABC, abstractmethod

from app.backend.schemas.processed_event import ProcessedEvent
from app.backend.schemas.raw_event import RawEvent


class BaseNormalizer(ABC):
    @abstractmethod
    def normalize(self, raw_event: RawEvent) -> ProcessedEvent:
        ...