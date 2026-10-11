from datetime import datetime
from pydantic import BaseModel, ConfigDict
from app.schemas.enums import Gender

class PatientBase(BaseModel):
    full_name: str
    phone: str
    age: int | None = None
    gender: Gender | None = None
    allergies: str | None = None
    medical_notes: str | None = None

class PatientCreate(PatientBase):
    pass

class PatientUpdate(BaseModel):
    full_name: str | None = None
    phone: str | None = None
    age: int | None = None
    gender: Gender | None = None
    allergies: str | None = None
    medical_notes: str | None = None

class PatientResponse(PatientBase):
    model_config = ConfigDict(from_attributes=True)
    id: str
    created_at: datetime
