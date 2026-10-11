from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schemas.dental import ToothRecordUpsert, ToothRecordResponse
from app.services.dental_service import DentalService

router = APIRouter()

@router.get("/patients/{patient_id}", response_model=list[ToothRecordResponse])
def get_patient_dental_chart(patient_id: str, db: Session = Depends(get_db)):
    return DentalService.get_patient_chart(db, patient_id)

@router.put("/tooth", response_model=ToothRecordResponse)
def update_tooth(payload: ToothRecordUpsert, db: Session = Depends(get_db)):
    return DentalService.upsert_tooth(db, payload)
