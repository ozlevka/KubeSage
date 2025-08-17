"""
Example usage of the KubeSage REST API endpoints.
This file demonstrates how to interact with the REST API programmatically.
"""

import requests
import json


class KubeSageAPIClient:
    """Client for interacting with KubeSage REST API."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
    
    def health_check(self) -> dict:
        """Check if the API is healthy."""
        response = self.session.get(f"{self.base_url}/health")
        response.raise_for_status()
        return response.json()
    
    def set_api_key(self, api_key: str) -> dict:
        """Set OpenAI API key."""
        payload = {"api_key": api_key}
        response = self.session.post(
            f"{self.base_url}/api/set-key",
            json=payload
        )
        response.raise_for_status()
        return response.json()
    
    def query_kubernetes(self, query: str, api_key: str) -> dict:
        """Send a Kubernetes query."""
        payload = {
            "query": query,
            "api_key": api_key
        }
        response = self.session.post(
            f"{self.base_url}/api/query",
            json=payload
        )
        response.raise_for_status()
        return response.json()


# Example usage
if __name__ == "__main__":
    # Initialize client
    client = KubeSageAPIClient()
    
    # Example API key (replace with your actual key)
    api_key = "sk-your-openai-api-key-here"
    
    try:
        # Health check
        print("🔍 Checking API health...")
        health = client.health_check()
        print(f"✅ {health['message']}")
        
        # Set API key (optional - can be done per query)
        print("\n🔑 Setting API key...")
        key_response = client.set_api_key(api_key)
        print(f"✅ {key_response['message']}")
        
        # Example queries
        queries = [
            "Show me all pods in the cluster",
            "What nodes are available and their status?",
            "Are there any failing pods?",
            "Show me recent cluster events",
            "Get details about pod nginx-deployment in default namespace"
        ]
        
        for query in queries:
            print(f"\n❓ Query: {query}")
            try:
                result = client.query_kubernetes(query, api_key)
                print(f"✅ Response: {result['output'][:200]}...")
            except requests.exceptions.HTTPError as e:
                print(f"❌ Error: {e}")
                
    except Exception as e:
        print(f"❌ Failed to connect to API: {e}")


# Example curl commands for testing
CURL_EXAMPLES = """
# Health check
curl -X GET "http://localhost:8000/health"

# Set API key
curl -X POST "http://localhost:8000/api/set-key" \
  -H "Content-Type: application/json" \
  -d '{"api_key": "sk-your-openai-api-key-here"}'

# Query Kubernetes
curl -X POST "http://localhost:8000/api/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Show me all pods in the cluster",
    "api_key": "sk-your-openai-api-key-here"
  }'

# Query with complex question
curl -X POST "http://localhost:8000/api/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Are there any pods with high restart counts that might indicate issues?",
    "api_key": "sk-your-openai-api-key-here"
  }'
"""
