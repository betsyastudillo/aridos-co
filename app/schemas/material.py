from typing import Optional
from pydantic import BaseModel
from uuid import UUID
from decimal import Decimal

class MaterialBase(BaseModel):
    name: str
    description: Optional[str]
    category: str
    price: Decimal # Decimal no Float para que coincida con el Numeric


class MaterialCreate(MaterialBase):
    pass


class MaterialResponse(MaterialBase):
    id: UUID
    is_active: bool

    class Config:
        from_attributes = True