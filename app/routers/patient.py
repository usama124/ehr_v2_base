from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import get_password_hash
from app.core.database import get_db
from app.core.dependency import require_permission
from app.core.enums import PermissionsEnum, RoleEnum
from app.core.responses import ApiCustomResponse, BadRequestException, NotFoundException
from app.crud import patient_crud, user_crud, role_perm_crud
from app.schema import PatientCreate, PatientUpdate

router = APIRouter()


@router.get("/list")
async def get_patients(
        db: AsyncSession = Depends(get_db),
        current_user=Depends(require_permission(PermissionsEnum.CAN_VIEW_PATIENT)),
):
    patients = await patient_crud.list_patients(db=db)
    response = await patient_crud.construct_patient_serialized_response(patients)
    return ApiCustomResponse.get_response(status_code=200, message="success", data=response)


@router.get("/get/{patient_id}")
async def get_patient_by_id(
        patient_id: int,
        db: AsyncSession = Depends(get_db),
        current_user=Depends(require_permission(PermissionsEnum.CAN_VIEW_PATIENT)),
):
    patient = await patient_crud.get_patient_by_id(db=db, _id=patient_id)
    if not patient:
        raise NotFoundException(message="Patient not found")

    response = await patient_crud.construct_patient_serialized_response(patient)
    return ApiCustomResponse.get_response(status_code=200, message="success", data=response)


@router.post("/add")
async def create_patient(
        patient: PatientCreate,
        db: AsyncSession = Depends(get_db),
        current_user=Depends(require_permission(PermissionsEnum.CAN_ADD_PATIENT)),
):
    if await user_crud.check_user_exists_by_email(db=db, email=patient.email.__str__()):
        raise BadRequestException(message="User already exists with same email")

    patient.password = get_password_hash(patient.password)
    role = await role_perm_crud.get_role_by_name(db=db, role=RoleEnum.PATIENT.value)
    db_patient = await patient_crud.create_patient(db=db, patient_data=patient, role_id=role.id)
    response = await patient_crud.construct_patient_serialized_response(db_patient)
    return ApiCustomResponse.get_response(status_code=200, message="success", data=response)


@router.put("/update/{patient_id}")
async def update_patient(
        patient_id: int,
        updated_data: PatientUpdate,
        db: AsyncSession = Depends(get_db),
        current_user=Depends(require_permission(PermissionsEnum.CAN_EDIT_PATIENT)),
):
    db_patient = await patient_crud.get_patient_by_id(db=db, _id=patient_id)
    if not db_patient:
        raise NotFoundException(message="Patient not found")

    db_patient = await patient_crud.update_patient(db=db, patient=db_patient,
                                                   updated_data=updated_data.dict(exclude_unset=True))
    response = await patient_crud.construct_patient_serialized_response(db_patient)
    return ApiCustomResponse.get_response(status_code=200, message="success", data=response)


@router.delete("/delete/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_patient(
        patient_id: int,
        db: AsyncSession = Depends(get_db),
        current_user=Depends(require_permission(PermissionsEnum.CAN_DELETE_PATIENT)),
):
    db_patient = await patient_crud.get_patient_by_id(db=db, _id=patient_id)
    if not db_patient:
        raise NotFoundException(message="Patient not found")

    db_patient.is_deleted = True
    db_patient.user.is_deleted = True
    await db.commit()
