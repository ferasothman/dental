from datetime import date, time
from sqlalchemy.orm import Session
from app.models.appointment import Appointment
from app.schemas.appointment import AppointmentCreate
from app.schemas.enums import AppointmentStatus

class AppointmentService:
    @staticmethod
    def is_slot_available(db: Session, appointment_date: date, appointment_time: time) -> bool:
        # الموعد متاح إذا لم يكن هناك حجز في نفس اليوم والوقت (إلا إذا كان ملغياً)
        existing = db.query(Appointment).filter(
            Appointment.appointment_date == appointment_date,
            Appointment.appointment_time == appointment_time,
            Appointment.status != AppointmentStatus.CANCELLED
        ).first()
        return existing is None

    @staticmethod
    def create_appointment(db: Session, payload: AppointmentCreate) -> Appointment:
        if not AppointmentService.is_slot_available(db, payload.appointment_date, payload.appointment_time):
            raise ValueError("عذراً، هذا التوقيت محجوز مسبقاً. يرجى اختيار وقت آخر.")

        appointment = Appointment(
            patient_id=payload.patient_id,
            appointment_date=payload.appointment_date,
            appointment_time=payload.appointment_time,
            notes=payload.notes,
            status=AppointmentStatus.BOOKED
        )
        db.add(appointment)
        db.commit()
        db.refresh(appointment)
        return appointment

    @staticmethod
    def list_appointments(db: Session, target_date: date | None = None, skip: int = 0, limit: int = 50) -> list[Appointment]:
        q = db.query(Appointment)
        if target_date:
            q = q.filter(Appointment.appointment_date == target_date)
        return q.order_by(Appointment.appointment_time.asc()).offset(skip).limit(limit).all()

    @staticmethod
    def update_status(db: Session, appointment_id: str, new_status: AppointmentStatus) -> Appointment | None:
        appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
        if appointment:
            appointment.status = new_status
            db.commit()
            db.refresh(appointment)
        return appointment
