from typing import Dict, Any, Callable
from app.mock_provider.base.base import AbstractProvider
from app.mock_provider.services.hmac_service import HMACService
from app.mock_provider.services.webhook_sender import WebhookSender


class EventProvider(AbstractProvider):
    def __init__(
        self,
        secret: str,
        webhook_url: str,
        generator: Callable[[], Dict[str, Any]]
    ):
        self.hmac = HMACService(secret)
        self.sender = WebhookSender(webhook_url)
        self.generator = generator

    async def generate_event(self) -> Dict[str, Any]:
        return self.generator()

    async def sign(self, payload: Dict[str, Any]) -> str:
        return self.hmac.sign(payload)

    async def send(self, payload: Dict[str, Any], signature: str) -> None:
        await self.sender.send(payload, signature)
