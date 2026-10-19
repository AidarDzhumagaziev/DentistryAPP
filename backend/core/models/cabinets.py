from sqlalchemy import CheckConstraint, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.common.enums.enums_db import CabinetType, _cabinet_type_values
from base import Base


class Cabinet(Base):
    __tablename__ = "cabinets"
    __table_args__ = (CheckConstraint(f"type IN ({_cabinet_type_values})"),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    number: Mapped[int] = mapped_column(nullable=False)
    type: Mapped[CabinetType] = mapped_column(String(50), nullable=False)
