from pydantic import BaseModel
from uuid import UUID
from decimal import Decimal
from datetime import date


class VehicleBase(BaseModel):
    type: str
    capacity_m3: Decimal
    plate: str
    soat_expiration_date: date
    technical_inspection_expiration_date: date


class VehicleCreate(VehicleBase):
    pass


class VehicleResponse(VehicleBase):
    id: UUID
    is_active: bool

    class Config:
        from_attributes = True