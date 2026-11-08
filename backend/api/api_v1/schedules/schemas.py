from datetime import date, time

from pydantic import BaseModel, ConfigDict, Field, model_validator

from common.enums.enums_db import ReasonType


# Work schedule schema
class WorkScheduleBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    doctor_id: int
    cabinet_id: int
    weekday: int = Field(ge=1, le=7)
    start_time: time
    end_time: time


class WorkScheduleCreate(WorkScheduleBase):
    @model_validator(mode="after")
    def validate_time(self) -> "WorkScheduleCreate":
        if self.start_time >= self.end_time:
            raise ValueError("end_time must be greater than start_time")
        return self


class WorkScheduleRead(WorkScheduleBase):
    id: int


class WorkScheduleUpdate(BaseModel):
    cabinet_id: int
    start_time: time
    end_time: time

    @model_validator(mode="after")
    def validate_time(self) -> "WorkScheduleUpdate":
        if self.start_time >= self.end_time:
            raise ValueError("end_time must be greater than start_time")
        return self


class WorkScheduleUpdatePartial(BaseModel):
    cabinet_id: int | None = None
    start_time: time | None = None
    end_time: time | None = None


# Schedules exception schema
class ScheduleExceptionBase(BaseModel):
    doctor_id: int
    date_from: date
    date_to: date
    reason: ReasonType


class ScheduleExceptionCreate(ScheduleExceptionBase):
    pass


class ScheduleExceptionRead(ScheduleExceptionBase):
    id: int
