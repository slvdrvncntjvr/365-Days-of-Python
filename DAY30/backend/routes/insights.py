from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from backend.database import get_db
from backend.models import Task

router = APIRouter()

@router.get("/insights/")
def get_task_insights(db: Session = Depends(get_db)):
    completed_tasks = db.query(Task).filter(Task.completed == True).count()
    pending_tasks = db.query(Task).filter(Task.completed == False).count()

    completion_times = [
        (task.completed_at - task.created_at).total_seconds() / 3600
        for task in db.query(Task).filter(Task.completed == True)
        if task.completed_at and task.created_at
    ]

    average_completion_time = sum(completion_times) / len(completion_times) if completion_times else 0

    return {
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks,
        "average_completion_time": round(average_completion_time, 2),
    }
