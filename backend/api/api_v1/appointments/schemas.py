from datetime import datetime

from pydantic import BaseModel

from common.enums.enums_db import AppointmentStatus


class AppointmentBase(BaseModel):
    doctor_id: int
    patient_id: int
    service_id: int
    cabinet_id: int
    starts_at: datetime
    ends_at: datetime
    status: AppointmentStatus


class AppointmentRead(AppointmentBase):
    id: int


class AppointmentCreate(AppointmentBase):
    pass
