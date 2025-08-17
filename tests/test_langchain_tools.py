"""
Integration tests for langchain_tools module.
"""
import pytest
import json
from src.langchain_tools import broad_insights_tools, deep_dive_tools, parse_params


class TestLangchainToolsIntegration:
    """Integration tests for langchain_tools functions."""

    def test_broad_insights_tools_exist(self):
        """Test that broad insights tools are properly defined."""
        assert len(broad_insights_tools) > 0
        
        for tool in broad_insights_tools:
            assert hasattr(tool, 'name')
            assert hasattr(tool, 'description')
            assert hasattr(tool, 'func')

    def test_deep_dive_tools_exist(self):
        """Test that deep dive tools are properly defined."""
        assert len(deep_dive_tools) > 0
        
        for tool in deep_dive_tools:
            assert hasattr(tool, 'name')
            assert hasattr(tool, 'description')
            assert hasattr(tool, 'func')

    def test_broad_insights_tools_execution(self, skip_if_no_k8s):
        """Test execution of broad insights tools."""
        for tool in broad_insights_tools:
            try:
                # Execute tool with dummy input
                result = tool.func("dummy_input")
                
                # Should return a dictionary with status
                assert isinstance(result, dict)
                assert "status" in result
                
            except Exception as e:
                # If there's an error, it should be handled gracefully
                assert "error" in str(e).lower() or "connection" in str(e).lower()

    def test_deep_dive_tools_with_valid_params(self, skip_if_no_k8s, test_namespace):
        """Test execution of deep dive tools with valid parameters."""
        # Test tools that require parameters
        param_tools = [
            ("Describe Pod with Restart Count", {"namespace": test_namespace, "pod_name": "test-pod"}),
            ("Get Pod Logs", {"namespace": test_namespace, "pod_name": "test-pod"}),
            ("Describe Service", {"namespace": test_namespace, "service_name": "kubernetes"}),
            ("Describe Deployment", {"namespace": test_namespace, "deployment_name": "test-deployment"}),
            ("Get Node Status & Capacity", {"node_name": "test-node"}),
            ("Check Pod Affinity & Anti-Affinity", {"namespace": test_namespace, "pod_name": "test-pod"})
        ]
        
        for tool_name, params in param_tools:
            tool = next((t for t in deep_dive_tools if t.name == tool_name), None)
            if tool:
                try:
                    # Execute tool with JSON parameters
                    result = tool.func(json.dumps(params))
                    
                    # Should return a dictionary with status
                    assert isinstance(result, dict)
                    assert "status" in result
                    
                except Exception as e:
                    # If there's an error, it should be handled gracefully
                    assert "error" in str(e).lower() or "connection" in str(e).lower()

    def test_deep_dive_tools_without_params(self, skip_if_no_k8s):
        """Test execution of deep dive tools that don't require parameters."""
        no_param_tools = [
            "Check RBAC Events & Role Bindings",
            "Get Persistent Volumes & Claims",
            "Get Running Jobs & CronJobs",
            "Get Ingress Resources & Annotations"
        ]
        
        for tool_name in no_param_tools:
            tool = next((t for t in deep_dive_tools if t.name == tool_name), None)
            if tool:
                try:
                    # Execute tool with dummy input
                    result = tool.func("dummy_input")
                    
                    # Should return a dictionary with status
                    assert isinstance(result, dict)
                    assert "status" in result
                    
                except Exception as e:
                    # If there's an error, it should be handled gracefully
                    assert "error" in str(e).lower() or "connection" in str(e).lower()

    def test_parse_params_with_dict(self):
        """Test parse_params function with dictionary input."""
        test_dict = {"namespace": "default", "pod_name": "test-pod"}
        result = parse_params(test_dict)
        assert result == test_dict

    def test_parse_params_with_json_string(self):
        """Test parse_params function with JSON string input."""
        test_dict = {"namespace": "default", "pod_name": "test-pod"}
        json_string = json.dumps(test_dict)
        result = parse_params(json_string)
        assert result == test_dict

    def test_parse_params_with_invalid_json(self):
        """Test parse_params function with invalid JSON."""
        with pytest.raises(ValueError):
            parse_params("invalid json string")

    def test_parse_params_with_non_dict_json(self):
        """Test parse_params function with non-dictionary JSON."""
        with pytest.raises(ValueError):
            parse_params(json.dumps(["not", "a", "dict"]))

    def test_tool_names_are_unique(self):
        """Test that all tool names are unique."""
        all_tools = broad_insights_tools + deep_dive_tools
        tool_names = [tool.name for tool in all_tools]
        assert len(tool_names) == len(set(tool_names))

    def test_tool_descriptions_exist(self):
        """Test that all tools have descriptions."""
        all_tools = broad_insights_tools + deep_dive_tools
        for tool in all_tools:
            assert tool.description
            assert len(tool.description) > 10  # Meaningful description

    def test_integration_with_kubernetes_functions(self, skip_if_no_k8s):
        """Test that tools properly integrate with underlying Kubernetes functions."""
        # Test a few key tools to ensure they call the right functions
        pod_tool = next((t for t in broad_insights_tools if "Pods" in t.name), None)
        if pod_tool:
            result = pod_tool.func("dummy")
            assert isinstance(result, dict)
            assert "status" in result
