from decimal import Decimal

from pydantic import BaseModel, Field

from common.enums.enums_db import CabinetType


class ServiceBase(BaseModel):
    name: str = Field(max_length=150)
    specialization_id: int = Field(gt=0)
    description: str
    price_from: Decimal = Field(ge=0, decimal_places=2)
    duration_min: int
    buffer_min: int = Field(ge=0, le=60, default=15)
    requires_consultation: bool = False
    cabinet_type: CabinetType


class ServiceCreate(ServiceBase):
    pass


class ServiceRead(ServiceBase):
    id: int


class ServiceUpdate(ServiceCreate):
    pass


class ServiceUpdatePartial(ServiceCreate):
    name: str | None = None  # type: ignore[assignment]
    specialization_id: int | None = None  # type: ignore[assignment]
    description: str | None = None  # type: ignore[assignment]
    price_from: Decimal | None = None  # type: ignore[assignment]
    duration_min: int | None = None  # type: ignore[assignment]
    buffer_min: int | None = None  # type: ignore[assignment]
    requires_consultation: bool | None = None  # type: ignore[assignment]
    cabinet_type: CabinetType | None = None  # type: ignore[assignment]
