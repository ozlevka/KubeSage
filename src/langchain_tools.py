from langchain.tools import Tool
from src.k8s_utils import get_nodes, get_pods, get_services, get_deployments

# Tool for fetching cluster nodes
nodes_tool = Tool(
    name="Get Kubernetes Nodes",
    description="Fetches all Kubernetes nodes and their status.",
    func=lambda _: get_nodes()
)

# Tool for fetching pods
pods_tool = Tool(
    name="Get Kubernetes Pods",
    description="Fetches all Kubernetes pods, including their namespace, status, and assigned node.",
    func=lambda _: get_pods()
)

# Tool for fetching services
services_tool = Tool(
    name="Get Kubernetes Services",
    description="Fetches all Kubernetes services, including their type and cluster IP.",
    func=lambda _: get_services()
)

# Tool for fetching deployments
deployments_tool = Tool(
    name="Get Kubernetes Deployments",
    description="Fetches all Kubernetes deployments, including replica count and available replicas.",
    func=lambda _: get_deployments()
)

# List of all tools for easy import
k8s_tools = [nodes_tool, pods_tool, services_tool, deployments_tool]