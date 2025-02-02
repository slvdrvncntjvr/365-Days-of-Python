from fastapi import WebSocket, WebSocketDisconnect
from typing import List
import json

active_connections: List[WebSocket] = []

async def connect_websocket(ws: WebSocket):
    await ws.accept()
    active_connections.append(ws)

async def broadcast_log(log):
    message = json.dumps({
        "event_type": log.event_type,
        "source_ip": log.source_ip,
        "details": log.details,
        "timestamp": str(log.timestamp)
    })
    for ws in active_connections:
        await ws.send_text(message)
