from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class AppointmentCreate(BaseModel):
    patient_id: int
    doctor_id: int
    appointment_time: datetime = Field(..., example="2025-07-14 10:45:05")
    reason: Optional[str]


class AppointmentUpdate(BaseModel):
    patient_id: Optional[int] = None
    doctor_id: Optional[int] = None
    appointment_time: Optional[datetime] = Field(default=None, example="2025-07-14 10:45:05")
    reason: Optional[str] = None


class AppointmentOut(BaseModel):
    id: int
    patient_id: int
    doctor_id: int
    appointment_time: datetime
    reason: Optional[str]
    is_deleted: bool

    class Config:
        from_attributes = True
