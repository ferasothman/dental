import uuid
from datetime import datetime, date
from sqlalchemy import Column, String, Float, Date, DateTime, ForeignKey, Text
from app.core.database import Base

class DentalLab(Base):
    __tablename__ = "dental_labs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), unique=True, nullable=False)
    phone = Column(String(30), nullable=True)
    specialty = Column(String(100), nullable=True) # زيركون، خزف، تقويم، أطقم

class LabOrder(Base):
    __tablename__ = "lab_orders"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_id = Column(String(36), ForeignKey("patients.id"), nullable=False)
    lab_name = Column(String(100), nullable=False)
    tooth_number = Column(String(50), nullable=True)
    work_type = Column(String(100), nullable=False)
    shade = Column(String(20), nullable=True)
    sent_date = Column(Date, default=date.today, nullable=False)
    expected_date = Column(Date, nullable=True)
    status = Column(String(30), default="Sent", nullable=False)
    lab_cost = Column(Float, default=0.0)
    patient_price = Column(Float, default=0.0)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
