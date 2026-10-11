import re
import unicodedata

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.patient import Patient
from app.models.appointment import Appointment
from app.models.dental import ToothRecord
from app.models.treatment_finance import TreatmentSession, PaymentReceipt
from app.models.lab import LabOrder
from app.models.xray import PatientXRay
from app.schemas.patient import PatientCreate, PatientUpdate, PatientResponse
from app.services.patient_service import PatientService

router = APIRouter()

_AR_MARKS = re.compile(r"[\u064B-\u065F\u0670\u0640]")  # تشكيل وتطويل


def normalize_name(value: str | None) -> str:
    """توحيد الاسم للمقارنة: يتجاهل المسافات الزائدة والتشكيل وفروق (أ إ آ ا) و(ى ي) و(ة ه) والحروف الكبيرة."""
    s = unicodedata.normalize("NFKC", value or "")
    s = _AR_MARKS.sub("", s)
    for src, dst in (("أ", "ا"), ("إ", "ا"), ("آ", "ا"), ("ى", "ي"), ("ة", "ه")):
        s = s.replace(src, dst)
    return " ".join(s.lower().split())


def find_same_name(db: Session, name: str, exclude_id: str | None = None, limit: int = 5) -> list[dict]:
    target = normalize_name(name)
    if not target:
        return []
    rows = db.query(Patient.id, Patient.full_name, Patient.phone, Patient.age).filter(
        Patient.is_deleted.isnot(True)
    ).all()
    matches = []
    for pid, full_name, phone, age in rows:
        if pid == exclude_id:
            continue
        if normalize_name(full_name) == target:
            matches.append({"id": pid, "full_name": full_name, "phone": phone, "age": age})
            if len(matches) >= limit:
                break
    return matches


def duplicate_error(matches: list[dict]) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail={
            "code": "duplicate_name",
            "message": "يوجد مريض مسجل بنفس الاسم",
            "matches": matches,
        },
    )


@router.get("", response_model=list[PatientResponse])
def get_patients(
    q: str | None = Query(None, description="بحث بالاسم أو الهاتف"),
    skip: int = Query(0, ge=0),
    limit: int = Query(1000, ge=1, le=5000),
    db: Session = Depends(get_db),
):
    return PatientService.search_patients(db, query=q, skip=skip, limit=limit)


@router.post("", response_model=PatientResponse, status_code=status.HTTP_201_CREATED)
def create_patient(
    payload: PatientCreate,
    confirm_duplicate: bool = Query(False, description="تأكيد الإنشاء رغم وجود اسم مطابق"),
    db: Session = Depends(get_db),
):
    if not confirm_duplicate:
        matches = find_same_name(db, payload.full_name)
        if matches:
            raise duplicate_error(matches)
    return PatientService.create_patient(db, payload)


@router.get("/{patient_id}", response_model=PatientResponse)
def get_patient(patient_id: str, db: Session = Depends(get_db)):
    patient = PatientService.get_patient(db, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="المريض غير موجود")
    return patient


@router.put("/{patient_id}", response_model=PatientResponse)
def update_patient(
    patient_id: str,
    payload: PatientUpdate,
    confirm_duplicate: bool = Query(False),
    db: Session = Depends(get_db),
):
    patient = PatientService.get_patient(db, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="المريض غير موجود")
    new_name = getattr(payload, "full_name", None)
    if new_name and not confirm_duplicate and normalize_name(new_name) != normalize_name(patient.full_name):
        matches = find_same_name(db, new_name, exclude_id=patient_id)
        if matches:
            raise duplicate_error(matches)
    return PatientService.update_patient(db, patient, payload)


@router.get("/{patient_id}/delete-impact")
def get_delete_impact(patient_id: str, db: Session = Depends(get_db)):
    """ملخص ما هو مرتبط بالملف، يُعرض للطبيب قبل الحذف."""
    patient = PatientService.get_patient(db, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="المريض غير موجود")

    def count(model) -> int:
        return db.query(func.count(model.id)).filter(model.patient_id == patient_id).scalar() or 0

    total_cost = float(db.query(func.coalesce(func.sum(TreatmentSession.cost), 0.0))
                       .filter(TreatmentSession.patient_id == patient_id).scalar() or 0.0)
    total_paid = float(db.query(func.coalesce(func.sum(PaymentReceipt.amount), 0.0))
                       .filter(PaymentReceipt.patient_id == patient_id).scalar() or 0.0)
    return {
        "sessions": count(TreatmentSession),
        "total_cost": total_cost,
        "payments": count(PaymentReceipt),
        "total_paid": total_paid,
        "balance": total_cost - total_paid,
        "appointments": count(Appointment),
        "xrays": count(PatientXRay),
        "lab_orders": count(LabOrder),
        "teeth": count(ToothRecord),
    }


@router.delete("/{patient_id}")
def delete_patient(
    patient_id: str,
    confirm_name: str = Query(..., min_length=1, description="اسم المريض كما هو، للتأكيد"),
    db: Session = Depends(get_db),
):
    patient = PatientService.get_patient(db, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="المريض غير موجود")
    if normalize_name(confirm_name) != normalize_name(patient.full_name):
        raise HTTPException(status_code=400, detail="اسم التأكيد لا يطابق اسم المريض")
    PatientService.soft_delete_patient(db, patient)
    return {"message": "تم حذف ملف المريض"}
