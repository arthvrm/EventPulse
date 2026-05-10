from abc import ABC, abstractmethod

from ..schemas.processed_event import ProcessedEvent
from ..schemas.raw_event import RawEvent


class BaseNormalizer(ABC):
    @abstractmethod
    def normalize(self, raw_event: RawEvent) -> ProcessedEvent:
        ...