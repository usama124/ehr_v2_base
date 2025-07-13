from enum import Enum as PyEnum


class RoleEnum(PyEnum):
    ADMIN = "ADMIN"
    DOCTOR = "DOCTOR"
    RECEPTIONIST = "RECEPTIONIST"
    PATIENT = "PATIENT"


class PermissionsEnum(PyEnum):
    CAN_ADD_USER = "CAN_ADD_USER"
    CAN_VIEW_USER = "CAN_VIEW_USER"
    CAN_EDIT_USER = "CAN_EDIT_USER"
    CAN_DELETE_USER = "CAN_DELETE_USER"

    CAN_ADD_DOCTOR = "CAN_ADD_DOCTOR"
    CAN_EDIT_DOCTOR = "CAN_EDIT_DOCTOR"
    CAN_VIEW_DOCTOR = "CAN_VIEW_DOCTOR"
    CAN_DELETE_DOCTOR = "CAN_DELETE_DOCTOR"

    CAN_ADD_PATIENT = "CAN_ADD_PATIENT"
    CAN_EDIT_PATIENT = "CAN_EDIT_PATIENT"
    CAN_VIEW_PATIENT = "CAN_VIEW_PATIENT"
    CAN_DELETE_PATIENT = "CAN_DELETE_PATIENT"

    CAN_ADD_APPOINTMENT = "CAN_ADD_APPOINTMENT"
    CAN_EDIT_APPOINTMENT = "CAN_EDIT_APPOINTMENT"
    CAN_VIEW_APPOINTMENT = "CAN_VIEW_APPOINTMENT"
    CAN_DELETE_APPOINTMENT = "CAN_DELETE_APPOINTMENT"

    CAN_ADD_RECORD = "CAN_ADD_RECORD"
    CAN_EDIT_RECORD = "CAN_EDIT_RECORD"
    CAN_VIEW_RECORD = "CAN_VIEW_RECORD"
    CAN_DELETE_RECORD = "CAN_DELETE_RECORD"

AdminPermissions = [
    PermissionsEnum.CAN_ADD_USER,
    PermissionsEnum.CAN_VIEW_USER,
    PermissionsEnum.CAN_EDIT_USER,
    PermissionsEnum.CAN_DELETE_USER,

    PermissionsEnum.CAN_ADD_DOCTOR,
    PermissionsEnum.CAN_VIEW_DOCTOR,
    PermissionsEnum.CAN_EDIT_DOCTOR,
    PermissionsEnum.CAN_DELETE_DOCTOR,

    PermissionsEnum.CAN_ADD_PATIENT,
    PermissionsEnum.CAN_VIEW_PATIENT,
    PermissionsEnum.CAN_EDIT_PATIENT,
    PermissionsEnum.CAN_DELETE_PATIENT,

    PermissionsEnum.CAN_ADD_APPOINTMENT,
    PermissionsEnum.CAN_VIEW_APPOINTMENT,
    PermissionsEnum.CAN_EDIT_APPOINTMENT,
    PermissionsEnum.CAN_DELETE_APPOINTMENT,

    PermissionsEnum.CAN_ADD_RECORD,
    PermissionsEnum.CAN_VIEW_RECORD,
    PermissionsEnum.CAN_EDIT_RECORD,
    PermissionsEnum.CAN_DELETE_RECORD,
]

DoctorPermissions = [
    PermissionsEnum.CAN_VIEW_APPOINTMENT,

    PermissionsEnum.CAN_ADD_RECORD,
    PermissionsEnum.CAN_EDIT_RECORD,
    PermissionsEnum.CAN_VIEW_RECORD,
    PermissionsEnum.CAN_DELETE_RECORD,

    PermissionsEnum.CAN_VIEW_PATIENT,
]

ReceptionistPermissions = [
    PermissionsEnum.CAN_ADD_APPOINTMENT,
    PermissionsEnum.CAN_VIEW_APPOINTMENT,
    PermissionsEnum.CAN_EDIT_APPOINTMENT,
    PermissionsEnum.CAN_DELETE_APPOINTMENT,

    PermissionsEnum.CAN_VIEW_PATIENT,
]

PatientPermissions = [
    PermissionsEnum.CAN_VIEW_APPOINTMENT,

    PermissionsEnum.CAN_VIEW_PATIENT,
]
