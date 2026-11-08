from datetime import datetime

from pydantic import BaseModel


class SlotRead(BaseModel):
    start: datetime
    end: datetime
