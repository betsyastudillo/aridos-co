from pydantic import BaseModel
from uuid import UUID
from decimal import Decimal
from datetime import datetime
from typing import Optional, Literal

class PaymentInitiateRequest(BaseModel):
    order_id: UUID

class PaymentResponse(BaseModel):
    id: UUID
    order_id: UUID
    bank_reference: str
    status: str
    amount: Decimal
    created_at: datetime
    confirmed_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class WebhookRequest(BaseModel):
    bank_reference: str
    status: Literal["confirmed", "failed"]