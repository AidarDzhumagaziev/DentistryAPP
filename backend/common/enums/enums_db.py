from enum import Enum


class CabinetType(str, Enum):
    GENERAL = "general"
    SURGICAL = "surgical"
    ROENTGEN = "roentgen"


_cabinet_type_values = ", ".join(f"'{c.value}'" for c in CabinetType)


class ReasonType(str, Enum):
    VACATION = "vacation"
    SICK_DAY = "sick_day"


_reason_type_values = ", ".join(f"'{r.value}'" for r in ReasonType)


class AppointmentStatus(str, Enum):
    SCHEDULED = "scheduled"
    CONFIRMED = "confirmed"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    NO_SHOW = "no_show"


_appointment_status_values = ", ".join(f"'{s.value}'" for s in AppointmentStatus)


class RoleType(str, Enum):
    PATIENT = "patient"
    DOCTOR = "doctor"
    ADMIN = "admin"
