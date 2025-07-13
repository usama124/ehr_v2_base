from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.core.enums import RoleEnum, PermissionsEnum


class Role(Base):
    __tablename__ = "role"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Enum(RoleEnum), unique=True)

    role_permissions = relationship("RolePermission", back_populates="role")
    user = relationship("User", back_populates="role")


class Permission(Base):
    __tablename__ = "permission"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(Enum(PermissionsEnum), unique=True)
    description = Column(String(500))

    role_permissions = relationship("RolePermission", back_populates="permission")


class RolePermission(Base):
    __tablename__ = "role_permission"

    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer, ForeignKey("role.id"), nullable=False)
    permission_id = Column(Integer, ForeignKey("permission.id"), nullable=False)

    role = relationship("Role", back_populates="role_permissions")
    permission = relationship("Permission", back_populates="role_permissions")
