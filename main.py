from fastapi import FastAPI, WebSocket
import os
from kubernetes import client, config

app = FastAPI()

# Load Kubernetes Configuration (In-Cluster or Local)
def load_kube_config():
    if "KUBERNETES_SERVICE_HOST" in os.environ:
        config.load_incluster_config()
    else:
        config.load_kube_config()


# Kubernetes Health Check API
@app.get("/health")
def check_cluster_health():
    """Check Kubernetes cluster health."""
    try:
        load_kube_config()
        v1 = client.CoreV1Api()
        nodes = v1.list_node()
        return {"status": "success", "nodes": [node.metadata.name for node in nodes.items]}
    except Exception as e:
        return {"status": "error", "message": str(e)}


# ✅ Get List of Pods
@app.get("/pods")
def get_pods():
    """Fetch all Kubernetes pods in the cluster."""
    try:
        v1 = client.CoreV1Api()
        pods = v1.list_pod_for_all_namespaces()
        return {"pods": [{"name": pod.metadata.name, "namespace": pod.metadata.namespace, "status": pod.status.phase} for pod in pods.items]}
    except Exception as e:
        return {"error": str(e)}

# ✅ Get List of Services
@app.get("/services")
def get_services():
    """Fetch all Kubernetes services."""
    try:
        v1 = client.CoreV1Api()
        services = v1.list_service_for_all_namespaces()
        return {"services": [{"name": svc.metadata.name, "namespace": svc.metadata.namespace} for svc in services.items]}
    except Exception as e:
        return {"error": str(e)}

# ✅ Get List of Deployments
@app.get("/deployments")
def get_deployments():
    """Fetch all Kubernetes deployments."""
    try:
        apps_v1 = client.AppsV1Api()
        deployments = apps_v1.list_deployment_for_all_namespaces()
        return {"deployments": [{"name": dep.metadata.name, "namespace": dep.metadata.namespace} for dep in deployments.items]}
    except Exception as e:
        return {"error": str(e)}


# WebSocket for Live Chat with `kubectl`
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket for running live kubectl commands."""
    await websocket.accept()
    await websocket.send_text("🔹 Live Kubernetes Chat Started! Type 'exit' to close.")

    load_kube_config()  # Load config once for efficiency
    v1 = client.CoreV1Api()
    apps_v1 = client.AppsV1Api()

    while True:
        cmd = await websocket.receive_text()
        if cmd.lower() == "exit":
            await websocket.send_text("❌ Closing connection.")
            break

        if cmd.lower() == "get pods":
            pods = v1.list_pod_for_all_namespaces()
            response = "\n".join([f"Pod: {pod.metadata.name} (Status: {pod.status.phase})" for pod in pods.items])
        elif cmd.lower() == "get services":
            services = v1.list_service_for_all_namespaces()
            response = "\n".join([f"Service: {svc.metadata.name}" for svc in services.items])
        elif cmd.lower() == "get deployments":
            deployments = apps_v1.list_deployment_for_all_namespaces()
            response = "\n".join([f"Deployment: {dep.metadata.name}" for dep in deployments.items])
        else:
            response = "❌ Invalid command. Try 'get pods', 'get services', or 'get deployments'."

        await websocket.send_text(response)

    await websocket.close()