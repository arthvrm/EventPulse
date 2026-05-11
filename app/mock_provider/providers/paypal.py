from app.mock_provider.event_generators.paypal import generate_payload as paypal_generator
from app.mock_provider.core.event_provider import EventProvider

# PayPalMockProvider = lambda secret, webhook_url: EventProvider(
#     secret,
#     webhook_url,
#     paypal_generator
# )

class PayPalMockProvider(EventProvider):
    def __init__(self, secret: str, webhook_url: str):
        super().__init__(
            secret=secret,
            webhook_url=webhook_url,
            generator=paypal_generator
        )
