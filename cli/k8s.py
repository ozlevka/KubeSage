from kubernetes import client, config
import os

def get_cluster_health():
    """Fetch cluster nodes and their status."""
    try:
        # Detect if running inside a Kubernetes pod
        if "KUBERNETES_SERVICE_HOST" in os.environ:
            print("Running inside a Kubernetes pod. Using in-cluster authentication.")
            config.load_incluster_config()
        else:
            print("Running locally. Using kubeconfig file.")
            config.load_kube_config()  # Load kubeconfig from default location

        v1 = client.CoreV1Api()
        nodes = v1.list_node()
        for node in nodes.items:
            status_condition = next(
                (condition for condition in node.status.conditions if condition.type == "Ready"), None
            )
            status = status_condition.status if status_condition else "Unknown"
            print(f"Node: {node.metadata.name}, Status: {status}")

    except Exception as e:
        print(f"Error accessing Kubernetes API: {e}")