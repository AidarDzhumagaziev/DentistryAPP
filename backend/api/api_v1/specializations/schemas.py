from pydantic import BaseModel, Field


class SpecializationBase(BaseModel):
    name: str = Field(max_length=50)


class SpecializationCreate(SpecializationBase):
    pass


class SpecializationRead(SpecializationBase):
    id: int
