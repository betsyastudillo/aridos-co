from pydantic import BaseModel
from uuid import UUID


class CompanyBase (BaseModel):
    legal_name: str
    nit: str
    type: str
    address: str
    phone: str
    email: str

class CompanyCreate(CompanyBase):
    pass

class CompanyResponse(CompanyBase):
    id: UUID
    verification_status: str

    class Config:
        from_attributes = True