from typing import Union, List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.models import Patient, User
from app.schema import PatientProfileOut, UserOut, PatientCreate


async def list_patients(db: AsyncSession):
    result = await db.execute(select(Patient).where(Patient.is_deleted == False))
    return result.scalars().all()


async def check_patient_exists(db: AsyncSession, _id: int):
    result = await db.execute(select(Patient).where(Patient.id == _id, Patient.is_deleted == False))
    return result.scalars().first()


async def get_patient_by_id(db: AsyncSession, _id: int):
    result = await db.execute(select(Patient).options(
        selectinload(Patient.user),
        selectinload(Patient.appointments),
        selectinload(Patient.medical_records)
    ).where(Patient.id == _id, Patient.is_deleted == False))
    return result.scalars().first()


async def create_patient(db: AsyncSession, patient_data: PatientCreate, role_id: int):
    user = User(
        email=patient_data.email.__str__(),
        password=patient_data.password,
        role_id=role_id
    )
    db.add(user)
    await db.commit()

    patient = Patient(
        first_name=patient_data.first_name,
        last_name=patient_data.last_name,
        date_of_birth=patient_data.date_of_birth,
        contact_number=patient_data.contact_number,
        gender=patient_data.gender,
        user_id=user.id
    )
    db.add(patient)
    await db.commit()
    await db.refresh(patient)

    patient = await get_patient_by_id(db=db, _id=patient.id)
    return patient


async def update_patient(db: AsyncSession, patient: Patient, updated_data: dict):
    for key, value in updated_data.items():
        setattr(patient, key, value)

    await db.commit()
    await db.refresh(patient)
    return patient


async def construct_patient_serialized_response(patient: Union[Patient, List[Patient]]) -> dict:
    if isinstance(patient, list):
        final_response = [PatientProfileOut.from_orm(pat).dict() for pat in patient]
    else:
        final_response = PatientProfileOut.from_orm(patient).dict()
        final_response["user"] = UserOut.from_orm(patient.user).dict()
        # TODO add appointments, and medical Record
    return final_response
