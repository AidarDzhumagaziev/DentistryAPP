from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    email: EmailStr | None = None
    phone: str = Field(min_length=12, max_length=12)
    full_name: str


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=100)


class UserRead(UserBase):
    pass
