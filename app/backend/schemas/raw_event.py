from datetime import datetime
from typing import Any

from pydantic import BaseModel


class RawEvent(BaseModel):
    provider: str
    
    payment_id: str
    event_id: str
    
    payload: dict[str, Any]
    
    raw_body: str
    
    headers: dict[str, str]
    
    received_at: datetime
    
    signature_valid: bool
    
    processing_attempts: int = 0
