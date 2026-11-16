from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from pydantic import BaseModel, field_serializer


class SlotRead(BaseModel):
    start: datetime
    end: datetime

    @field_serializer("start", "end")
    def serializer_datetime(self, dt: datetime):
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(ZoneInfo("Europe/Moscow")).isoformat()
