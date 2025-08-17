"""
Test configuration and fixtures for KubeSage integration tests.
"""
import pytest
import os


@pytest.fixture(scope="session")
def skip_if_no_k8s():
    """Skip tests if Kubernetes is not available."""
    if "KUBERNETES_SERVICE_HOST" not in os.environ and not os.path.exists(os.path.expanduser("~/.kube/config")):
        pytest.skip("Kubernetes cluster not available")


@pytest.fixture
def test_namespace():
    """Provide test namespace for integration tests."""
    return "default"


@pytest.fixture
def test_pod_name():
    """Provide test pod name for integration tests."""
    return "kube-system"  # Use system namespace pods for testing


@pytest.fixture
def test_service_name():
    """Provide test service name for integration tests."""
    return "kubernetes"  # Default kubernetes service


@pytest.fixture
def test_node_name():
    """Get first available node name for testing."""
    try:
        from src.k8s_utils import get_all_nodes
        result = get_all_nodes()
        if result["status"] == "success" and result["nodes"]:
            return result["nodes"][0]["name"]
    except:
        pass
    return "test-node"


@pytest.fixture
def valid_openai_key():
    """Provide OpenAI API key from environment or skip test."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        pytest.skip("OPENAI_API_KEY environment variable not set")
    return api_key
