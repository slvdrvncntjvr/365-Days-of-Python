from sqlalchemy.orm import Session
from . import models, schemas

def create_threat_log(db: Session, log: schemas.ThreatLogCreate):
    db_log = models.ThreatLog(**log.model_dump())
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

def get_threat_logs(db: Session, limit: int = 10):
    return db.query(models.ThreatLog).order_by(models.ThreatLog.timestamp.desc()).limit(limit).all()
