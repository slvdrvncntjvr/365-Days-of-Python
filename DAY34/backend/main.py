from fastapi import FastAPI, WebSocket
from backend.database import engine, Base
from backend.routes import tasks
import asyncio

app = FastAPI(title="Voice-Controlled Task Manager")

Base.metadata.create_all(bind=engine)

app.include_router(tasks.router, prefix="/api")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Received: {data}")  # Log the command
            response = process_voice_command(data)  # Process command
            await websocket.send_text(f"Task Manager: {response}")
    except Exception as e:
        print("WebSocket error:", e)

def process_voice_command(command: str) -> str:
    """ Process voice command into an action """
    command = command.lower()
    if "add task" in command:
        return "Task added successfully."
    elif "remove task" in command:
        return "Task removed."
    elif "show tasks" in command:
        return "Here are your tasks..."
    else:
        return "Sorry, I didn't understand that."
