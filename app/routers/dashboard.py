from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependency import require_permission
from app.core.enums import PermissionsEnum
from app.core.responses import ApiCustomResponse
from app.crud import doctor_crud, patient_crud, appointment_crud, record_crud

router = APIRouter()


@router.get("/summary")
async def get_summary(
        db: AsyncSession = Depends(get_db),
        current_user=Depends(require_permission(PermissionsEnum.CAN_VIEW_STATS)),
):
    doctors = await doctor_crud.get_doctors_count(db=db)
    patients = await patient_crud.get_patients_count(db=db)
    appointments = await appointment_crud.get_appointments_count(db=db)
    medical_records = await record_crud.get_medical_records_count(db=db)

    response = {
        "total_patients": patients,
        "total_doctors": doctors,
        "total_appointments": appointments,
        "total_medical_records": medical_records,
    }
    return ApiCustomResponse.get_response(status_code=200, message="success", data=response)
