from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependency import require_permission
from app.core.enums import PermissionsEnum, RoleEnum
from app.core.responses import ApiCustomResponse, NotFoundException
from app.crud import patient_crud, doctor_crud, appointment_crud
from app.schema import AppointmentCreate, AppointmentUpdate

router = APIRouter()


@router.get("/list")
async def get_appointments(
        db: AsyncSession = Depends(get_db),
        current_user=Depends(require_permission(PermissionsEnum.CAN_VIEW_APPOINTMENT)),
):
    if current_user.role.name == RoleEnum.DOCTOR:
        appointments = await appointment_crud.list_doctor_appointments(db=db, doc_id=current_user.doctor_profile.id)
    elif current_user.role.name == RoleEnum.PATIENT:
        appointments = await appointment_crud.list_patient_appointments(db=db, pat_id=current_user.patient_profile.id)
    else:
        appointments = await appointment_crud.list_appointments(db=db)
    response = await appointment_crud.construct_appointment_serialized_response(appointments)
    return ApiCustomResponse.get_response(status_code=200, message="success", data=response)


@router.get("/get/{appointment_id}")
async def get_appointment_by_id(
        appointment_id: int,
        db: AsyncSession = Depends(get_db),
        current_user=Depends(require_permission(PermissionsEnum.CAN_VIEW_APPOINTMENT)),
):
    appointment = await appointment_crud.get_appointment_by_id(db=db, _id=appointment_id)
    if not appointment:
        raise NotFoundException(message="Appointment not found")
    response = await appointment_crud.construct_appointment_serialized_response(appointments)
    return ApiCustomResponse.get_response(status_code=200, message="success", data=response)


@router.post("/add")
async def create_appointment(
        appointment: AppointmentCreate,
        db: AsyncSession = Depends(get_db),
        current_user=Depends(require_permission(PermissionsEnum.CAN_ADD_APPOINTMENT)),
):
    if not await doctor_crud.check_doctor_exists(db=db, _id=appointment.doctor_id):
        raise NotFoundException(message="Doctor not found")

    if not await patient_crud.check_patient_exists(db=db, _id=appointment.patient_id):
        raise NotFoundException(message="Patient not found")

    db_appointment = await appointment_crud.create_appointment(db=db, appointment_data=appointment)
    response = await appointment_crud.construct_appointment_serialized_response(db_appointment)
    return ApiCustomResponse.get_response(status_code=200, message="success", data=response)


@router.put("/update/{appointment_id}")
async def update_appointment(
        appointment_id: int,
        updated_data: AppointmentUpdate,
        db: AsyncSession = Depends(get_db),
        current_user=Depends(require_permission(PermissionsEnum.CAN_EDIT_APPOINTMENT)),
):
    db_appointment = await appointment_crud.get_appointment_by_id(db=db, _id=appointment_id)
    if not db_appointment:
        raise NotFoundException(message="Appointment not found")

    db_appointment = await appointment_crud.update_appointment(db=db, appointment=db_appointment,
                                                               updated_data=updated_data.dict(exclude_unset=True))
    response = await appointment_crud.construct_appointment_serialized_response(db_appointment)
    return ApiCustomResponse.get_response(status_code=200, message="success", data=response)


@router.delete("/delete/{appointment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_appointment(
        appointment_id: int,
        db: AsyncSession = Depends(get_db),
        current_user=Depends(require_permission(PermissionsEnum.CAN_DELETE_APPOINTMENT)),
):
    db_appointment = await appointment_crud.check_appointment_exists(db=db, _id=appointment_id)
    if not db_appointment:
        raise NotFoundException(message="Appointment not found")

    db_appointment.is_deleted = True
    await db.commit()
