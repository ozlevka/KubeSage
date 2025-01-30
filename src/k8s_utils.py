import os
from kubernetes import client, config

def load_kube_config():
    """Load Kubernetes config (either in-cluster or local)."""
    if "KUBERNETES_SERVICE_HOST" in os.environ:
        config.load_incluster_config()
    else:
        config.load_kube_config()

def check_cluster_health():
    """Check Kubernetes cluster health."""
    try:
        load_kube_config()
        v1 = client.CoreV1Api()
        nodes = v1.list_node()
        return {"status": "success", "nodes": [node.metadata.name for node in nodes.items]}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def get_pods():
    """Fetch all Kubernetes pods in the cluster."""
    try:
        load_kube_config()
        v1 = client.CoreV1Api()
        pods = v1.list_pod_for_all_namespaces()
        return [{"name": pod.metadata.name, "namespace": pod.metadata.namespace, "status": pod.status.phase} for pod in pods.items]
    except Exception as e:
        return {"error": str(e)}

def get_services():
    """Fetch all Kubernetes services."""
    try:
        load_kube_config()
        v1 = client.CoreV1Api()
        services = v1.list_service_for_all_namespaces()
        return [{"name": svc.metadata.name, "namespace": svc.metadata.namespace} for svc in services.items]
    except Exception as e:
        return {"error": str(e)}

def get_deployments():
    """Fetch all Kubernetes deployments."""
    try:
        load_kube_config()
        apps_v1 = client.AppsV1Api()
        deployments = apps_v1.list_deployment_for_all_namespaces()
        return [{"name": dep.metadata.name, "namespace": dep.metadata.namespace} for dep in deployments.items]
    except Exception as e:
        return {"error": str(e)}