from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
from .database import engine, Base
from .routes import events
from . import websocket


app = FastAPI(title="Cyber Threat Monitor API")

Base.metadata.create_all(bind=engine)  

app.include_router(events.router, prefix="/api")

app.mount("/", StaticFiles(directory="backend/static", html=True), name="static")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message received: {data}")


