from datetime import date
from typing import Optional

from pydantic import BaseModel, EmailStr, model_validator

from app.core.enums import RoleEnum, Gender


class DoctorCreate(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    specialty: str
    contact_number: str


class PatientCreate(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    contact_number: str
    date_of_birth: date
    gender: Gender


class DoctorUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    specialty: Optional[str] = None
    contact_number: Optional[str] = None


class PatientUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    contact_number: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[Gender] = None


class DoctorProfileOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    specialty: str
    contact_number: str
    user_id: int
    is_deleted: bool

    class Config:
        from_attributes = True


class PatientProfileOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    contact_number: str
    date_of_birth: date
    gender: Gender
    user_id: int
    is_deleted: bool

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: RoleEnum

    first_name: Optional[str] = None
    last_name: Optional[str] = None
    specialty: Optional[str] = None
    contact_number: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[Gender] = None

    @model_validator(mode="after")
    def validate_fields_based_on_role(self):
        required_fields = []

        if self.role == RoleEnum.DOCTOR:
            required_fields = ["first_name", "last_name", "specialty", "contact_number"]
        elif self.role == RoleEnum.PATIENT:
            required_fields = ["first_name", "last_name", "date_of_birth", "contact_number", "gender"]

        missing = [field for field in required_fields if not getattr(self, field)]
        if missing:
            raise ValueError(f"Missing required fields for role {self.role.value}: {', '.join(missing)}")

        return self


class UserOut(BaseModel):
    id: int
    email: EmailStr
    role_id: int
    is_deleted: bool

    # role: RoleOut
    # doctor_profile: Optional[DoctorProfileOut]
    # patient_profile: Optional[PatientProfileOut]

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str
