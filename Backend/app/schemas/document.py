from typing import Optional
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class DocumentBase(BaseModel):
    id: UUID
    company_id: UUID
    document_type: str
    document_url: str
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None    

    class Config:
        from_attributes = True


class DocumentStatusUpdate(BaseModel):
    status: str