from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class MedicalRecordCreate(BaseModel):
    patient_id: int
    doctor_id: int
    visit_date: datetime
    diagnosis: str
    treatment: str
    notes: Optional[str] = None


class MedicalRecordUpdate(BaseModel):
    patient_id: Optional[int] = None
    doctor_id: Optional[int] = None
    visit_date: Optional[datetime] = None
    diagnosis: Optional[str] = None
    treatment: Optional[str] = None
    notes: Optional[str] = None


class MedicalRecordOut(BaseModel):
    id: int
    patient_id: int
    doctor_id: int
    visit_date: datetime
    diagnosis: str
    treatment: str
    notes: Optional[str] = None
    is_deleted: bool

    class Config:
        from_attributes = True
