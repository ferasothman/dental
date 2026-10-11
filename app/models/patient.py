import uuid
from datetime import datetime
from sqlalchemy import Column, String, Date, Integer, DateTime, Boolean, Text
from sqlalchemy.orm import relationship
from app.core.database import Base

class Patient(Base):
    __tablename__ = "patients"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    full_name = Column(String(100), nullable=False, index=True)
    phone = Column(String(20), nullable=False, index=True)
    age = Column(Integer, nullable=True)            # العمر كرقم مباشر
    birth_date = Column(Date, nullable=True)
    gender = Column(String(10), nullable=True)      # الجنس
    allergies = Column(Text, nullable=True)
    medical_notes = Column(Text, nullable=True)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    appointments = relationship("Appointment", back_populates="patient", cascade="all, delete-orphan")
    teeth = relationship("ToothRecord", back_populates="patient", cascade="all, delete-orphan")
