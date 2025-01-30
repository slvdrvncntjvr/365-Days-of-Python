from fastapi import FastAPI
from backend.routes.tasks import router as tasks_router
from backend.routes.insights import router as insights_router
from backend.database import engine, Base

app = FastAPI(title="PyProd AI - Productivity Assistant")

# Include routers
app.include_router(tasks_router, prefix="/tasks", tags=["Tasks"])
app.include_router(insights_router, prefix="/insights", tags=["Insights"])

Base.metadata.create_all(bind=engine)  # Ensures database tables are created

@app.get("/")
def home():
    return {"message": "Welcome to PyProd AI"}
