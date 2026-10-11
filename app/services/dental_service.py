from sqlalchemy.orm import Session
from datetime import datetime
from app.models.dental import ToothRecord
from app.schemas.dental import ToothRecordUpsert

class DentalService:
    @staticmethod
    def get_patient_chart(db: Session, patient_id: str) -> list[ToothRecord]:
        return db.query(ToothRecord).filter(
            ToothRecord.patient_id == patient_id
        ).order_by(ToothRecord.tooth_number.asc()).all()

    @staticmethod
    def upsert_tooth(db: Session, payload: ToothRecordUpsert) -> ToothRecord:
        tooth = db.query(ToothRecord).filter(
            ToothRecord.patient_id == payload.patient_id,
            ToothRecord.tooth_number == payload.tooth_number
        ).first()

        if tooth is None:
            tooth = ToothRecord(
                patient_id=payload.patient_id,
                tooth_number=payload.tooth_number,
            )
            db.add(tooth)

        tooth.condition = payload.condition
        # التاج والجذر يُحدَّثان فقط إن أُرسلا صراحةً
        if payload.crown_condition is not None:
            tooth.crown_condition = payload.crown_condition
        if payload.root_condition is not None:
            tooth.root_condition = payload.root_condition
        tooth.surfaces = payload.surfaces
        tooth.material = payload.material
        tooth.notes = payload.notes
        tooth.updated_at = datetime.utcnow()

        db.commit()
        db.refresh(tooth)
        return tooth