from datetime import date
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.models.appointment import Appointment
from app.schemas.appointment import AppointmentCreate, AppointmentUpdate, AppointmentResponse, AppointmentStatusUpdate
from app.services.appointment_service import AppointmentService

router = APIRouter()

@router.get("", response_model=list[AppointmentResponse])
def get_appointments(
    appointment_date: date | None = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    db: Session = Depends(get_db)
):
    return AppointmentService.list_appointments(db, target_date=appointment_date, skip=skip, limit=limit)

@router.get("/today", response_model=list[AppointmentResponse])
def get_today_appointments(db: Session = Depends(get_db)):
    return AppointmentService.list_appointments(db, target_date=date.today())

@router.post("", response_model=AppointmentResponse, status_code=status.HTTP_201_CREATED)
def create_appointment(payload: AppointmentCreate, db: Session = Depends(get_db)):
    try:
        return AppointmentService.create_appointment(db, payload)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

@router.put("/{appointment_id}", response_model=AppointmentResponse)
def update_appointment(appointment_id: str, payload: AppointmentUpdate, db: Session = Depends(get_db)):
    apt = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not apt:
        raise HTTPException(status_code=404, detail="الموعد غير موجود")
    if payload.appointment_date: apt.appointment_date = payload.appointment_date
    if payload.appointment_time: apt.appointment_time = payload.appointment_time
    if payload.notes is not None: apt.notes = payload.notes
    if payload.status: apt.status = payload.status
    db.commit()
    db.refresh(apt)
    return apt

@router.delete("/{appointment_id}")
def delete_appointment(appointment_id: str, db: Session = Depends(get_db)):
    apt = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not apt:
        raise HTTPException(status_code=404, detail="الموعد غير موجود")
    db.delete(apt)
    db.commit()
    return {"message": "تم حذف الموعد بنجاح"}
