from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.api.deps import get_db
from app.models.condition import ClinicalCondition

router = APIRouter()

class ConditionCreate(BaseModel):
    name: str
    color: str = "#3B82F6"
    requires_lab: bool = False
    default_cost: float = 0.0

class ConditionUpdate(BaseModel):
    name: str | None = None
    color: str | None = None
    requires_lab: bool | None = None
    default_cost: float | None = None

DEFAULT_CONDITIONS = [
    {"name": "سليم", "color": "#94A3B8", "requires_lab": False, "default_cost": 0.0},
    {"name": "تسوس", "color": "#F43F5E", "requires_lab": False, "default_cost": 0.0},
    {"name": "حشوة ضوئية", "color": "#0284C7", "requires_lab": False, "default_cost": 75000.0},
    {"name": "علاج عصب (لب)", "color": "#D97706", "requires_lab": False, "default_cost": 150000.0},
    {"name": "تاج زيركون", "color": "#9333EA", "requires_lab": True, "default_cost": 350000.0},
    {"name": "جسر خزفي", "color": "#8B5CF6", "requires_lab": True, "default_cost": 500000.0},
    {"name": "زرعة سنية", "color": "#059669", "requires_lab": True, "default_cost": 1200000.0},
    {"name": "قلع سن", "color": "#64748B", "requires_lab": False, "default_cost": 50000.0}
]

@router.get("")
def get_conditions(db: Session = Depends(get_db)):
    conditions = db.query(ClinicalCondition).all()
    if not conditions:
        for item in DEFAULT_CONDITIONS:
            db.add(ClinicalCondition(**item))
        db.commit()
        conditions = db.query(ClinicalCondition).all()
    return conditions

@router.post("")
def add_condition(payload: ConditionCreate, db: Session = Depends(get_db)):
    name = payload.name.strip()
    exists = db.query(ClinicalCondition).filter(ClinicalCondition.name == name).first()
    if exists:
        raise HTTPException(status_code=409, detail="الحالة مضافة مسبقاً")
    cond = ClinicalCondition(**payload.model_dump())
    db.add(cond)
    db.commit()
    db.refresh(cond)
    return cond

@router.put("/{condition_id}")
def update_condition(condition_id: str, payload: ConditionUpdate, db: Session = Depends(get_db)):
    cond = db.query(ClinicalCondition).filter(ClinicalCondition.id == condition_id).first()
    if not cond:
        raise HTTPException(status_code=404, detail="الحالة غير موجودة")
    if payload.name: cond.name = payload.name.strip()
    if payload.color: cond.color = payload.color
    if payload.requires_lab is not None: cond.requires_lab = payload.requires_lab
    if payload.default_cost is not None: cond.default_cost = payload.default_cost
    db.commit()
    db.refresh(cond)
    return cond

@router.delete("/{condition_id}")
def delete_condition(condition_id: str, db: Session = Depends(get_db)):
    cond = db.query(ClinicalCondition).filter(ClinicalCondition.id == condition_id).first()
    if not cond:
        raise HTTPException(status_code=404, detail="غير موجود")
    db.delete(cond)
    db.commit()
    return {"message": "تم الحذف بنجاح"}
