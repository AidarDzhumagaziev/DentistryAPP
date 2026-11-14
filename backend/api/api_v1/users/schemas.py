from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    email: EmailStr
    phone: str = Field(min_length=12, max_length=12)
    full_name: str


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=100)


class UserRead(UserBase):
    model_config = ConfigDict(strict=True)

    id: int
    is_active: bool = True
    role_id: int


class UserShortRead(BaseModel):
    full_name: str
    phone: str = Field(min_length=12, max_length=12)


class UserAdminCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    phone: str
    full_name: str
    email: EmailStr | None = None
