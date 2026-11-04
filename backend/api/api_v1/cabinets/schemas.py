from pydantic import BaseModel

from common.enums.enums_db import CabinetType


class CabinetBase(BaseModel):
    number: int
    type: CabinetType


class CabinetCreate(CabinetBase):
    pass


class CabinetRead(CabinetBase):
    id: int
