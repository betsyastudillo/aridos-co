from typing import Optional
from uuid import UUID
from decimal import Decimal
from sqlalchemy.orm import Session
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.material import Material
from app.models.company import Company
from app.schemas.order import OrderCreate


def get_orders(db: Session,) -> Optional[Order]:
    return db.query(Order).all()


def get_order_by_id(db: Session, order_id: UUID) -> Optional[Order]:
    return db.query(Order).filter(Order.id == order_id).first()


def create_order(db: Session, order: OrderCreate) -> Order:
    company = db.query(Company).filter(Company.id == order.company_id).first()

    if not company:
        raise ValueError("Company not found")
    if company.verification_status != "approved":
        raise ValueError("Company is not approved")

    new_order = Order(company_id=order.company_id, status="created")
    db.add(new_order)
    db.flush()  # Asigna el id al pedido sin cerrar la transacción todavía

    subtotal = Decimal("0")
    tax = Decimal("0")
    for item_data in order.items:
        material = db.query(Material).filter(Material.id == item_data.material_id).first()

        if not material:
            raise ValueError(f"Material with id {item_data.material_id} not found")
        if not material.is_active:
            raise ValueError(f"Material with id {item_data.material_id} is not active")

        item_subtotal = material.price * item_data.quantity_m3
        item_tax = item_subtotal * material.tax_rate
        subtotal += item_subtotal
        tax += item_tax

        order_item = OrderItem(
            order_id=new_order.id,
            material_id=item_data.material_id,
            quantity_m3=item_data.quantity_m3,
            unit_price=material.price,
            subtotal=item_subtotal
        )
        db.add(order_item)

    new_order.subtotal = subtotal
    new_order.tax = tax
    new_order.total = subtotal + tax
    db.commit()
    db.refresh(new_order)
    return new_order


def edit_order(db: Session, order_id: UUID, order_data: OrderCreate) -> Optional[Order]:
    order = get_order_by_id(db, order_id)

    if not order:
        return None
    if order.status != "created":
        raise ValueError("Only orders with status 'created' can be edited")
    
    # Se borran los items existentes antes de agregar los nuevos
    db.query(OrderItem).filter(OrderItem.order_id == order.id).delete()
    db.flush()  # Asegura que los cambios se reflejen antes de agregar nuevos items

    subtotal = Decimal("0")
    tax = Decimal("0")

    for item_data in order_data.items:
        material = db.query(Material).filter(Material.id == item_data.material_id).first()

        if not material:
            raise ValueError(f"Material with id {item_data.material_id} not found")
        if not material.is_active:
            raise ValueError(f"Material with id {item_data.material_id} is not active")

        item_subtotal = material.price * item_data.quantity_m3
        item_tax = item_subtotal * material.tax_rate
        subtotal += item_subtotal
        tax += item_tax

        order_item = OrderItem(
            order_id=order.id,
            material_id=item_data.material_id,
            quantity_m3=item_data.quantity_m3,
            unit_price=material.price,
            subtotal=item_subtotal
        )
        db.add(order_item)

    order.subtotal = subtotal
    order.tax = tax
    order.total = subtotal + tax
    db.commit()
    db.refresh(order)
    return order