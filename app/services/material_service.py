from typing import Optional
from uuid import UUID
from sqlalchemy.orm import Session
from app.models.material import Material
from app.schemas.material import MaterialCreate


def get_materials(db: Session) -> Optional[Material]:
    return db.query(Material).filter(Material.is_active == True).all()


def get_material_by_id(db: Session, material_id: UUID) -> Optional[Material]:
    return db.query(Material).filter(Material.id == material_id, Material.is_active == True).first()


def create_material(db: Session, material: MaterialCreate) -> Material:
    new_material = Material(
        name=material.name,
        description=material.description,
        category=material.category,
        price=material.price,
    )
    db.add(new_material)
    db.commit()
    db.refresh(new_material)
    return new_material


def edit_material(db: Session, material_id: UUID, material: MaterialCreate) -> Optional[Material]:
    material_exists = get_material_by_id(db, material_id)
    if not material_exists:
        return None

    for key, value in material.model_dump().items():
        setattr(material_exists, key, value)
    db.commit()
    db.refresh(material_exists)
    return material_exists


def deactivate_material(db: Session, material_id: UUID) -> Optional[Material]:
    material_exists = get_material_by_id(db, material_id)
    if not material_exists:
        return None
    material_exists.is_active = False
    db.commit()
    db.refresh(material_exists)
    return material_exists