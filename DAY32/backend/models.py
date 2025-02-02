from .database import Base
from sqlalchemy import Column, Integer, String, DateTime
import datetime

class SecurityLog(Base):
    __tablename__ = "security_logs"

    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String, index=True)  # e.g., "LOGIN_SUCCESS", "FAILED_LOGIN", "SUSPICIOUS_ACTIVITY"
    username = Column(String, index=True)
    ip_address = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    details = Column(String, nullable=True)
