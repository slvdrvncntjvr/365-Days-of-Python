from sqlalchemy.orm import Session
from . import models, schemas

def create_log(db: Session, log: schemas.LogCreate):
    db_log = models.SecurityLog(**log.model_dump())
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

def get_logs(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.SecurityLog).offset(skip).limit(limit).all()
