from fastapi import FastAPI, WebSocket
from backend.database import engine, Base
from backend.routes import tasks

app = FastAPI(title="Voice-Controlled Task Manager")

Base.metadata.create_all(bind=engine)

app.include_router(tasks.router, prefix="/api")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message received: {data}")
    except WebSocketDisconnect:
        print("WebSocket client disconnected") 

