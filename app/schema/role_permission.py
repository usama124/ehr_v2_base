from typing import Optional

from pydantic import BaseModel

from app.core.enums import RoleEnum, PermissionsEnum


class Role(BaseModel):
    name: RoleEnum


class Permission(BaseModel):
    id: Optional[int]
    code: PermissionsEnum
    description: str


class RolePermissionCreate(BaseModel):
    role: RoleEnum
    permission: PermissionsEnum


class RolePermissionOut(BaseModel):
    id: int
    role: Role
    permission: Permission


class RoleOut(BaseModel):
    id: int
    name: RoleEnum
    role_permissions: RolePermissionOut
