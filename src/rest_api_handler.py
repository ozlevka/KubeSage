import traceback
from fastapi import HTTPException
from pydantic import BaseModel
from openai import RateLimitError, AuthenticationError
from src.langchain_agent import process_query


class QueryRequest(BaseModel):
    """Request model for processing queries."""
    query: str
    model_name: str = "openai/gpt-4o"


class QueryResponse(BaseModel):
    """Response model for query operations."""
    status: str
    output: str = None
    error: str = None


def process_kubernetes_query(request: QueryRequest) -> QueryResponse:
    """Process a Kubernetes query using the LangChain agent."""
    try:
        # Process the query with specified model
        response = process_query(request.query, request.model_name)
        
        return QueryResponse(
            status="success",
            output=str(response.get('output', ''))
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=f"❌ Configuration error: {str(e)}"
        )
    except AuthenticationError:
        raise HTTPException(
            status_code=401,
            detail="❌ Invalid API Key! Please check your OPENROUTER_API_KEY environment variable."
        )
    except RateLimitError:
        raise HTTPException(
            status_code=429,
            detail="⚠️ You exceeded your quota, please check your plan and billing details."
        )
    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"❌ An unexpected error occurred: {str(e)}"
        )


def health_check() -> dict:
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "KubeSage REST API",
        "message": "🔹 Kubernetes Chat Assistant REST API is running!"
    }
