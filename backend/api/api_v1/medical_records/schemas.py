from pydantic import BaseModel


class MedicalRecordBase(BaseModel):
    complaints: str | None
    objective_findings: str | None
    diagnosis: str | None
    treatment_plan: str | None


class MedicalRecordCreate(MedicalRecordBase):
    appointment_id: int


class MedicalRecordRead(MedicalRecordBase):
    id: int
