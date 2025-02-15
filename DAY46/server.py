import asyncio
import websockets
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.staticfiles import StaticFiles
import uvicorn
import json

app = FastAPI(title="Real-Time Witty Poll")

poll_options = {
    "Pizza": 0,
    "Burger": 0,
    "Sushi": 0,
    "Pasta": 0
}

respp = {
    "Pizza": "pine apple?",
    "Burger": "borgar",
    "Sushi": "japaniz",
    "Pasta": "italiani"
}

def get_poll_results():
    total_votes = sum(poll_options.values())
    results = []
    for option, count in poll_options.items():
        percentage = (count / total_votes * 100) if total_votes > 0 else 0
        response = respp.get(option, "")
        results.append(f"{option}: {count} votes ({percentage:.1f}%) - {response}")
    return "\n".join(results)

class ConnectionManager:
    def __init__(self):
        self.active_connections = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.post("/vote")
async def vote(request: Request):
    data = await request.json()
    option = data.get("option")
    if option in poll_options:
        poll_options[option] += 1
    await manager.broadcast(get_poll_results())
    return {"message": "Vote recorded", "results": poll_options}

@app.get("/poll")
async def poll():
    return poll_options

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await asyncio.sleep(0.1)
    except WebSocketDisconnect:
        manager.disconnect(websocket)

app.mount("/", StaticFiles(directory=".", html=True), name="static")

if __name__ == "__main__":
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)
