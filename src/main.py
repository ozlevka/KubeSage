from fastapi import FastAPI, WebSocket
from src.k8s_utils import debug_k8s
from src.websocket_handler import websocket_handler

app = FastAPI()

# Kubernetes API Debug
@app.get("/debug")
def debug_endpoint():
    return debug_k8s()

# WebSocket for Live Chat with `kubectl`
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket_handler(websocket)