import uuid
from sqlalchemy import Column, String, Boolean, Float
from app.core.database import Base

class ClinicalCondition(Base):
    __tablename__ = "clinical_conditions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), unique=True, nullable=False)
    color = Column(String(30), default="#3B82F6") # كود اللون
    requires_lab = Column(Boolean, default=False)   # هل تحتاج مخبر؟
    default_cost = Column(Float, default=0.0)      # التكلفة الافتراضية
