from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, field_validator

# أرقام FDI الصالحة: دائمة 11-18 و21-28 و31-38 و41-48، ولبنية 51-55 و61-65 و71-75 و81-85
VALID_TEETH = (
    {q * 10 + n for q in (1, 2, 3, 4) for n in range(1, 9)}
    | {q * 10 + n for q in (5, 6, 7, 8) for n in range(1, 6)}
)

class ToothRecordBase(BaseModel):
    tooth_number: int = Field(..., description="رقم السن")
    condition: str = "سليم"
    crown_condition: str | None = Field(None, max_length=100)
    root_condition: str | None = Field(None, max_length=100)
    surfaces: str | None = Field(None, max_length=50)
    material: str | None = Field(None, max_length=50)
    notes: str | None = None

    @field_validator("tooth_number")
    @classmethod
    def check_tooth_number(cls, v: int) -> int:
        if v not in VALID_TEETH:
            raise ValueError("رقم السن غير صالح")
        return v

class ToothRecordUpsert(ToothRecordBase):
    patient_id: str

class ToothRecordResponse(ToothRecordBase):
    model_config = ConfigDict(from_attributes=True)
    id: str
    patient_id: str
    updated_at: datetime