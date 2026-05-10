from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class Payment(BaseModel):
    provider: str
    
    payment_id: str
    
    status: str
    amount: Decimal
    currency: str
    fee: Decimal = Decimal("0")
    net_amount: Decimal
    order_id: Optional[str] = None
    customer_id: Optional[str] = None
    
    created_at: datetime
    updated_at: datetime
    
    last_event_id: Optional[str] = None
