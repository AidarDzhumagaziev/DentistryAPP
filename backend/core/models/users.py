from typing import Optional

from sqlalchemy import ForeignKey, LargeBinary, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship


from .base import Base
from .mixins import TimeStampMixin
from .patients import Patient
from .doctors import Doctor


class User(Base, TimeStampMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(50), nullable=True, unique=True)
    phone: Mapped[str] = mapped_column(String(12), nullable=False, unique=True)
    password_hash: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), nullable=False)
    full_name: Mapped[str] = mapped_column(String(100), nullable=False)
    is_active: Mapped[bool] = mapped_column(
        nullable=False, default=True, server_default="true"
    )
    patient_profile: Mapped["Patient"] = relationship(back_populates="user")
    doctor_profile: Mapped["Doctor"] = relationship(back_populates="user")

    role: Mapped["Role"] = relationship(back_populates="users")


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)

    users: Mapped[list["User"]] = relationship(back_populates="role")
