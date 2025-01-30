from fastapi import FastAPI, WebSocket
from k8s_utils import check_cluster_health, get_pods, get_services, get_deployments

app = FastAPI()

# Kubernetes Health Check API
@app.get("/health")
def health():
    return check_cluster_health()

# Get List of Pods
@app.get("/pods")
def pods():
    return {"pods": get_pods()}

# Get List of Services
@app.get("/services")
def services():
    return {"services": get_services()}

# Get List of Deployments
@app.get("/deployments")
def deployments():
    return {"deployments": get_deployments()}

# WebSocket for Live Chat with `kubectl`
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket for running live Kubernetes queries."""
    await websocket.accept()
    await websocket.send_text("🔹 Live Kubernetes Chat Started! Type 'exit' to close.")

    while True:
        cmd = await websocket.receive_text()
        if cmd.lower() == "exit":
            await websocket.send_text("❌ Closing connection.")
            break

        if cmd.lower() == "get pods":
            response = "\n".join([f"Pod: {p['name']} (Status: {p['status']})" for p in get_pods()])
        elif cmd.lower() == "get services":
            response = "\n".join([f"Service: {s['name']}" for s in get_services()])
        elif cmd.lower() == "get deployments":
            response = "\n".join([f"Deployment: {d['name']}" for d in get_deployments()])
        else:
            response = "❌ Invalid command. Try 'get pods', 'get services', or 'get deployments'."

        await websocket.send_text(response)

    await websocket.close()