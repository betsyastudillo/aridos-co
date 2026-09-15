import uuid
from datetime import datetime
from typing import Optional
from uuid import UUID
from sqlalchemy.orm import Session
from app.models.payment import Payment
from app.models.order import Order


def get_payments(db: Session) -> list[Payment]:
    return db.query(Payment).all()


def get_payment_by_order(db: Session, order_id: UUID) -> Optional[Payment]:
    return db.query(Payment).filter(Payment.order_id == order_id).first()


def initiate_payment(db: Session, order_id: UUID) -> Payment:
    
    order = db.query(Order).filter(Order.id == order_id).first()
    
    if not order:
        raise ValueError("Order not found")
    
    if order.status != "transport_assigned":
        raise ValueError("Order must have transport assigned before initiating payment")

    existing = db.query(Payment).filter(Payment.order_id == order_id).first()
    
    if existing:
        raise ValueError("A payment already exists for this order")

    new_payment = Payment(
        order_id=order_id,
        bank_reference=str(uuid.uuid4()),
        status="pending",
        amount=order.total,
    )
    
    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)
    
    return new_payment


def confirm_payment_webhook(db: Session, bank_reference: str, status: str) -> Payment:
    
    payment = db.query(Payment).filter(Payment.bank_reference == bank_reference).first()
    
    if not payment:
        raise ValueError("Payment not found for this bank reference")
    
    if payment.status != "pending":
        raise ValueError(f"Payment already processed with status: {payment.status}")

    payment.status = status
    
    if status == "confirmed":
        payment.confirmed_at = datetime.utcnow()
        order = db.query(Order).filter(Order.id == payment.order_id).first()
        order.status = "payment_confirmed"

    db.commit()
    db.refresh(payment)
    
    return payment

