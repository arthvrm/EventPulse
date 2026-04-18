from abc import ABC, abstractmethod
from typing import Dict, Any


class AbstractProvider(ABC):
    @abstractmethod
    async def generate_event(self) -> Dict[str, Any]:
        """Generate mock event payload"""
        pass

    @abstractmethod
    async def sign(self, payload: Dict[str, Any]) -> str:
        """Generate HMAC signature"""
        pass

    @abstractmethod
    async def send(self, payload: Dict[str, Any], signature: str) -> None:
        """Send webhook"""
        pass
