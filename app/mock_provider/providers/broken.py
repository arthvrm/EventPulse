from event_generators.broken import generate_payload as broken_generator
from core.event_provider import EventProvider


class BrokenProvider(EventProvider):
    def __init__(self, secret: str, webhook_url: str):
        super().__init__(
            secret=secret,
            webhook_url=webhook_url,
            generator=broken_generator
        )
