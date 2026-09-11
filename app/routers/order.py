from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from app.database import get_db
from app.schemas.order import OrderCreate, OrderResponse
from app.services.order_service import create_order, edit_order, get_orders, get_order_by_id


router = APIRouter(prefix="/orders", tags=["Orders"])


@router.get("/", response_model=list[OrderResponse])
def list_orders(db: Session = Depends(get_db)):
    return get_orders(db)


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: UUID, db: Session = Depends(get_db)):
    order = get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.post("/", response_model=OrderResponse)
def create_new_order(order: OrderCreate, db: Session = Depends(get_db)):
    try:
        return create_order(db, order)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@router.put("/{order_id}", response_model=OrderResponse)
def update_order(order_id: UUID, order: OrderCreate, db: Session = Depends(get_db)):
    try:
        return edit_order(db, order_id, order)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order