from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import get_password_hash
from app.core.database import get_db
from app.core.dependency import require_permission
from app.core.enums import PermissionsEnum, RoleEnum
from app.core.responses import ApiCustomResponse, BadRequestException, NotFoundException
from app.crud import doctor_crud, user_crud, role_perm_crud
from app.schema import DoctorCreate, DoctorUpdate

router = APIRouter()


@router.get("/list")
async def get_doctors(
        db: AsyncSession = Depends(get_db),
        current_user=Depends(require_permission(PermissionsEnum.CAN_VIEW_DOCTOR)),
):
    doctors = await doctor_crud.list_doctors(db=db)
    response = await doctor_crud.construct_doctor_serialized_response(doctors)
    return ApiCustomResponse.get_response(status_code=200, message="success", data=response)


@router.get("/get/{doctor_id}")
async def get_doctor_by_id(
        doctor_id: int,
        db: AsyncSession = Depends(get_db),
        current_user=Depends(require_permission(PermissionsEnum.CAN_VIEW_DOCTOR)),
):
    doctors = await doctor_crud.get_doctor_by_id(db=db, _id=doctor_id)
    response = await doctor_crud.construct_doctor_serialized_response(doctors)
    return ApiCustomResponse.get_response(status_code=200, message="success", data=response)


@router.post("/add")
async def create_doctor(
        doctor: DoctorCreate,
        db: AsyncSession = Depends(get_db),
        current_user=Depends(require_permission(PermissionsEnum.CAN_ADD_DOCTOR)),
):
    if await user_crud.check_user_exists_by_email(db=db, email=doctor.email.__str__()):
        raise BadRequestException(message="User already exists with same email")

    doctor.password = get_password_hash(doctor.password)
    role = await role_perm_crud.get_role_by_name(db=db, role=RoleEnum.DOCTOR.value)
    db_doctor = await doctor_crud.create_doctor(db=db, doctor_data=doctor, role_id=role.id)
    response = await doctor_crud.construct_doctor_serialized_response(db_doctor)
    return ApiCustomResponse.get_response(status_code=200, message="success", data=response)


@router.put("/update/{doctor_id}")
async def update_doctor(
        doctor_id: int,
        updated_data: DoctorUpdate,
        db: AsyncSession = Depends(get_db),
        current_user=Depends(require_permission(PermissionsEnum.CAN_EDIT_DOCTOR)),
):
    db_doctor = await doctor_crud.get_doctor_by_id(db=db, _id=doctor_id)
    if not db_doctor:
        raise NotFoundException(message="Doctor not found")

    db_doctor = await doctor_crud.update_doctor(db=db, doctor=db_doctor,
                                                updated_data=updated_data.dict(exclude_unset=True))
    response = await doctor_crud.construct_doctor_serialized_response(db_doctor)
    return ApiCustomResponse.get_response(status_code=200, message="success", data=response)


@router.delete("/delete/{doctor_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_doctor(
        doctor_id: int,
        db: AsyncSession = Depends(get_db),
        current_user=Depends(require_permission(PermissionsEnum.CAN_DELETE_DOCTOR)),
):
    db_doctor = await doctor_crud.get_doctor_by_id(db=db, _id=doctor_id)
    if not db_doctor:
        raise NotFoundException(message="Doctor not found")

    db_doctor.is_deleted = True
    db_doctor.user.is_deleted = True
    await db.commit()
    # return ApiCustomResponse.get_response(status_code=200, message="success", data={"message": "Deleted successfully."})
