from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependency import require_permission
from app.core.enums import PermissionsEnum, RoleEnum
from app.core.responses import ApiCustomResponse, NotFoundException
from app.crud import patient_crud, doctor_crud, record_crud
from app.schema import MedicalRecordCreate, MedicalRecordUpdate

router = APIRouter()


@router.get("/list")
async def get_medical_record(
        patient_id: int = None,
        db: AsyncSession = Depends(get_db),
        current_user=Depends(require_permission(PermissionsEnum.CAN_VIEW_RECORD)),
):
    if current_user.role.name == RoleEnum.DOCTOR:
        medical_records = await record_crud.list_medical_records_by_doctor_and_patient(db=db, patient_id=patient_id,
                                                                                       doc_id=current_user.doctor_profile.id)
    else:
        medical_records = await record_crud.list_all_medical_reocrds(db=db)
    response = await record_crud.construct_medical_record_serialized_response(medical_records)
    return ApiCustomResponse.get_response(status_code=200, message="success", data=response)


@router.get("/get/{record_id}")
async def get_medical_record_by_id(
        record_id: int,
        db: AsyncSession = Depends(get_db),
        current_user=Depends(require_permission(PermissionsEnum.CAN_VIEW_RECORD)),
):
    record = await record_crud.get_medical_record_by_id(db=db, _id=record_id)
    if not record:
        raise NotFoundException(message="Medical record not found")

    response = await record_crud.construct_medical_record_serialized_response(record)
    return ApiCustomResponse.get_response(status_code=200, message="success", data=response)


@router.post("/add")
async def create_medical_record(
        record: MedicalRecordCreate,
        db: AsyncSession = Depends(get_db),
        current_user=Depends(require_permission(PermissionsEnum.CAN_ADD_RECORD)),
):
    if not await doctor_crud.check_doctor_exists(db=db, _id=record.doctor_id):
        raise NotFoundException(message="Doctor not found")

    if not await patient_crud.check_patient_exists(db=db, _id=record.patient_id):
        raise NotFoundException(message="Patient not found")

    db_record = await record_crud.create_medical_record(db=db, record_data=record)
    response = await record_crud.construct_medical_record_serialized_response(db_record)
    return ApiCustomResponse.get_response(status_code=200, message="success", data=response)


@router.put("/update/{record_id}")
async def update_medical_record(
        record_id: int,
        updated_data: MedicalRecordUpdate,
        db: AsyncSession = Depends(get_db),
        current_user=Depends(require_permission(PermissionsEnum.CAN_EDIT_RECORD)),
):
    db_record = await record_crud.check_medical_record_exists(db=db, _id=record_id)
    if not db_record:
        raise NotFoundException(message="Medical record not found")

    db_record = await record_crud.update_medical_record(db=db, medical_record=db_record,
                                                        updated_data=updated_data.dict(exclude_unset=True))
    response = await record_crud.construct_medical_record_serialized_response(db_record)
    return ApiCustomResponse.get_response(status_code=200, message="success", data=response)


@router.delete("/delete/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_medical_record(
        record_id: int,
        db: AsyncSession = Depends(get_db),
        current_user=Depends(require_permission(PermissionsEnum.CAN_DELETE_RECORD)),
):
    db_record = await record_crud.check_medical_record_exists(db=db, _id=record_id)
    if not db_record:
        raise NotFoundException(message="Appointment not found")

    db_record.is_deleted = True
    await db.commit()
