from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.core.enums import RoleEnum, PermissionsEnum
from app.models import Role, User
from app.schema.role_permission import RoleOut


async def get_role_by_name(db: AsyncSession, role: str):
    result = await db.execute(select(Role).where(Role.name == role))
    return result.scalars().first()


async def get_role_by_name_with_permissions(db: AsyncSession, role: str) -> dict:
    result = await db.execute(select(Role).options(selectinload(Role.role_permissions)).where(Role.name == role))
    role_obj = result.scalars().first()

    role_dict = RoleOut.from_orm(role_obj).dict()
    return role_dict


async def check_has_permission(user: User, permission_code: PermissionsEnum):
    if not user.role or not user.role.role_permissions:
        return False

    if user.role.name == RoleEnum.ADMIN:
        return True

    for role_perm in user.role.role_permissions:
        if role_perm.permission and role_perm.permission.code == permission_code:
            return True
    return False
