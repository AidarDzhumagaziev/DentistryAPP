from pydantic import BaseModel


class MedicalRecordBase(BaseModel):
    appointment_id: int
    complaints: str | None
    objective_findings: str | None
    diagnosis: str | None
    treatment_plan: str | None


class MedicalRecordCreate(MedicalRecordBase):
    pass


class MedicalRecordRead(MedicalRecordBase):
    pass
