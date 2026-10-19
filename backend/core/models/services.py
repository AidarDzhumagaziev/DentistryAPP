from typing import TYPE_CHECKING

from decimal import Decimal

from sqlalchemy import CheckConstraint, ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from common.enums.enums_db import CabinetType, _cabinet_type_values

from .base import Base
from .mixins import TimeStampMixin

if TYPE_CHECKING:
    from .appointments import Appointment


class Service(Base, TimeStampMixin):
    __tablename__ = "services"
    __table_args__ = (
        CheckConstraint("duration_min > 0"),
        CheckConstraint("buffer_min >= 0"),
        CheckConstraint(f"cabinet_type IN ({_cabinet_type_values})"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    specialization_id: Mapped[int] = mapped_column(
        ForeignKey("specializations.id", ondelete="RESTRICT"), nullable=False
    )
    description: Mapped[str] = mapped_column(Text, nullable=False)
    price_from: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    duration_min: Mapped[int] = mapped_column(nullable=False)
    buffer_min: Mapped[int] = mapped_column(nullable=False)
    requires_consultation: Mapped[bool] = mapped_column(
        nullable=False, default=False, server_default="false"
    )
    cabinet_type: Mapped[CabinetType] = mapped_column(String(50), nullable=False)

    appointments: Mapped["Appointment"] = relationship(back_populates="service")
