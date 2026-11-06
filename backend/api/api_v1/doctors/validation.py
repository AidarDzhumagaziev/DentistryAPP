from core.models import Doctor

from api.api_v1.specializations.schemas import SpecializationRead
from api.api_v1.users.schemas import UserRead

from .schemas import DoctorRead


def validation_doctor(doctor: Doctor) -> DoctorRead:
    doctor_read = DoctorRead(
        user_id=doctor.user_id,
        experience_years=doctor.experience_years,
        bio=doctor.bio,
        photo_url=doctor.photo_url,
        is_active=doctor.is_active,
        user=UserRead(
            phone=doctor.user.phone,
            full_name=doctor.user.full_name,
            id=doctor.user.id,
            role_id=doctor.user.role_id,
        ),
        specializations=[
            SpecializationRead(id=spec.specialization.id, name=spec.specialization.name)
            for spec in doctor.specializations
        ],
    )
    return doctor_read
