from pydantic import BaseModel
from datetime import datetime

class ThreatLogBase(BaseModel):
    event_type: str
    source_ip: str
    details: str

class ThreatLogCreate(ThreatLogBase):
    pass

class ThreatLogResponse(ThreatLogBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True
