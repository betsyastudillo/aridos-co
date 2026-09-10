from typing import Optional
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.services.auth_service import hash_password, verify_password

def create_user(db: Session, user_create: UserCreate) -> User:
    new_user = User(
        document_id=user_create.document_id,
        full_name=user_create.full_name,
        email=user_create.email,
        hashed_password=hash_password(user_create.password),
        role=user_create.role,
        company_id=user_create.company_id,
        is_active=user_create.is_active,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_user_by_document_id(db: Session, document_id: str) -> Optional[User]:
    return db.query(User).filter(User.document_id == document_id).first()


def authenticate_user(db: Session, document_id: str, password: str) -> Optional[User]:
    user = get_user_by_document_id(db, document_id)
    if user and verify_password(password, user.hashed_password):
        return user
    return None