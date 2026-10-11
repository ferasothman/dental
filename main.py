import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.core.config import settings
from app.core.database import Base, engine
from app.core.paths import resource_path
import app.models  # استيراد كافة الجداول إجبارياً قبل create_all
from app.api.v1.router import api_router

# إنشاء كافة الجداول والتأكد من وجودها
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="عيادة طب الأسنان",
    version="2.0.0",
    description="نظام إدارة عيادة الأسنان الذكي المتطور"
)

STATIC_DIR = resource_path("app/static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_PREFIX)

if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

@app.get("/", include_in_schema=False)
def root():
    index = STATIC_DIR / "index.html"
    if index.exists():
        return FileResponse(str(index))
    return {"message": "نظام عيادة طب الأسنان يعمل بنجاح", "docs": "/docs"}

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy"}