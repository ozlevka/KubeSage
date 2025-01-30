from fastapi import FastAPI, WebSocket
from src.websocket_handler import websocket_handler

app = FastAPI()

# WebSocket for Live Chat with `kubectl`
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket_handler(websocket)