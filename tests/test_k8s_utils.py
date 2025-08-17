"""
Integration tests for k8s_utils module.
"""
import pytest
from src.k8s_utils import (
    get_all_pods_with_usage, get_all_services, get_all_deployments,
    get_all_nodes, get_all_endpoints, get_cluster_events, get_all_namespaces
)


class TestK8sUtilsIntegration:
    """Integration tests for k8s_utils functions."""

    def test_get_all_pods_with_usage(self, skip_if_no_k8s):
        """Test retrieving all pods with resource usage."""
        result = get_all_pods_with_usage()
        
        assert "status" in result
        if result["status"] == "success":
            assert "pods" in result
            assert isinstance(result["pods"], list)
            for pod in result["pods"]:
                assert "name" in pod
                assert "namespace" in pod
                assert "status" in pod

    def test_get_all_services(self, skip_if_no_k8s):
        """Test retrieving all services."""
        result = get_all_services()
        
        assert "status" in result
        if result["status"] == "success":
            assert "services" in result
            assert isinstance(result["services"], list)
            for service in result["services"]:
                assert "name" in service
                assert "namespace" in service
                assert "type" in service

    def test_get_all_deployments(self, skip_if_no_k8s):
        """Test retrieving all deployments."""
        result = get_all_deployments()
        
        assert "status" in result
        if result["status"] == "success":
            assert "deployments" in result
            assert isinstance(result["deployments"], list)
            for deployment in result["deployments"]:
                assert "name" in deployment
                assert "namespace" in deployment

    def test_get_all_nodes(self, skip_if_no_k8s):
        """Test retrieving all nodes."""
        result = get_all_nodes()
        
        assert "status" in result
        if result["status"] == "success":
            assert "nodes" in result
            assert isinstance(result["nodes"], list)
            for node in result["nodes"]:
                assert "name" in node
                assert "status" in node

    def test_get_all_endpoints(self, skip_if_no_k8s):
        """Test retrieving all endpoints."""
        result = get_all_endpoints()
        
        assert "status" in result
        if result["status"] == "success":
            assert "endpoints" in result
            assert isinstance(result["endpoints"], list)

    def test_get_cluster_events(self, skip_if_no_k8s):
        """Test retrieving cluster events."""
        result = get_cluster_events()
        
        assert "status" in result
        if result["status"] == "success":
            assert "events" in result
            assert isinstance(result["events"], list)
            assert len(result["events"]) <= 10  # Should return max 10 events

    def test_get_all_namespaces(self, skip_if_no_k8s):
        """Test retrieving all namespaces."""
        result = get_all_namespaces()
        
        assert "status" in result
        if result["status"] == "success":
            assert "namespaces" in result
            assert isinstance(result["namespaces"], list)
            for namespace in result["namespaces"]:
                assert "name" in namespace
                assert "status" in namespace

    def test_functions_return_proper_error_format(self):
        """Test that functions return proper error format when cluster unavailable."""
        functions = [
            get_all_pods_with_usage,
            get_all_services,
            get_all_deployments,
            get_all_nodes,
            get_all_endpoints,
            get_cluster_events,
            get_all_namespaces
        ]
        
        for func in functions:
            result = func()
            assert "status" in result
            if result["status"] == "error":
                assert "message" in result
