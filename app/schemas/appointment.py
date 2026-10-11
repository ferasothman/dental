from datetime import date, time, datetime
from pydantic import BaseModel, ConfigDict

class AppointmentCreate(BaseModel):
    patient_id: str
    appointment_date: date
    appointment_time: time
    notes: str | None = None

class AppointmentUpdate(BaseModel):
    appointment_date: date | None = None
    appointment_time: time | None = None
    notes: str | None = None
    status: str | None = None

class AppointmentStatusUpdate(BaseModel):
    status: str

class AppointmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    patient_id: str
    appointment_date: date
    appointment_time: time
    status: str = "Booked"
    notes: str | None = None
    created_at: datetime
