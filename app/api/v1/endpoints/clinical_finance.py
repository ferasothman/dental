from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import date
from app.api.deps import get_db
from app.models.treatment_finance import TreatmentSession, PaymentReceipt, ClinicExpense
from app.models.lab import LabOrder

router = APIRouter()

class SessionCreate(BaseModel):
    patient_id: str
    tooth_number: str | None = None
    procedure_name: str
    cost: float = 0.0
    notes: str | None = None

class SessionUpdate(BaseModel):
    procedure_name: str | None = None
    cost: float | None = None
    notes: str | None = None

class PaymentCreate(BaseModel):
    patient_id: str
    amount: float
    payment_method: str = "Cash"
    notes: str | None = None

class ExpenseCreate(BaseModel):
    expense_date: date | None = None
    category: str
    title: str
    amount: float
    notes: str | None = None

@router.post("/sessions")
def add_treatment_session(payload: SessionCreate, db: Session = Depends(get_db)):
    session = TreatmentSession(**payload.model_dump())
    db.add(session)
    db.commit()
    db.refresh(session)
    return session

@router.put("/sessions/{session_id}")
def update_session(session_id: str, payload: SessionUpdate, db: Session = Depends(get_db)):
    session = db.query(TreatmentSession).filter(TreatmentSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="الجلسة غير موجودة")
    if payload.procedure_name is not None: session.procedure_name = payload.procedure_name
    if payload.cost is not None: session.cost = float(payload.cost or 0.0)
    if payload.notes is not None: session.notes = payload.notes
    db.commit()
    db.refresh(session)
    return session

@router.delete("/sessions/{session_id}")
def delete_session(session_id: str, db: Session = Depends(get_db)):
    session = db.query(TreatmentSession).filter(TreatmentSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="الجلسة غير موجودة")
    db.delete(session)
    db.commit()
    return {"message": "تم حذف الجلسة بنجاح"}

@router.get("/sessions/patients/{patient_id}")
def get_patient_sessions(patient_id: str, db: Session = Depends(get_db)):
    return db.query(TreatmentSession).filter(TreatmentSession.patient_id == patient_id).order_by(TreatmentSession.session_date.desc()).all()

@router.post("/payments")
def add_payment(payload: PaymentCreate, db: Session = Depends(get_db)):
    payment = PaymentReceipt(**payload.model_dump())
    db.add(payment)
    db.commit()
    db.refresh(payment)
    return payment

@router.get("/finance/summary/{patient_id}")
def get_financial_summary(patient_id: str, db: Session = Depends(get_db)):
    sessions = db.query(TreatmentSession).filter(TreatmentSession.patient_id == patient_id).all()
    payments = db.query(PaymentReceipt).filter(PaymentReceipt.patient_id == patient_id).all()
    total_cost = float(sum((s.cost or 0.0) for s in sessions))
    total_paid = float(sum((p.amount or 0.0) for p in payments))
    balance_due = max(0.0, total_cost - total_paid)
    return {
        "total_cost": total_cost,
        "total_paid": total_paid,
        "balance_due": balance_due,
        "payments": payments
    }

@router.get("/expenses")
def list_expenses(db: Session = Depends(get_db)):
    return db.query(ClinicExpense).order_by(ClinicExpense.expense_date.desc()).all()

@router.post("/expenses")
def add_expense(payload: ExpenseCreate, db: Session = Depends(get_db)):
    data = payload.model_dump()
    if not data.get("expense_date"):
        data["expense_date"] = date.today()
    exp = ClinicExpense(**data)
    db.add(exp)
    db.commit()
    db.refresh(exp)
    return exp

@router.delete("/expenses/{exp_id}")
def delete_expense(exp_id: str, db: Session = Depends(get_db)):
    exp = db.query(ClinicExpense).filter(ClinicExpense.id == exp_id).first()
    if not exp:
        raise HTTPException(status_code=404, detail="المصروف غير موجود")
    db.delete(exp)
    db.commit()
    return {"message": "تم حذف المصروف"}

@router.get("/reports")
def get_financial_report(
    start_date: date | None = Query(None),
    end_date: date | None = Query(None),
    db: Session = Depends(get_db)
):
    q_payments = db.query(PaymentReceipt)
    q_labs = db.query(LabOrder)
    q_expenses = db.query(ClinicExpense)

    if start_date:
        q_payments = q_payments.filter(PaymentReceipt.payment_date >= start_date)
        q_labs = q_labs.filter(LabOrder.sent_date >= start_date)
        q_expenses = q_expenses.filter(ClinicExpense.expense_date >= start_date)

    if end_date:
        q_payments = q_payments.filter(PaymentReceipt.payment_date <= end_date)
        q_labs = q_labs.filter(LabOrder.sent_date <= end_date)
        q_expenses = q_expenses.filter(ClinicExpense.expense_date <= end_date)

    payments = q_payments.all()
    lab_orders = q_labs.all()
    expenses = q_expenses.all()

    # الحساب الآمن المحمي من قيم None
    total_revenue = float(sum((p.amount or 0.0) for p in payments))
    total_lab_expenses = float(sum((o.lab_cost or 0.0) for o in lab_orders))
    total_clinic_expenses = float(sum((e.amount or 0.0) for e in expenses))

    total_expenses = total_lab_expenses + total_clinic_expenses
    net_profit = total_revenue - total_expenses

    return {
        "start_date": str(start_date) if start_date else None,
        "end_date": str(end_date) if end_date else None,
        "total_revenue": total_revenue,
        "total_lab_expenses": total_lab_expenses,
        "total_clinic_expenses": total_clinic_expenses,
        "total_expenses": total_expenses,
        "net_profit": net_profit,
        "payments_count": len(payments),
        "expenses_count": len(expenses)
    }
