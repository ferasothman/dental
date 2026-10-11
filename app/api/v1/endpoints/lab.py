from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import date
from app.api.deps import get_db
from app.models.lab import LabOrder, DentalLab
from app.models.treatment_finance import TreatmentSession

router = APIRouter()

class LabCreate(BaseModel):
    name: str
    phone: str | None = None
    specialty: str | None = None

class LabOrderCreate(BaseModel):
    patient_id: str
    lab_name: str
    tooth_number: str | None = None
    work_type: str
    shade: str | None = None
    sent_date: date = date.today()
    expected_date: date | None = None
    lab_cost: float = 0.0
    patient_price: float = 0.0
    notes: str | None = None

class StatusUpdate(BaseModel):
    status: str

DEFAULT_LABS = [
    {"name": "مخبر النخبة للزيركون", "phone": "0991234567", "specialty": "زيركون وفينير"},
    {"name": "مخبر الشام للخزف", "phone": "0944567890", "specialty": "جسور وخزف"},
    {"name": "مخبر الدقة للتقويم", "phone": "0933112233", "specialty": "أجهزة تقويم وأطقم"}
]

# قائمة المخابر المعتمدة
@router.get("/labs")
def list_labs(db: Session = Depends(get_db)):
    labs = db.query(DentalLab).all()
    if not labs:
        for l in DEFAULT_LABS:
            db.add(DentalLab(**l))
        db.commit()
        labs = db.query(DentalLab).all()
    return labs

@router.post("/labs")
def add_lab(payload: LabCreate, db: Session = Depends(get_db)):
    name = payload.name.strip()
    exists = db.query(DentalLab).filter(DentalLab.name == name).first()
    if exists:
        raise HTTPException(status_code=409, detail="المخبر مضاف مسبقاً")
    lab = DentalLab(**payload.model_dump())
    db.add(lab)
    db.commit()
    db.refresh(lab)
    return lab

@router.delete("/labs/{lab_id}")
def delete_lab(lab_id: str, db: Session = Depends(get_db)):
    lab = db.query(DentalLab).filter(DentalLab.id == lab_id).first()
    if not lab:
        raise HTTPException(status_code=404, detail="غير موجود")
    db.delete(lab)
    db.commit()
    return {"message": "تم حذف المخبر"}

# طلبات المخبر
@router.get("")
def list_lab_orders(patient_id: str | None = Query(None), db: Session = Depends(get_db)):
    q = db.query(LabOrder)
    if patient_id:
        q = q.filter(LabOrder.patient_id == patient_id)
    return q.order_by(LabOrder.sent_date.desc()).all()

@router.post("")
def create_lab_order(payload: LabOrderCreate, db: Session = Depends(get_db)):
    order = LabOrder(**payload.model_dump())
    db.add(order)
    if payload.patient_price > 0:
        session_entry = TreatmentSession(
            patient_id=payload.patient_id,
            procedure_name=f"عمل مخبري: {payload.work_type} ({payload.tooth_number or 'عام'})",
            cost=payload.patient_price,
            notes=f"مرسل لمخبر: {payload.lab_name} - لون: {payload.shade or '---'}"
        )
        db.add(session_entry)
    db.commit()
    db.refresh(order)
    return order

@router.patch("/{order_id}/status")
def update_lab_status(order_id: str, payload: StatusUpdate, db: Session = Depends(get_db)):
    order = db.query(LabOrder).filter(LabOrder.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="غير موجود")
    order.status = payload.status
    db.commit()
    db.refresh(order)
    return order

@router.delete("/{order_id}")
def delete_lab_order(order_id: str, db: Session = Depends(get_db)):
    order = db.query(LabOrder).filter(LabOrder.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="غير موجود")
    db.delete(order)
    db.commit()
    return {"message": "تم الحذف بنجاح"}
