import os
from kubernetes import client, config

def load_kube_config():
    """Load Kubernetes configuration (In-Cluster or Local)."""
    if "KUBERNETES_SERVICE_HOST" in os.environ:
        config.load_incluster_config()
    else:
        config.load_kube_config()

def get_all_pods_with_usage():
    """Fetches pod details including status, node, CPU/memory usage."""
    try:
        load_kube_config()
        v1 = client.CoreV1Api()
        custom_api = client.CustomObjectsApi()

        pods = v1.list_pod_for_all_namespaces().items
        metrics = custom_api.list_cluster_custom_object("metrics.k8s.io", "v1beta1", "pods")

        pod_usage_map = {}
        for pod in metrics.get("items", []):
            pod_name = pod.get("metadata", {}).get("name")
            if pod_name and "containers" in pod:
                container = pod["containers"][0] if pod["containers"] else {}
                pod_usage_map[pod_name] = {
                    "cpu": container.get("usage", {}).get("cpu", "N/A"),
                    "memory": container.get("usage", {}).get("memory", "N/A"),
                }

        return {
            "status": "success",
            "pods": [
                {
                    "name": pod.metadata.name,
                    "namespace": pod.metadata.namespace,
                    "status": pod.status.phase if pod.status else "Unknown",
                    "node": pod.spec.node_name if pod.spec else "Unknown",
                    "cpu": pod_usage_map.get(pod.metadata.name, {}).get("cpu", "N/A"),
                    "memory": pod_usage_map.get(pod.metadata.name, {}).get("memory", "N/A"),
                }
                for pod in pods
            ]
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

def get_all_services():
    """Fetches all services with their types and ports."""
    try:
        load_kube_config()
        v1 = client.CoreV1Api()
        services = v1.list_service_for_all_namespaces().items

        return {
            "status": "success",
            "services": [
                {
                    "name": svc.metadata.name,
                    "namespace": svc.metadata.namespace,
                    "type": svc.spec.type if svc.spec else "Unknown",
                    "ports": [{"port": p.port, "protocol": p.protocol} for p in (svc.spec.ports or [])]
                }
                for svc in services
            ]
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

def get_all_deployments():
    """Fetches all deployments with their replica status."""
    try:
        load_kube_config()
        apps_v1 = client.AppsV1Api()
        deployments = apps_v1.list_deployment_for_all_namespaces().items

        return {
            "status": "success",
            "deployments": [
                {
                    "name": dep.metadata.name,
                    "namespace": dep.metadata.namespace,
                    "replicas": dep.status.replicas if dep.status else 0,
                    "available_replicas": dep.status.available_replicas if dep.status else 0
                }
                for dep in deployments
            ]
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

def get_all_nodes():
    """Fetches all nodes with their health conditions and resource capacity."""
    try:
        load_kube_config()
        v1 = client.CoreV1Api()
        nodes = v1.list_node().items

        return {
            "status": "success",
            "nodes": [
                {
                    "name": node.metadata.name,
                    "status": node.status.conditions[-1].type if node.status.conditions else "Unknown",
                    "capacity": node.status.capacity if node.status else {}
                }
                for node in nodes
            ]
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

def get_all_endpoints():
    """Fetches all endpoints and their associated services."""
    try:
        load_kube_config()
        v1 = client.CoreV1Api()
        endpoints = v1.list_endpoints_for_all_namespaces().items

        endpoint_data = []
        for ep in endpoints:
            if not ep.subsets:
                continue
            for subset in ep.subsets:
                addresses = [addr.ip for addr in subset.addresses] if subset.addresses else []
                ports = [p.port for p in subset.ports] if subset.ports else []
                endpoint_data.append({
                    "name": ep.metadata.name,
                    "namespace": ep.metadata.namespace,
                    "addresses": addresses,
                    "ports": ports
                })

        return {"status": "success", "endpoints": endpoint_data}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def get_cluster_events():
    """Fetches recent cluster-wide events."""
    try:
        load_kube_config()
        v1 = client.CoreV1Api()
        events = v1.list_event_for_all_namespaces().items

        return {
            "status": "success",
            "events": [
                {"type": event.type, "message": event.message, "involved_object": event.involved_object.kind if event.involved_object else "Unknown"}
                for event in events[-10:]  # Last 10 events safely
            ]
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

def get_all_namespaces():
    """Fetches all namespaces with their statuses."""
    try:
        load_kube_config()
        v1 = client.CoreV1Api()
        namespaces = v1.list_namespace().items

        return {
            "status": "success",
            "namespaces": [
                {"name": ns.metadata.name, "status": ns.status.phase if ns.status else "Unknown"} for ns in namespaces
            ]
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}