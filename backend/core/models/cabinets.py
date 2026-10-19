from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.common.enums.enums_db import CabinetType, _cabinet_type_values
from base import Base

if TYPE_CHECKING:
    from schedules import WorkSchedule
    from appointments import Appointment


class Cabinet(Base):
    __tablename__ = "cabinets"
    __table_args__ = (CheckConstraint(f"type IN ({_cabinet_type_values})"),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    number: Mapped[int] = mapped_column(nullable=False)
    type: Mapped[CabinetType] = mapped_column(String(50), nullable=False)

    work_schedules: Mapped[list["WorkSchedule"]] = relationship(
        back_populates="cabinet"
    )

    appointments: Mapped["Appointment"] = relationship(back_populates="cabinet")
