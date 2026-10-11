import uuid
from datetime import datetime, date
from sqlalchemy import Column, String, Date, DateTime, ForeignKey, Text
from app.core.database import Base

class PatientXRay(Base):
    __tablename__ = "patient_xrays"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_id = Column(String(36), ForeignKey("patients.id"), nullable=False)
    title = Column(String(100), default="صورة شعاعية")
    image_data = Column(Text, nullable=False) # تخزين الصورة بصيغة Base64 لتسهيل النقل
    taken_date = Column(Date, default=date.today, nullable=False)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
