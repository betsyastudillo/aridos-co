from sqlalchemy.orm import Session
from app.models.company import Company
from app.schemas.company import CompanyBase, CompanyCreate, CompanyResponse

def create_company(db: Session, company: CompanyCreate) -> CompanyResponse:
    new_company = Company(
        legal_name=company.legal_name,
        nit=company.nit,
        type=company.type,
        address=company.address,
        phone=company.phone,
        email=company.email,
        verification_status="pending"  # Default status
    )
    db.add(new_company)
    db.commit()
    db.refresh(new_company)
    return new_company