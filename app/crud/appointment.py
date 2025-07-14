from typing import Union, List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.models import Appointment
from app.schema import AppointmentCreate, AppointmentOut, DoctorProfileOut, PatientProfileOut


async def list_appointments(db: AsyncSession):
    result = await db.execute(select(Appointment).where(Appointment.is_deleted == False))
    return result.scalars().all()


async def list_doctor_appointments(db: AsyncSession, doc_id: int):
    result = await db.execute(select(Appointment)
    .where(
        Appointment.is_deleted == False, Appointment.doctor_id == doc_id
    ))
    return result.scalars().all()


async def list_patient_appointments(db: AsyncSession, pat_id: int):
    result = await db.execute(select(Appointment)
    .where(
        Appointment.is_deleted == False, Appointment.patient_id == pat_id
    ))
    return result.scalars().all()


async def check_appointment_exists(db: AsyncSession, _id: int):
    result = await db.execute(select(Appointment).where(Appointment.id == _id, Appointment.is_deleted == False))
    return result.scalars().first()


async def get_appointment_by_id(db: AsyncSession, _id: int):
    result = await db.execute(select(Appointment).options(
        selectinload(Appointment.doctor),
        selectinload(Appointment.patient)
    ).where(Appointment.id == _id, Appointment.is_deleted == False))
    return result.scalars().first()


async def create_appointment(db: AsyncSession, appointment_data: AppointmentCreate):
    appointment = Appointment(
        patient_id=appointment_data.patient_id,
        doctor_id=appointment_data.doctor_id,
        appointment_time=appointment_data.appointment_time,
        reason=appointment_data.reason
    )
    db.add(appointment)
    await db.commit()

    appointment = await get_appointment_by_id(db=db, _id=appointment.id)
    return appointment


async def update_appointment(db: AsyncSession, appointment: Appointment, updated_data: dict):
    for key, value in updated_data.items():
        setattr(appointment, key, value)

    await db.commit()
    await db.refresh(appointment)
    return appointment


async def construct_appointment_serialized_response(appointment: Union[Appointment, List[Appointment]]) -> dict:
    if isinstance(appointment, list):
        final_response = [AppointmentOut.from_orm(apt).dict() for apt in appointment]
    else:
        final_response = AppointmentOut.from_orm(appointment).dict()
        final_response["doctor"] = DoctorProfileOut.from_orm(appointment.doctor).dict()
        final_response["patient"] = PatientProfileOut.from_orm(appointment.patient).dict()
    return final_response
