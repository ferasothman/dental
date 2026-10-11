from fastapi import APIRouter
from app.api.v1.endpoints import (
    patients,
    appointments,
    dental,
    clinical_finance,
    auth,
    conditions,
    lab,
    xray,
    backup
)

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(conditions.router, prefix="/conditions", tags=["Clinical Conditions"])
api_router.include_router(patients.router, prefix="/patients", tags=["Patients"])
api_router.include_router(appointments.router, prefix="/appointments", tags=["Appointments"])
api_router.include_router(dental.router, prefix="/dental-chart", tags=["Dental Chart"])
api_router.include_router(clinical_finance.router, prefix="/clinical-finance", tags=["Finance"])
api_router.include_router(lab.router, prefix="/lab-orders", tags=["Dental Lab"])
api_router.include_router(xray.router, prefix="/xrays", tags=["Dental X-Rays"])
api_router.include_router(backup.router, prefix="/backup", tags=["Backup & Restore"])
