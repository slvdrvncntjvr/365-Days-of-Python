from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database import get_db
from backend import crud, schemas

router = APIRouter(prefix="/logs", tags=["Security Logs"])

@router.post("/", response_model=schemas.LogResponse)
def log_event(log: schemas.LogCreate, db: Session = Depends(get_db)):
    return crud.create_log(db, log)

@router.get("/", response_model=list[schemas.LogResponse])
def get_all_logs(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_logs(db, skip=skip, limit=limit)
