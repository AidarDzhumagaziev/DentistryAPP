from datetime import date

from pydantic import BaseModel


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
