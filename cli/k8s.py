from kubernetes import client, config

def get_cluster_health():
    """Fetch cluster nodes and their status."""
    try:
        config.load_kube_config()  # Load kubeconfig from default location
        v1 = client.CoreV1Api()
        nodes = v1.list_node()
        for node in nodes.items:
            print(f"Node: {node.metadata.name}, Status: {node.status.conditions[-1].type}")
    except Exception as e:
        print(f"Error accessing Kubernetes API: {e}")