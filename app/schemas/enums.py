from enum import Enum

class Gender(str, Enum):
    MALE = "Male"
    FEMALE = "Female"
    OTHER = "Other"

class AppointmentStatus(str, Enum):
    BOOKED = "Booked"
    CONFIRMED = "Confirmed"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"
    NO_SHOW = "No-Show"

class ToothCondition(str, Enum):
    HEALTHY = "Healthy"
    CARIES = "Caries"           # تسوس
    FILLED = "Filled"           # حشوة
    CROWN = "Crown"             # تلبيسة
    ROOT_CANAL = "Root Canal"   # علاج عصب
    MISSING = "Missing"         # سن مفقود
    IMPLANT = "Implant"         # زرعة
