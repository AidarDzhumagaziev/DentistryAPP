from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, declared_attr, mapped_column


class TimeStampMixin:
    """Для сущностей, которые могут изменяться после создания"""

    @declared_attr
    def created_at(cls) -> Mapped[datetime]:
        return mapped_column(DateTime, server_default=func.now())

    @declared_attr
    def updated_at(cls) -> Mapped[datetime]:
        return mapped_column(DateTime, server_default=func.now(), onupdate=func.now())


class CreatedAtMixin:
    """Для append-only сущностей, которые не будут меняться после создания"""

    @declared_attr
    def created_at(cls) -> Mapped[datetime]:
        return mapped_column(DateTime, server_default=func.now())
