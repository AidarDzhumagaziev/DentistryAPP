from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class UserBase(BaseModel):
    email: EmailStr
    phone: str = Field(min_length=12, max_length=12)
    full_name: str

    @field_validator("email", mode="before")
    @classmethod
    def normalize_email(cls, v: str) -> str:
        if isinstance(v, str):
            return v.strip().lower()
        return v


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=100)


class UserRead(UserBase):
    model_config = ConfigDict(strict=True)

    id: int
    is_active: bool = True
    role: str


class UserShortRead(BaseModel):
    full_name: str
    phone: str = Field(min_length=12, max_length=12)


class UserAdminCreate(UserBase):
    full_name: str
    phone: str = Field(min_length=12, max_length=12)
    email: EmailStr
