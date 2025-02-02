from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import database, schemas, crud, websocket

router = APIRouter()

@router.post("/log/", response_model=schemas.ThreatLogResponse)
def log_threat(log: schemas.ThreatLogCreate, db: Session = Depends(database.get_db)):
    new_log = crud.create_threat_log(db, log)
    websocket.broadcast_log(new_log)  # Send real-time update
    return new_log

@router.get("/logs/", response_model=list[schemas.ThreatLogResponse])
def get_logs(db: Session = Depends(database.get_db), limit: int = 10):
    return crud.get_threat_logs(db, limit)
