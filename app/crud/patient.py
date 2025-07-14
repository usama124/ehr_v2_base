from typing import Union, List

from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.models import Patient, User, Appointment
from app.schema import PatientProfileOut, UserOut, PatientCreate, AppointmentOut, MedicalRecordOut


async def get_patients_count(db: AsyncSession):
    count = await db.scalar(select(func.count(Patient.id)))
    return count


async def list_patients(db: AsyncSession, patient_id: int = None):
    query = select(Patient).where(Patient.is_deleted == False)
    if patient_id:
        query = query.where(Patient.id == patient_id)
    result = await db.execute(query)
    return result.scalars().all()


async def list_patients_assigned_to_doctor(db: AsyncSession, doctor_id: int):
    stmt = (
        select(Patient)
        .join(Appointment, Appointment.patient_id == Patient.id)
        .where(
            Appointment.doctor_id == doctor_id,
            Appointment.is_deleted == False,
            Patient.is_deleted == False,
        )
        .distinct()
    )
    result = await db.execute(stmt)
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
        final_response["appointments"] = [AppointmentOut.from_orm(appointment).dict() for appointment in
                                          patient.appointments]
        final_response["medical_records"] = [MedicalRecordOut.from_orm(record).dict() for record in
                                             patient.medical_records]
    return final_response
