from datetime import datetime
from decimal import Decimal
from typing import Optional, Literal

from pydantic import BaseModel


class ProcessedEvent(BaseModel):
    provider: str
    
    payment_id: str
    event_id: str
    
    event_type: str
    status: str
    amount: Decimal  # Revenue Aggregation
    currency: str
    fee: Optional[Decimal] = None
    net_amount: Optional[Decimal] = None
    order_id: Optional[str] = None
    customer_id: Optional[str] = None
    failure_reason: Optional[str] = None
    processing_error: Optional[str] = None
    
    provider_created_at: datetime
    received_at: datetime  # Revenue Aggregation
    processed_at: datetime
    
    latency_ms: Optional[int] = None
    
    processing_error: Optional[str] = None
