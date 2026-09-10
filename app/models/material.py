from sqlalchemy import Column, String, Numeric, Boolean
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.database import Base

class Material(Base):
    __tablename__ = "materials"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    category = Column(String, nullable=True)
    price = Column(Numeric(10, 2), nullable=False) # Se usa Numeric porque no tiene errores de redondeo como Float
    is_active = Column(Boolean, nullable=False, default=True)