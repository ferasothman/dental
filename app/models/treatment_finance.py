import uuid
from datetime import datetime, date
from sqlalchemy import Column, String, Float, Date, DateTime, ForeignKey, Text
from app.core.database import Base

class TreatmentSession(Base):
    __tablename__ = "treatment_sessions"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_id = Column(String(36), ForeignKey("patients.id"), nullable=False)
    tooth_number = Column(String(50), nullable=True)
    session_date = Column(Date, default=date.today, nullable=False)
    procedure_name = Column(String(100), nullable=False)
    cost = Column(Float, default=0.0)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class PaymentReceipt(Base):
    __tablename__ = "payment_receipts"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_id = Column(String(36), ForeignKey("patients.id"), nullable=False)
    payment_date = Column(Date, default=date.today, nullable=False)
    amount = Column(Float, nullable=False)
    payment_method = Column(String(30), default="Cash")
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class ClinicExpense(Base):
    __tablename__ = "clinic_expenses"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    expense_date = Column(Date, default=date.today, nullable=False)
    category = Column(String(50), nullable=False) # مواد أسنان، إيجار، صيانة، تعقيم...
    title = Column(String(100), nullable=False)
    amount = Column(Float, nullable=False)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
