import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text, UniqueConstraint
from sqlalchemy.orm import relationship
from app.core.database import Base

class ToothRecord(Base):
    __tablename__ = "tooth_records"
    # سجل واحد فقط لكل سن عند كل مريض
    __table_args__ = (UniqueConstraint("patient_id", "tooth_number", name="uq_patient_tooth"),)

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_id = Column(String(36), ForeignKey("patients.id"), nullable=False, index=True)
    tooth_number = Column(Integer, nullable=False)  # رقم السن FDI (11-48 أو 51-85)

    condition = Column(String(100), default="سليم", nullable=False)         # قديم: للتوافق مؤقتاً
    crown_condition = Column(String(100), default="سليم", nullable=False)    # حالة التاج
    root_condition = Column(String(100), default="سليم", nullable=False)     # حالة الجذر

    surfaces = Column(String(50), nullable=True)   # أسطح السن (مثل: MODB)
    material = Column(String(50), nullable=True)   # المادة المستخدمة
    notes = Column(Text, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # العلاقة مع المريض
    patient = relationship("Patient", back_populates="teeth")