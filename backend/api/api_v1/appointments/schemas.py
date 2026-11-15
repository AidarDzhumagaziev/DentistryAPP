from datetime import datetime

from pydantic import BaseModel, ConfigDict

from api.api_v1.cabinets.schemas import CabinetRead
from api.api_v1.doctors.schemas import DoctorRead, DoctorShortRead
from api.api_v1.patients.schemas import PatientShortRead
from api.api_v1.services.schemas import ServiceRead
from common.enums.enums_db import AppointmentStatus


class AppointmentBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    starts_at: datetime
    ends_at: datetime
    status: AppointmentStatus
    doctor: DoctorShortRead
    service: ServiceRead
    cabinet: CabinetRead


class AppointmentCreate(BaseModel):
    doctor_id: int
    service_id: int
    starts_at: datetime
    ends_at: datetime


class AppointmentUpdate(BaseModel):
    status: AppointmentStatus


class AppointmentPatientRead(AppointmentBase):
    id: int


class AppointmentDoctorRead(AppointmentPatientRead):
    patient: PatientShortRead


class AppointmentAdminRead(AppointmentDoctorRead):
    patient_id: int
    doctor: DoctorRead  # type: ignore[assignment]
