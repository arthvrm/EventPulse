from typing import Type, Optional

from base.base import AbstractProvider
from providers.stripe import StripeMockProvider
from providers.paypal import PayPalMockProvider
from providers.broken import BrokenProvider


class ProviderFactory:
    _providers: dict[str, Type[AbstractProvider]] = {
        "stripe": StripeMockProvider,
        "paypal": PayPalMockProvider,
        "broken": BrokenProvider,
    }

    @classmethod
    def create(
        cls,    # cls бо classmethod не потребує створенння екземпляра класу
        provider_type: str,
        secret: str,
        webhook_url: str
    ) -> Optional[AbstractProvider]:
        provider_cls = cls._providers.get(provider_type, None)    # відповідно тут cls. як звернення до трибута класу

        if provider_cls is None:
            print(f"\nUnknown provider: {provider_type}\n")
            return None

        return provider_cls(secret=secret, webhook_url=webhook_url)
