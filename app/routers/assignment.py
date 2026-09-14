from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from app.database import get_db
from app.schemas.assignment import AssignmentCreate, AssignmentResponse
from app.services.assignment_service import create_assignment, get_assignment_by_order, get_assignments


router = APIRouter(prefix="/assignments", tags=["Assignments"])


@router.get("/", response_model=AssignmentResponse)
def get_list_assignments(db: Session = Depends(get_db)):
    try:
        return get_assignments(db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/", response_model=AssignmentResponse)
def register_assignment(data: AssignmentCreate, db: Session = Depends(get_db)):
    try:
        return create_assignment(db, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/order/{order_id}", response_model=AssignmentResponse)
def get_assignment_by_order_id(order_id: UUID, db: Session = Depends(get_db)):
    assignment = get_assignment_by_order(db, order_id)
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found for this order")
    return assignment