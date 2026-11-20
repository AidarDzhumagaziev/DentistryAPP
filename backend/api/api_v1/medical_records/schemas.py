from pydantic import BaseModel


class MedicalRecordBase(BaseModel):
    complaints: str | None
    objective_findings: str | None
    diagnosis: str | None
    treatment_plan: str | None


class MedicalRecordCreate(MedicalRecordBase):
    pass


class MedicalRecordRead(MedicalRecordBase):
    id: int


class MedicalRecordUpdatePartial(MedicalRecordBase):
    complaints: str | None = None
    objective_findings: str | None = None
    diagnosis: str | None = None
    treatment_plan: str | None = None
