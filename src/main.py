from fastapi import FastAPI, WebSocket
from src.websocket_handler import websocket_handler
from src.rest_api_handler import (
    process_kubernetes_query, 
    health_check,
    QueryRequest,
    QueryResponse
)

app = FastAPI(
    title="KubeSage API",
    description="AI-powered Kubernetes troubleshooting assistant with WebSocket and REST API support",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Health check endpoint
@app.get("/", response_model=dict)
async def root():
    """Root endpoint with health check."""
    return health_check()

@app.get("/health", response_model=dict)
async def health():
    """Health check endpoint."""
    return health_check()

# REST API endpoints
@app.post("/api/query", response_model=QueryResponse)
async def query_kubernetes(request: QueryRequest):
    """Process a Kubernetes query using natural language."""
    return process_kubernetes_query(request)

# WebSocket for Live Chat with `kubectl`
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket_handler(websocket)