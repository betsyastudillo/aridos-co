from typing import Optional
from uuid import UUID
from sqlalchemy.orm import Session
from app.models.company import Company
from app.schemas.company import CompanyBase, CompanyCreate, CompanyResponse


def get_companies(db: Session) -> list[Company]:
    return db.query(Company).filter(Company.is_active == True).all()


def get_company(db: Session, company_id: UUID) -> Optional[Company]:
    return db.query(Company).filter(Company.id == company_id).first()


def create_a_company(db: Session, company: CompanyCreate) -> Company:
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


def edit_company(db: Session, company_id: UUID, company_update: CompanyCreate) -> Optional[Company]:
    company = get_company(db, company_id)
    if not company:
        return None

    for key, value in company_update.model_dump().items():
        setattr(company, key, value)

    db.commit()
    db.refresh(company)
    return company


def deactivate_company(db: Session, company_id: UUID) -> Optional[Company]:
    company = get_company(db, company_id)
    if not company:
        return None

    company.is_active = False
    db.commit()
    return company