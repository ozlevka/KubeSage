import os
from kubernetes import client, config

def load_kube_config():
    """Load Kubernetes config (either in-cluster or local)."""
    if "KUBERNETES_SERVICE_HOST" in os.environ:
        config.load_incluster_config()
    else:
        config.load_kube_config()

def debug_k8s():
    """Debug Kubernetes API Connection"""
    try:
        load_kube_config()
        v1 = client.CoreV1Api()
        nodes = v1.list_node()
        return {
            "status": "success",
            "nodes": [node.metadata.name for node in nodes.items], # non JSON output for node names
            "env": dict(os.environ),  # Print env variables
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

def get_nodes():
    """Fetch Kubernetes cluster nodes and return as JSON."""
    try:
        load_kube_config()
        v1 = client.CoreV1Api()
        nodes = v1.list_node()
        return {
            "status": "success",
            "nodes": [{"name": node.metadata.name, "status": node.status.conditions[-1].type} for node in nodes.items]
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

def get_pods():
    """Fetch all Kubernetes pods and return as JSON."""
    try:
        load_kube_config()
        v1 = client.CoreV1Api()
        pods = v1.list_pod_for_all_namespaces()
        return {
            "status": "success",
            "pods": [
                {
                    "name": pod.metadata.name,
                    "namespace": pod.metadata.namespace,
                    "status": pod.status.phase,
                    "node_name": pod.spec.node_name
                } for pod in pods.items
            ]
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

def get_services():
    """Fetch all Kubernetes services and return as JSON."""
    try:
        load_kube_config()
        v1 = client.CoreV1Api()
        services = v1.list_service_for_all_namespaces()
        return {
            "status": "success",
            "services": [
                {
                    "name": svc.metadata.name,
                    "namespace": svc.metadata.namespace,
                    "type": svc.spec.type,
                    "cluster_ip": svc.spec.cluster_ip
                } for svc in services.items
            ]
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

def get_deployments():
    """Fetch all Kubernetes deployments and return as JSON."""
    try:
        load_kube_config()
        apps_v1 = client.AppsV1Api()
        deployments = apps_v1.list_deployment_for_all_namespaces()
        return {
            "status": "success",
            "deployments": [
                {
                    "name": dep.metadata.name,
                    "namespace": dep.metadata.namespace,
                    "replicas": dep.spec.replicas,
                    "available_replicas": dep.status.available_replicas
                } for dep in deployments.items
            ]
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}