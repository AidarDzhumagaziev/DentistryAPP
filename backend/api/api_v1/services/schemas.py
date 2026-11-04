from decimal import Decimal

from pydantic import BaseModel, Field

from common.enums.enums_db import CabinetType


class ServiceBase(BaseModel):
    name: str = Field(max_length=150)
    specialization_id: int
    description: str
    price_from: Decimal
    duration_min: int
    buffer_min: int
    requires_consultation: bool = False
    cabinet_type: CabinetType


class ServiceCreate(ServiceBase):
    pass


class ServiceRead(ServiceBase):
    id: int
