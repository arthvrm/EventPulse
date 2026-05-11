from app.mock_provider.event_generators.stripe import generate_payload as stripe_generator
from app.mock_provider.core.event_provider import EventProvider

# StripeMockProvider = lambda secret, webhook_url: MockProvider(
#     secret,
#     webhook_url,
#     stripe_generator
# )

class StripeMockProvider(EventProvider):
    def __init__(self, secret: str, webhook_url: str):
        super().__init__(
            secret=secret,
            webhook_url=webhook_url,
            generator=stripe_generator
        )
