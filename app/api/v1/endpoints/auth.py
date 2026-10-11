from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.api.deps import get_db
from app.models.user import User

router = APIRouter()

class SetupDoctorRequest(BaseModel):
    username: str
    password: str
    full_name: str

class LoginRequest(BaseModel):
    username: str
    password: str

class CreateUserRequest(BaseModel):
    username: str
    password: str
    full_name: str
    role: str = "secretary" # 'doctor' أو 'secretary'

class UpdateUserRequest(BaseModel):
    full_name: str | None = None
    username: str | None = None
    password: str | None = None
    role: str | None = None

@router.get("/status")
def get_auth_status(db: Session = Depends(get_db)):
    user_count = db.query(User).count()
    return {"initialized": user_count > 0}

@router.post("/setup-doctor")
def setup_first_doctor(payload: SetupDoctorRequest, db: Session = Depends(get_db)):
    if db.query(User).count() > 0:
        raise HTTPException(status_code=400, detail="النظام مهيأ مسبقاً")
    
    doctor = User(
        username=payload.username.strip(),
        password_hash=User.hash_password(payload.password),
        full_name=payload.full_name.strip(),
        role="doctor"
    )
    db.add(doctor)
    db.commit()
    db.refresh(doctor)
    return {"message": "تم تهيئة الحساب بنجاح", "user": {"id": doctor.id, "username": doctor.username, "full_name": doctor.full_name, "role": doctor.role}}

@router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == payload.username.strip()).first()
    if not user or not user.verify_password(payload.password):
        raise HTTPException(status_code=401, detail="اسم المستخدم أو كلمة المرور غير صحيحة")
    
    return {
        "id": user.id,
        "username": user.username,
        "full_name": user.full_name,
        "role": user.role
    }

@router.get("/users")
def list_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return [{"id": u.id, "username": u.username, "full_name": u.full_name, "role": u.role, "created_at": u.created_at} for u in users]

@router.post("/users")
def create_user(payload: CreateUserRequest, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.username == payload.username.strip()).first()
    if existing:
        raise HTTPException(status_code=409, detail="اسم المستخدم هذا محجوز مسبقاً")
    
    user = User(
        username=payload.username.strip(),
        password_hash=User.hash_password(payload.password),
        full_name=payload.full_name.strip(),
        role=payload.role
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "تم إنشاء المستخدم بنجاح", "user": {"id": user.id, "username": user.username, "full_name": user.full_name, "role": user.role}}

@router.put("/users/{user_id}")
def update_user(user_id: str, payload: UpdateUserRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="المستخدم غير موجود")
    
    if payload.username and payload.username.strip() != user.username:
        exists = db.query(User).filter(User.username == payload.username.strip()).first()
        if exists:
            raise HTTPException(status_code=409, detail="اسم المستخدم الجديد محجوز مسبقاً")
        user.username = payload.username.strip()

    if payload.full_name:
        user.full_name = payload.full_name.strip()
    
    if payload.password and len(payload.password.strip()) > 0:
        user.password_hash = User.hash_password(payload.password.strip())

    if payload.role:
        user.role = payload.role

    db.commit()
    db.refresh(user)
    return {"id": user.id, "username": user.username, "full_name": user.full_name, "role": user.role}

@router.delete("/users/{user_id}")
def delete_user(user_id: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="المستخدم غير موجود")
    
    # التأكد من بقاء طبيب واحد على الأقل في النظام
    if user.role == "doctor":
        doctor_count = db.query(User).filter(User.role == "doctor").count()
        if doctor_count <= 1:
            raise HTTPException(status_code=400, detail="لا يمكن حذف الطبيب الوحيد المسجل في النظام")

    db.delete(user)
    db.commit()
    return {"message": "تم حذف المستخدم بنجاح"}
