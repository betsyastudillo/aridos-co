from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from app.database import get_db
from app.schemas.payment import PaymentInitiateRequest, PaymentResponse, WebhookRequest
from app.services.payment_service import get_payments, initiate_payment, confirm_payment_webhook, get_payment_by_order


router = APIRouter(prefix="/payments", tags=["Payments"])


@router.get("/", response_model=PaymentResponse)
def get_all_payments(db: Session = Depends(get_db)):
    payment = get_payments(db)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found for this order")
    return payment


@router.get("/order/{order_id}", response_model=PaymentResponse)
def get_payment_by_order_id(order_id: UUID, db: Session = Depends(get_db)):
    payment = get_payment_by_order(db, order_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found for this order")
    return payment


@router.post("/initiate", response_model=PaymentResponse)
def start_payment(data: PaymentInitiateRequest, db: Session = Depends(get_db)):
    try:
        return initiate_payment(db, data.order_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/webhook", response_model=PaymentResponse)
def bank_webhook(data: WebhookRequest, db: Session = Depends(get_db)):
    try:
        return confirm_payment_webhook(db, data.bank_reference, data.status)
    except ValueError as e:

        raise HTTPException(status_code=400, detail=str(e))

