import os
import shutil
from typing import Optional
import uuid
from uuid import UUID
from fastapi import UploadFile
from sqlalchemy.orm import Session
from app.models.document import Document

UPLOAD_DIR = "uploads/documents"

def get_documents_by_company(db: Session, company_id: UUID) -> list[Document]:
    return db.query(Document).filter(Document.company_id == company_id).all()


def save_document_file(file: UploadFile, company_id: UUID) -> str:
    company_folder = os.path.join(UPLOAD_DIR, str(company_id))
    os.makedirs(company_folder, exist_ok=True)

    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(company_folder, unique_filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Para que la ruta quede como: "/uploads/documents/{company_id}/archivo.pdf" 
    relative_url = f"/{file_path}"
    return relative_url


def create_document(db: Session, company_id: UUID, document_type: str, file: UploadFile) -> Document:
    file_path = save_document_file(file, company_id)

    new_document = Document(
        company_id=company_id,
        document_type=document_type,
        document_url=file_path,
        status="pending"
    )

    db.add(new_document)
    db.commit()
    db.refresh(new_document)
    return new_document


# Actualizar el estado del documento
def update_document_status(db: Session, document_id: UUID, new_status: str) -> Optional[Document]:
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        return None

    document.status = new_status
    db.commit()
    db.refresh(document)
    return document


def replace_document_file(db: Session, document_id: UUID, new_file: UploadFile) -> Optional[Document]:
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        return None
    
    old_path = document.document_url.lstrip("/")
    if os.path.exists(old_path):
        os.remove(old_path)
        
    # Guarda el nuevo archivo
    new_file_path = save_document_file(new_file, document.company_id)

    # Actualiza el registro del documento con la nueva ruta del archivo
    document.document_url = new_file_path
    document.status = "pending"  # Reinicia el estado a "pending" 
    db.commit()
    db.refresh(document)
    return document