from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class RawEvent(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        extra="allow",
    )
    internal_event_id: str
    provider: str
    external_event_id: str | None = None
    event_type: str | None = None
    raw_body: bytes
    headers: dict[str, str]
    query_params: dict[str, str] = Field(default_factory=dict)
    signature: str | None = None
    signature_verified: bool = False
    request_id: str
    client_ip: str | None = None
    payload: dict[str, Any] | None = None
    received_at: datetime