from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.company import CompanyBase, CompanyCreate, CompanyResponse
from app.services.company_service import create_company

router = APIRouter(prefix="/companies", tags=["Companies"])

@router.post("/", response_model=CompanyResponse)
def create_company_(company: CompanyCreate, db: Session = Depends(get_db)):
    return create_company(db=db, company=company)