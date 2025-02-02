from sqlalchemy import Column, Integer, String, DateTime
from .database import Base
from datetime import datetime

class ThreatLog(Base):
    __tablename__ = "threat_logs"

    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String, index=True)
    source_ip = Column(String)
    details = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
