from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.patient import Patient
from app.schemas.patient import PatientCreate, PatientUpdate

class PatientService:
    @staticmethod
    def create_patient(db: Session, payload: PatientCreate) -> Patient:
        patient = Patient(**payload.model_dump())
        db.add(patient)
        db.commit()
        db.refresh(patient)
        return patient

    @staticmethod
    def get_patient(db: Session, patient_id: str) -> Patient | None:
        return db.query(Patient).filter(Patient.id == patient_id, Patient.is_deleted == False).first()

    @staticmethod
    def search_patients(db: Session, query: str | None = None, skip: int = 0, limit: int = 50) -> list[Patient]:
        q = db.query(Patient).filter(Patient.is_deleted == False)
        if query:
            q = q.filter(
                or_(
                    Patient.full_name.ilike(f"%{query}%"),
                    Patient.phone.contains(query)
                )
            )
        return q.offset(skip).limit(limit).all()

    @staticmethod
    def update_patient(db: Session, patient: Patient, payload: PatientUpdate) -> Patient:
        update_data = payload.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(patient, field, value)
        db.commit()
        db.refresh(patient)
        return patient

    @staticmethod
    def soft_delete_patient(db: Session, patient: Patient) -> None:
        patient.is_deleted = True
        db.commit()
