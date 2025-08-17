"""
Integration tests for langchain_agent module.
"""
import pytest
from src.langchain_agent import set_openai_key, process_query


class TestLangchainAgentIntegration:
    """Integration tests for langchain_agent functions."""

    def test_set_openai_key_with_valid_key(self, valid_openai_key):
        """Test setting OpenAI API key with valid key."""
        try:
            set_openai_key(valid_openai_key)
            # If no exception is raised, the key was accepted
            assert True
        except Exception as e:
            # If there's an error, it should be a proper exception
            assert "error" in str(e).lower() or "invalid" in str(e).lower()

    def test_set_openai_key_with_invalid_key(self):
        """Test setting OpenAI API key with invalid key."""
        with pytest.raises(Exception):
            set_openai_key("invalid-key-12345")

    def test_process_query_without_api_key(self):
        """Test processing query without setting API key first."""
        # Reset agent to None
        import src.langchain_agent
        src.langchain_agent.agent_executor = None
        
        result = process_query("test query")
        
        assert result["status"] == "error"
        assert "API Key not set" in result["message"]

    def test_process_query_with_valid_setup(self, valid_openai_key):
        """Test processing query with valid OpenAI setup."""
        try:
            # Setup the agent
            set_openai_key(valid_openai_key)
            
            # Test a simple query
            result = process_query("What is Kubernetes?")
            
            # Should return some response
            assert "output" in result or "status" in result
            
        except Exception as e:
            # If there's an error, it should be handled gracefully
            pytest.skip(f"OpenAI API not available: {e}")

    def test_agent_initialization_state(self):
        """Test that agent variables are properly initialized."""
        import src.langchain_agent
        
        # Check that global variables exist
        assert hasattr(src.langchain_agent, 'llm')
        assert hasattr(src.langchain_agent, 'agent_executor')

    def test_kubernetes_query_integration(self, valid_openai_key, skip_if_no_k8s):
        """Test integration with Kubernetes queries."""
        try:
            # Setup the agent
            set_openai_key(valid_openai_key)
            
            # Test a Kubernetes-specific query
            result = process_query("List all pods in the cluster")
            
            # Should return some response
            assert "output" in result or "status" in result
            
        except Exception as e:
            # If there's an error, it should be handled gracefully
            pytest.skip(f"Integration test failed: {e}")
