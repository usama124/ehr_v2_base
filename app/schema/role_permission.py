from typing import Optional

from pydantic import BaseModel

from app.core.enums import RoleEnum, PermissionsEnum


class Role(BaseModel):
    name: RoleEnum


class Permission(BaseModel):
    id: Optional[int]
    code: PermissionsEnum
    description: str


class PermissionBasicOut(BaseModel):
    code: PermissionsEnum


class RolePermissionCreate(BaseModel):
    role: RoleEnum
    permission: PermissionsEnum


class RolePermissionOut(BaseModel):
    permission: PermissionBasicOut

    class Config:
        from_attributes = True


class RoleOut(BaseModel):
    id: int
    name: str
    # role_permissions: list[RolePermissionOut]

    class Config:
        from_attributes = True
