from typing import List
from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.company import Company
from app.schemas.company import CompanyBase, CompanyCreate, CompanyResponse
from app.services.company_service import create_a_company, get_companies, get_company, edit_company, deactivate_company

router = APIRouter(prefix="/companies", tags=["Companies"])

@router.get("/", response_model=List[CompanyResponse])
def list_companies(db: Session = Depends(get_db)):
    return get_companies(db)


@router.get("/{company_id}", response_model=CompanyResponse)
def get_company_by_id(company_id: UUID, db: Session = Depends(get_db)):
    company = get_company(db, company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company


@router.post("/", response_model=CompanyResponse)
def create_company(company: CompanyCreate, db: Session = Depends(get_db)):
    return create_a_company(db=db, company=company)


@router.put("/{company_id}", response_model=CompanyResponse)
def update_company(company_id: UUID, company_update: CompanyCreate, db: Session = Depends(get_db)):
    company = edit_company(db, company_id, company_update)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company


@router.delete("/{company_id}")
def remove_company(company_id: UUID, db: Session = Depends(get_db)):
    company = deactivate_company(db, company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return {"detail": "Company deactivated successfully"}
    