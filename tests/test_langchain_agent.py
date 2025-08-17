"""
Integration tests for langchain_agent module.
"""
import pytest
from src.langchain_agent import init_llm_and_executor, process_query


class TestLangchainAgentIntegration:
    """Integration tests for langchain_agent functions."""

    def test_init_llm_and_executor_with_env_var(self):
        """Test initializing LLM and executor with environment variable."""
        import os
        # Save original env var
        original_key = os.environ.get("OPENAI_API_KEY")
        
        try:
            # Set a test key
            os.environ["OPENAI_API_KEY"] = "test-key-for-testing"
            
            # This should raise ValueError since we're using a test key
            with pytest.raises(Exception):
                init_llm_and_executor()
                
        finally:
            # Restore original env var
            if original_key:
                os.environ["OPENAI_API_KEY"] = original_key
            elif "OPENAI_API_KEY" in os.environ:
                del os.environ["OPENAI_API_KEY"]

    def test_init_llm_and_executor_without_env_var(self):
        """Test initializing LLM and executor without environment variable."""
        import os
        # Save original env var
        original_key = os.environ.get("OPENAI_API_KEY")
        
        try:
            # Remove env var
            if "OPENAI_API_KEY" in os.environ:
                del os.environ["OPENAI_API_KEY"]
            
            with pytest.raises(ValueError, match="OPENAI_API_KEY environment variable is not set"):
                init_llm_and_executor()
                
        finally:
            # Restore original env var
            if original_key:
                os.environ["OPENAI_API_KEY"] = original_key

    def test_process_query_without_env_var(self):
        """Test processing query without environment variable set."""
        import os
        # Save original env var
        original_key = os.environ.get("OPENAI_API_KEY")
        
        try:
            # Remove env var
            if "OPENAI_API_KEY" in os.environ:
                del os.environ["OPENAI_API_KEY"]
            
            # Reset agent to None
            import src.langchain_agent
            src.langchain_agent.agent_executor = None
            
            # This should trigger initialization which will fail
            with pytest.raises(ValueError, match="OPENAI_API_KEY environment variable is not set"):
                process_query("test query")
                
        finally:
            # Restore original env var
            if original_key:
                os.environ["OPENAI_API_KEY"] = original_key

    def test_process_query_with_model_parameter(self):
        """Test processing query with model parameter."""
        import os
        # Save original env var
        original_key = os.environ.get("OPENAI_API_KEY")
        
        try:
            # Set a test key
            os.environ["OPENAI_API_KEY"] = "test-key-for-testing"
            
            # Reset agent to None
            import src.langchain_agent
            src.langchain_agent.agent_executor = None
            
            # This should raise an exception due to invalid key, but test the model parameter
            with pytest.raises(Exception):
                process_query("test query", "openai/gpt-4o-mini")
                
        finally:
            # Restore original env var
            if original_key:
                os.environ["OPENAI_API_KEY"] = original_key
            elif "OPENAI_API_KEY" in os.environ:
                del os.environ["OPENAI_API_KEY"]

    def test_agent_initialization_state(self):
        """Test that agent variables are properly initialized."""
        import src.langchain_agent
        
        # Check that global variables exist
        assert hasattr(src.langchain_agent, 'llm')
        assert hasattr(src.langchain_agent, 'agent_executor')
        assert hasattr(src.langchain_agent, 'current_model')

    def test_model_change_reinitializes_agent(self):
        """Test that changing model reinitializes the agent."""
        import os
        import src.langchain_agent
        
        # Save original env var
        original_key = os.environ.get("OPENAI_API_KEY")
        
        try:
            # Set a test key
            os.environ["OPENAI_API_KEY"] = "test-key-for-testing"
            
            # Reset agent state
            src.langchain_agent.agent_executor = None
            src.langchain_agent.current_model = None
            
            # Mock successful initialization for testing
            def mock_init(model_name):
                src.langchain_agent.current_model = model_name
                src.langchain_agent.agent_executor = "mock_agent"
            
            # Replace the init function temporarily
            original_init = src.langchain_agent.init_llm_and_executor
            src.langchain_agent.init_llm_and_executor = mock_init
            
            try:
                # First call with model1
                result1 = process_query("test", "model1")
                assert src.langchain_agent.current_model == "model1"
                
                # Second call with different model should reinitialize
                result2 = process_query("test", "model2")
                assert src.langchain_agent.current_model == "model2"
                
            finally:
                # Restore original function
                src.langchain_agent.init_llm_and_executor = original_init
                
        finally:
            # Restore original env var
            if original_key:
                os.environ["OPENAI_API_KEY"] = original_key
            elif "OPENAI_API_KEY" in os.environ:
                del os.environ["OPENAI_API_KEY"]
