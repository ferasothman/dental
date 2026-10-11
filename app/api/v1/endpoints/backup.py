import os
import shutil
from datetime import datetime
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from app.core.database import engine

router = APIRouter()
DB_FILE = os.path.abspath(engine.url.database)

@router.get("/download")
def download_backup():
    if not os.path.exists(DB_FILE):
        raise HTTPException(status_code=404, detail="ملف قاعدة البيانات غير موجود على السيرفر")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"dental_backup_{timestamp}.db"
    return FileResponse(
        path=DB_FILE,
        filename=filename,
        media_type="application/octet-stream"
    )

@router.post("/restore")
async def restore_backup(file: UploadFile = File(...)):
    if not file.filename.endswith((".db", ".sqlite")):
        raise HTTPException(status_code=400, detail="يرجى رفع ملف بصيغة .db")
    
    engine.dispose()
    
    if os.path.exists(DB_FILE):
        shutil.copy2(DB_FILE, f"{DB_FILE}.safety_backup")
    
    with open(DB_FILE, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    return {"message": "تمت استعادة قاعدة البيانات بنجاح!"}
