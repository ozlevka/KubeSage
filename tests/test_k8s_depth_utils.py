"""
Integration tests for k8s_depth_utils module.
"""
import pytest
from src.k8s_depth_utils import (
    describe_pod_with_restart_count, get_pod_logs, describe_service,
    describe_deployment, get_node_status_and_capacity, get_rbac_events_and_role_bindings,
    get_persistent_volumes_and_claims, get_running_jobs_and_cronjobs,
    get_ingress_resources, check_pod_affinity, get_kubernetes_object_yaml
)


class TestK8sDepthUtilsIntegration:
    """Integration tests for k8s_depth_utils functions."""

    def test_describe_pod_with_restart_count(self, skip_if_no_k8s, test_namespace):
        """Test describing pod with restart count."""
        # Try to get a real pod from the cluster
        from src.k8s_utils import get_all_pods_with_usage
        pods_result = get_all_pods_with_usage()
        
        if pods_result["status"] == "success" and pods_result["pods"]:
            pod_name = pods_result["pods"][0]["name"]
            namespace = pods_result["pods"][0]["namespace"]
            
            result = describe_pod_with_restart_count(namespace, pod_name)
            
            assert "status" in result
            if result["status"] == "success":
                assert "name" in result
                assert "namespace" in result
                assert "restart_count" in result
                assert "containers" in result

    def test_get_pod_logs(self, skip_if_no_k8s, test_namespace):
        """Test retrieving pod logs."""
        # Try to get a real pod from the cluster
        from src.k8s_utils import get_all_pods_with_usage
        pods_result = get_all_pods_with_usage()
        
        if pods_result["status"] == "success" and pods_result["pods"]:
            pod_name = pods_result["pods"][0]["name"]
            namespace = pods_result["pods"][0]["namespace"]
            
            result = get_pod_logs(namespace, pod_name)
            
            assert "status" in result
            if result["status"] == "success":
                assert "logs" in result
                assert isinstance(result["logs"], list)
                assert len(result["logs"]) <= 10

    def test_describe_service(self, skip_if_no_k8s, test_service_name, test_namespace):
        """Test describing a service."""
        result = describe_service(test_namespace, test_service_name)
        
        assert "status" in result
        if result["status"] == "success":
            assert "name" in result
            assert "namespace" in result
            assert "type" in result

    def test_describe_deployment(self, skip_if_no_k8s, test_namespace):
        """Test describing a deployment."""
        # Try to get a real deployment from the cluster
        from src.k8s_utils import get_all_deployments
        deployments_result = get_all_deployments()
        
        if deployments_result["status"] == "success" and deployments_result["deployments"]:
            deployment_name = deployments_result["deployments"][0]["name"]
            namespace = deployments_result["deployments"][0]["namespace"]
            
            result = describe_deployment(namespace, deployment_name)
            
            assert "status" in result
            if result["status"] == "success":
                assert "name" in result
                assert "namespace" in result
                assert "containers" in result

    def test_get_node_status_and_capacity(self, skip_if_no_k8s, test_node_name):
        """Test getting node status and capacity."""
        result = get_node_status_and_capacity(test_node_name)
        
        assert "status" in result
        if result["status"] == "success":
            assert "name" in result
            assert "conditions" in result
            assert "capacity" in result

    def test_get_rbac_events_and_role_bindings(self, skip_if_no_k8s):
        """Test retrieving RBAC events and role bindings."""
        result = get_rbac_events_and_role_bindings()
        
        assert "status" in result
        if result["status"] == "success":
            assert "rbac_events" in result
            assert "role_bindings" in result
            assert "cluster_role_bindings" in result

    def test_get_persistent_volumes_and_claims(self, skip_if_no_k8s):
        """Test retrieving persistent volumes and claims."""
        result = get_persistent_volumes_and_claims()
        
        assert "status" in result
        if result["status"] == "success":
            assert "persistent_volumes" in result
            assert "persistent_volume_claims" in result

    def test_get_running_jobs_and_cronjobs(self, skip_if_no_k8s):
        """Test retrieving running jobs and cronjobs."""
        result = get_running_jobs_and_cronjobs()
        
        assert "status" in result
        if result["status"] == "success":
            assert "running_jobs" in result
            assert "cronjobs" in result

    def test_get_ingress_resources(self, skip_if_no_k8s):
        """Test retrieving ingress resources."""
        result = get_ingress_resources()
        
        assert "status" in result
        if result["status"] == "success":
            assert "ingress_resources" in result

    def test_check_pod_affinity(self, skip_if_no_k8s, test_namespace):
        """Test checking pod affinity."""
        # Try to get a real pod from the cluster
        from src.k8s_utils import get_all_pods_with_usage
        pods_result = get_all_pods_with_usage()
        
        if pods_result["status"] == "success" and pods_result["pods"]:
            pod_name = pods_result["pods"][0]["name"]
            namespace = pods_result["pods"][0]["namespace"]
            
            result = check_pod_affinity(namespace, pod_name)
            
            assert "status" in result
            if result["status"] == "success":
                assert "pod" in result
                assert "namespace" in result
                assert "affinity_details" in result

    def test_get_kubernetes_object_yaml(self, skip_if_no_k8s, test_namespace):
        """Test retrieving Kubernetes object YAML."""
        # Try to get a real pod from the cluster
        from src.k8s_utils import get_all_pods_with_usage
        pods_result = get_all_pods_with_usage()
        
        if pods_result["status"] == "success" and pods_result["pods"]:
            pod_name = pods_result["pods"][0]["name"]
            namespace = pods_result["pods"][0]["namespace"]
            
            # Test getting pod YAML
            result = get_kubernetes_object_yaml("pod", pod_name, namespace)
            
            assert "status" in result
            if result["status"] == "success":
                assert "resource_type" in result
                assert "name" in result
                assert "namespace" in result
                assert "yaml_content" in result
                assert result["resource_type"] == "pod"
                assert result["name"] == pod_name
                assert result["namespace"] == namespace
                assert "apiVersion" in result["yaml_content"]
                assert "kind: Pod" in result["yaml_content"]
        
        # Test with unsupported resource type
        result = get_kubernetes_object_yaml("unsupported", "test", "default")
        assert result["status"] == "error"
        assert "Unsupported resource type" in result["message"]
        
        # Test with non-existent resource
        result = get_kubernetes_object_yaml("pod", "non-existent-pod", "default")
        assert result["status"] == "error"
        assert "not found" in result["message"]

    def test_functions_return_proper_error_format(self):
        """Test that functions return proper error format when cluster unavailable."""
        functions_with_params = [
            (describe_pod_with_restart_count, ["default", "test-pod"]),
            (get_pod_logs, ["default", "test-pod"]),
            (describe_service, ["default", "test-service"]),
            (describe_deployment, ["default", "test-deployment"]),
            (get_node_status_and_capacity, ["test-node"]),
            (check_pod_affinity, ["default", "test-pod"]),
            (get_kubernetes_object_yaml, ["pod", "test-pod", "default"])
        ]
        
        functions_without_params = [
            get_rbac_events_and_role_bindings,
            get_persistent_volumes_and_claims,
            get_running_jobs_and_cronjobs,
            get_ingress_resources
        ]
        
        for func, params in functions_with_params:
            result = func(*params)
            assert "status" in result
            if result["status"] == "error":
                assert "message" in result
        
        for func in functions_without_params:
            result = func()
            assert "status" in result
            if result["status"] == "error":
                assert "message" in result
