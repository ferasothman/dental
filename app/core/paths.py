import os
import sys
from pathlib import Path


def resource_path(rel: str) -> Path:
    """ملفات داخل البرنامج (مثل static) - للقراءة فقط"""
    base = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parents[2]))
    return base / rel


def data_dir() -> Path:
    """مكان البيانات: يبقى بعد التحديث أو إعادة التثبيت"""
    base = Path(os.environ.get("PROGRAMDATA", Path.home())) / "DentalClinic"
    base.mkdir(parents=True, exist_ok=True)
    return base