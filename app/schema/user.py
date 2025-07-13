from pydantic import BaseModel, EmailStr
from app.core.enums import RoleEnum
from app.schema.role_permission import RoleOut


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: RoleEnum


class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: RoleOut

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str
