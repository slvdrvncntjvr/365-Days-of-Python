from backend.database import Base
from sqlalchemy import Column, Integer, String

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, index=True)
    status = Column(String, default="pending")
