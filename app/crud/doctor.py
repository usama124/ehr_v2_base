from typing import Union, List

from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.models import Doctor, User
from app.schema import DoctorProfileOut, UserOut, DoctorCreate


async def get_doctors_count(db: AsyncSession):
    count = await db.scalar(select(func.count(Doctor.id)))
    return count


async def list_doctors(db: AsyncSession):
    result = await db.execute(select(Doctor).where(Doctor.is_deleted == False))
    return result.scalars().all()


async def check_doctor_exists(db: AsyncSession, _id: int):
    result = await db.execute(select(Doctor).where(Doctor.id == _id, Doctor.is_deleted == False))
    return result.scalars().first()


async def get_doctor_by_id(db: AsyncSession, _id: int):
    result = await db.execute(select(Doctor).options(
        selectinload(Doctor.user),
        selectinload(Doctor.appointments),
        selectinload(Doctor.medical_records)
    ).where(Doctor.id == _id, Doctor.is_deleted == False))
    return result.scalars().first()


async def create_doctor(db: AsyncSession, doctor_data: DoctorCreate, role_id: int):
    user = User(
        email=doctor_data.email.__str__(),
        password=doctor_data.password,
        role_id=role_id
    )
    db.add(user)
    await db.commit()

    doctor = Doctor(
        first_name=doctor_data.first_name,
        last_name=doctor_data.last_name,
        specialty=doctor_data.specialty,
        contact_number=doctor_data.contact_number,
        user_id=user.id
    )
    db.add(doctor)
    await db.commit()
    await db.refresh(doctor)

    doctor = await get_doctor_by_id(db=db, _id=doctor.id)
    return doctor


async def update_doctor(db: AsyncSession, doctor: Doctor, updated_data: dict):
    for key, value in updated_data.items():
        setattr(doctor, key, value)

    await db.commit()
    await db.refresh(doctor)
    return doctor


async def construct_doctor_serialized_response(doctor: Union[Doctor, List[Doctor]]) -> dict:
    if isinstance(doctor, list):
        final_response = [DoctorProfileOut.from_orm(doc).dict() for doc in doctor]
    else:
        final_response = DoctorProfileOut.from_orm(doctor).dict()
        final_response["user"] = UserOut.from_orm(doctor.user).dict()
        # TODO add appointments, and medical Record
    return final_response
