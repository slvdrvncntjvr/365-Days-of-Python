from fastapi import FastAPI
from backend.database import engine
from backend import models
from backend.routers import logs

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="CyberSec Logger", description="A simple security event logger API")

app.include_router(logs.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the CyberSec Logger API"}
