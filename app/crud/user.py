from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.core.enums import RoleEnum
from app.schema import UserCreate, UserOut, RoleOut, DoctorProfileOut, PatientProfileOut
from app.models import User, Doctor, Patient, Role, RolePermission


async def check_user_exists_by_email(db: AsyncSession, email: str) -> User:
    result = await db.execute(select(User).where(User.email == email, User.is_deleted == False))
    user = result.scalars().first()
    return user


async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(
        select(User)
        .options(
            selectinload(User.role).selectinload(Role.role_permissions).selectinload(RolePermission.permission),
            selectinload(User.doctor_profile),
            selectinload(User.patient_profile)
        )
        .where(User.email == email, User.is_deleted == False)
    )
    user = result.scalars().first()
    return user


async def create_doctor(db: AsyncSession, user_id: int, user_create: UserCreate) -> Doctor:
    doctor = Doctor(
        first_name=user_create.first_name,
        last_name=user_create.last_name,
        specialty=user_create.specialty,
        contact_number=user_create.contact_number,
        user_id=user_id
    )
    db.add(doctor)
    await db.commit()
    await db.refresh(doctor)
    return doctor


async def create_patient(db: AsyncSession, user_id: int, user_create: UserCreate) -> Patient:
    patient = Patient(
        first_name=user_create.first_name,
        last_name=user_create.last_name,
        date_of_birth=user_create.date_of_birth,
        contact_number=user_create.contact_number,
        gender=user_create.gender.value,
        user_id=user_id
    )
    db.add(patient)
    await db.commit()
    await db.refresh(patient)
    return patient


async def create_user(db: AsyncSession, role_id: int, user_create: UserCreate):
    user = User(
        email=user_create.email,
        password=user_create.password,
        role_id=role_id
    )
    db.add(user)
    await db.commit()
    if user_create.role == RoleEnum.DOCTOR:
        doctor = await create_doctor(db=db, user_id=user.id, user_create=user_create)
    elif user_create.role == RoleEnum.PATIENT:
        patient = await create_patient(db=db, user_id=user.id, user_create=user_create)
    await db.refresh(user)
    user = await get_user_by_email(db=db, email=user.email)
    user_response = await construct_user_serialized_response(user)
    return user_response


async def construct_user_serialized_response(user: User) -> dict:
    final_response = UserOut.from_orm(user).dict()
    final_response["role"] = RoleOut.from_orm(user.role).dict()
    final_response["role"]["permissions"] = []
    for role_perm in user.role.role_permissions:
        final_response["role"]["permissions"].append(role_perm.permission.code.value)

    if user.role.name == RoleEnum.DOCTOR:
        final_response["doctor_profile"] = DoctorProfileOut.from_orm(user.doctor_profile).dict()
    elif user.role.name == RoleEnum.PATIENT:
        final_response["patient_profile"] = PatientProfileOut.from_orm(user.patient_profile).dict()
    return final_response
