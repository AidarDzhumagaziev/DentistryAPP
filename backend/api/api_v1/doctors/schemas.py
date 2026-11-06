from pydantic import BaseModel, ConfigDict, Field


class DoctorBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: int
    experience_years: int = Field(gt=0)
    bio: str
    photo_url: str
    is_active: bool = True


class DoctorCreate(DoctorBase):
    pass


class DoctorRead(DoctorBase):
    pass
