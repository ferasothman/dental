from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import date
from app.api.deps import get_db
from app.models.xray import PatientXRay

router = APIRouter()

class XRayCreate(BaseModel):
    patient_id: str
    title: str = "صورة شعاعية"
    image_data: str # Base64 Data URL
    taken_date: date = date.today()
    notes: str | None = None

@router.get("/patients/{patient_id}")
def get_patient_xrays(patient_id: str, db: Session = Depends(get_db)):
    return db.query(PatientXRay).filter(PatientXRay.patient_id == patient_id).order_by(PatientXRay.taken_date.desc()).all()

@router.post("")
def add_patient_xray(payload: XRayCreate, db: Session = Depends(get_db)):
    xray = PatientXRay(**payload.model_dump())
    db.add(xray)
    db.commit()
    db.refresh(xray)
    return xray

@router.delete("/{xray_id}")
def delete_patient_xray(xray_id: str, db: Session = Depends(get_db)):
    xray = db.query(PatientXRay).filter(PatientXRay.id == xray_id).first()
    if not xray:
        raise HTTPException(status_code=404, detail="الصورة غير موجودة")
    db.delete(xray)
    db.commit()
    return {"message": "تم حذف الصورة بنجاح"}
