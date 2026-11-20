from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    field_validator,
    model_validator,
)


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


class UserProfileRead(BaseModel):
    full_name: str
    phone: str = Field(min_length=12, max_length=12)
    email: EmailStr


class UserAdminCreate(UserBase):
    full_name: str
    phone: str = Field(min_length=12, max_length=12)
    email: EmailStr


class PasswordChange(BaseModel):
    current_password: str = Field(min_length=8, max_length=128)
    new_password: str = Field(min_length=8, max_length=128)
    confirm_password: str = Field(min_length=8, max_length=128)

    @model_validator(mode="after")
    def passwords_match(self):
        if self.new_password != self.confirm_password:
            raise ValueError("new_password and confirm_password do not match")
        if self.current_password == self.new_password:
            raise ValueError("new_password must differ from current_password")
        return self
