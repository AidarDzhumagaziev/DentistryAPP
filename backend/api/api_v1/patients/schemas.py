from datetime import date

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from api.api_v1.users.schemas import UserShortRead


class PatientBase(BaseModel):
    user_id: int
    birth_date: date
    allergies: str
    chronic_diseas: str
    no_show_count: int = 0
    notes: str | None = None


class PatientCreate(PatientBase):
    pass


class PatientRead(PatientBase):
    pass


class PatientUpdate(BaseModel):
    birth_date: date
    allergies: str
    chronic_diseas: str
    no_show_count: int = 0
    notes: str | None = None


class PatientUpdatePartial(PatientUpdate):
    birth_date: date | None = None  # type: ignore[assignment]
    allergies: str | None = None  # type: ignore[assignment]
    chronic_diseas: str | None = None  # type: ignore[assignment]
    no_show_count: int | None = None  # type: ignore[assignment]


class PatientShortRead(BaseModel):
    birth_date: date
    allergies: str
    chronic_diseas: str
    user: UserShortRead
