from pydantic import BaseModel, ConfigDict, Field

from api.api_v1.specializations.schemas import SpecializationRead
from api.api_v1.users.schemas import UserRead


class DoctorBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: int
    experience_years: int = Field(gt=0)
    bio: str
    photo_url: str
    is_active: bool = True


class DoctorCreate(DoctorBase):
    specializations_ids: list[int] = Field(min_length=1)


class DoctorRead(DoctorBase):
    user: UserRead
    specializations: list[SpecializationRead]
