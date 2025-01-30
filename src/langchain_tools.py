import json

from langchain.tools import Tool
from src.k8s_utils import (
    get_all_pods_with_usage, get_all_services, get_all_deployments,
    get_all_nodes, get_all_endpoints, get_cluster_events, get_all_namespaces
)
from src.k8s_depth_utils import (
    describe_pod_with_restart_count, get_pod_logs, describe_service,
    describe_deployment, get_node_status_and_capacity, get_rbac_events_and_role_bindings,
    get_persistent_volumes_and_claims, get_running_jobs_and_cronjobs, get_ingress_resources, check_pod_affinity
)

# Broad Insights Tools
broad_insights_tools = [
    Tool(
        name="Get All Pods with Resource Usage",
        description="Fetches pod details including status, node, CPU/memory usage.",
        func=lambda _: get_all_pods_with_usage(),
    ),
    Tool(
        name="Get All Services",
        description="Lists all services with types and ports.",
        func=lambda _: get_all_services(),
    ),
    Tool(
        name="Get All Deployments",
        description="Lists deployments with replica status.",
        func=lambda _: get_all_deployments(),
    ),
    Tool(
        name="Get All Nodes",
        description="Lists nodes with health conditions & capacity.",
        func=lambda _: get_all_nodes(),
    ),
    Tool(
        name="Get All Endpoints",
        description="Fetches endpoints and associated services.",
        func=lambda _: get_all_endpoints(),
    ),
    Tool(
        name="Get Cluster Events",
        description="Lists recent cluster-wide warnings & failures.",
        func=lambda _: get_cluster_events(),
    ),
    Tool(
        name="Get Namespace List",
        description="Lists all namespaces and their statuses.",
        func=lambda _: get_all_namespaces(),
    ),
]

# Utility function to safely parse JSON inputs
def parse_params(params):
    """Parses input parameters safely and ensures correct function arguments."""
    print(f"Unparsed Params: {params}") # Debugging Output
    if isinstance(params, dict):
        # print(f"✅ Parsed Params (Already Dict): {params}")  # Debugging Output
        return params  # Already a dictionary, return as is

    try:
        parsed = json.loads(params)  # Convert JSON string to dictionary
        if not isinstance(parsed, dict):
            raise ValueError("Parsed parameters must be a dictionary.")

        # print(f"✅ Parsed Params (From JSON): {parsed}")  # Debugging Output
        return parsed
    except json.JSONDecodeError:
        raise ValueError("Invalid parameter format. Please provide a valid JSON.")



# Deep Dive Tools with Fixed Parameter Parsing
deep_dive_tools = [
    Tool(
        name="Describe Pod with Restart Count",
        description="Fetches detailed pod info + restart count. (pass input as valid JSON)",
        func=lambda params: describe_pod_with_restart_count(
            *parse_params(params)
        ),
    ),
    Tool(
        name="Get Pod Logs",
        description="Fetches the last 10 log lines for a specific pod. (pass input as valid JSON)",
        func=lambda params: get_pod_logs(
            *parse_params(params)
        ),
    ),
    Tool(
        name="Describe Service",
        description="Fetches detailed information about a specific service. (pass input as valid JSON)",
        func=lambda params: describe_service(
            *parse_params(params)
        ),
    ),
    Tool(
        name="Describe Deployment",
        description="Fetches deployment details including replica count and container images. Takes namespace and deployment_name as inputs (pass input as valid JSON)",
        func=lambda params: describe_deployment(
            *parse_params(params)
        ),
    ),
    Tool(
        name="Get Node Status & Capacity",
        description="Fetches node health conditions and resource pressure. (pass input as valid JSON)",
        func=lambda params: get_node_status_and_capacity(
            *parse_params(params)
        ),
    ),
    Tool(
        name="Check RBAC Events & Role Bindings",
        description="Fetches RBAC events, RoleBindings, and ClusterRoleBindings.",
        func=lambda _: get_rbac_events_and_role_bindings(),  # No parameters needed
    ),
    Tool(
        name="Get Persistent Volumes & Claims",
        description="Lists all Persistent Volumes (PVs) and Persistent Volume Claims (PVCs).",
        func=lambda _: get_persistent_volumes_and_claims(),  # No parameters needed
    ),
    Tool(
        name="Get Running Jobs & CronJobs",
        description="Lists all active Jobs and CronJobs.",
        func=lambda _: get_running_jobs_and_cronjobs(),  # No parameters needed
    ),
    Tool(
        name="Get Ingress Resources & Annotations",
        description="Fetches all Ingress resources, their rules, hosts, and annotations.",
        func=lambda _: get_ingress_resources(),  # No parameters needed
    ),
    Tool(
        name="Check Pod Affinity & Anti-Affinity",
        description="Analyzes the affinity and anti-affinity rules for a specific pod. (pass input as valid JSON)",
        func=lambda params: check_pod_affinity(
            *parse_params(params)
        ),
    ),
]

