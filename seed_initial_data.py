import asyncio
from sqlalchemy.future import select
from app.core.database import SessionLocal
from app.models import Role, Permission, RolePermission
from app.core.enums import RoleEnum, PermissionsEnum, AdminPermissions, DoctorPermissions, PatientPermissions, ReceptionistPermissions


role_permission_map = {
    RoleEnum.ADMIN: AdminPermissions,
    RoleEnum.DOCTOR: DoctorPermissions,
    RoleEnum.RECEPTIONIST: ReceptionistPermissions,
    RoleEnum.PATIENT: PatientPermissions,
}


async def seed_roles_permissions():
    async with SessionLocal() as session:
        # 1. Seed roles
        for role_enum in RoleEnum:
            result = await session.execute(select(Role).where(Role.name == role_enum))
            if not result.scalars().first():
                role = Role(name=role_enum)
                session.add(role)

        # 2. Seed permissions
        for perm_enum in PermissionsEnum:
            result = await session.execute(select(Permission).where(Permission.code == perm_enum))
            if not result.scalars().first():
                permission = Permission(code=perm_enum, description=perm_enum.value.replace("_", " ").title())
                session.add(permission)

        await session.commit()

        # 3. Seed RolePermissions
        # Fetch all roles and permissions into dicts
        result = await session.execute(select(Role))
        roles = {r.name: r for r in result.scalars().all()}

        result = await session.execute(select(Permission))
        permissions = {p.code: p for p in result.scalars().all()}

        # Create RolePermission mappings
        for role_name, perms in role_permission_map.items():
            role = roles[role_name]
            for perm_enum in perms:
                permission = permissions[perm_enum]
                result = await session.execute(
                    select(RolePermission).where(
                        RolePermission.role_id == role.id,
                        RolePermission.permission_id == permission.id
                    )
                )
                if not result.scalars().first():
                    session.add(RolePermission(role_id=role.id, permission_id=permission.id))

        await session.commit()
        print("✅ Role, permissions, and mappings seeded successfully.")


if __name__ == "__main__":
    asyncio.run(seed_roles_permissions())
