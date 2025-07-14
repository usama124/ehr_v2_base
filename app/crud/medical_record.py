from typing import Union, List

from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.models import MedicalRecord
from app.schema import MedicalRecordCreate, MedicalRecordOut, DoctorProfileOut, PatientProfileOut


async def get_medical_records_count(db: AsyncSession):
    count = await db.scalar(select(func.count(MedicalRecord.id)))
    return count


async def list_all_medical_reocrds(db: AsyncSession):
    result = await db.execute(select(MedicalRecord).where(MedicalRecord.is_deleted == False))
    return result.scalars().all()


async def list_medical_records_by_doctor_and_patient(db: AsyncSession, doc_id: int, patient_id: int = None):
    query = select(MedicalRecord).where(MedicalRecord.is_deleted == False, MedicalRecord.doctor_id == doc_id)
    if patient_id:
        query.where(MedicalRecord.patient_id == patient_id)
    result = await db.execute(query)
    return result.scalars().all()


async def check_medical_record_exists(db: AsyncSession, _id: int):
    result = await db.execute(select(MedicalRecord).where(MedicalRecord.id == _id, MedicalRecord.is_deleted == False))
    return result.scalars().first()


async def get_medical_record_by_id(db: AsyncSession, _id: int):
    result = await db.execute(select(MedicalRecord).options(
        selectinload(MedicalRecord.doctor),
        selectinload(MedicalRecord.patient)
    ).where(MedicalRecord.id == _id, MedicalRecord.is_deleted == False))
    return result.scalars().first()


async def create_medical_record(db: AsyncSession, record_data: MedicalRecordCreate):
    medical_record = MedicalRecord(
        patient_id=record_data.patient_id,
        doctor_id=record_data.doctor_id,
        visit_date=record_data.visit_date,
        diagnosis=record_data.diagnosis,
        treatment=record_data.treatment,
        notes=record_data.notes
    )
    db.add(medical_record)
    await db.commit()

    medical_record = await get_medical_record_by_id(db=db, _id=medical_record.id)
    return medical_record


async def update_medical_record(db: AsyncSession, medical_record: MedicalRecord, updated_data: dict):
    for key, value in updated_data.items():
        setattr(medical_record, key, value)

    await db.commit()
    await db.refresh(medical_record)
    return medical_record


async def construct_medical_record_serialized_response(
        medical_record: Union[MedicalRecord, List[MedicalRecord]]) -> dict:
    if isinstance(medical_record, list):
        final_response = [MedicalRecordOut.from_orm(record).dict() for record in medical_record]
    else:
        final_response = MedicalRecordOut.from_orm(medical_record).dict()
        final_response["doctor"] = DoctorProfileOut.from_orm(medical_record.doctor).dict()
        final_response["patient"] = PatientProfileOut.from_orm(medical_record.patient).dict()
    return final_response
