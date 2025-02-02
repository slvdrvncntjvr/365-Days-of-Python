from pydantic import BaseModel
import datetime

class LogCreate(BaseModel):
    event_type: str
    username: str
    ip_address: str
    details: str | None = None

class LogResponse(LogCreate):
    id: int
    timestamp: datetime.datetime

    class Config:
        from_attributes = True
