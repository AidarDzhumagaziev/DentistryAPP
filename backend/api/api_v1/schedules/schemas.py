from datetime import time

from pydantic import BaseModel, Field, model_validator


class WorkScheduleBase(BaseModel):
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
