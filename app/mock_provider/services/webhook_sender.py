import httpx


class WebhookSender:
    def __init__(self, url: str):
        self.url = url

    async def send(self, payload: dict, signature: str):
        async with httpx.AsyncClient() as client:
            await client.post(
                self.url,
                json=payload,
                headers={
                    "X-Signature": signature
                },
                timeout=5.0
            )
