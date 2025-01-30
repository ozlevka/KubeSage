from langchain.agents import initialize_agent
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.agents import AgentType
from src.langchain_tools import k8s_tools

llm = None
agent_executor = None


def set_openai_key(api_key: str) -> None:
    """
    Sets the OpenAI API Key, initializes the LangChain agent, and runs an initial test query.

    Raises:
        AuthenticationError: If the API key is invalid.
        RateLimitError: If OpenAI usage limits are exceeded.
        Exception: For any other unexpected errors.
    """
    global llm, agent_executor

    # Initialize LLM with the new API key
    llm = ChatOpenAI(model_name="gpt-4o-mini", openai_api_key=api_key)

    llm.invoke("Hi")

    # Define a Prompt Template for guiding the agent
    prompt_template = PromptTemplate(
        input_variables=["input"],
        template="""
        You are an AI Kubernetes assistant. Given a user query, choose the correct tool to fetch information.

        - Use "Get Kubernetes Nodes" to retrieve all node statuses.
        - Use "Get Kubernetes Pods" for detailed pod information.
        - Use "Get Kubernetes Services" to list services with their cluster IPs.
        - Use "Get Kubernetes Deployments" for deployment details.

        User Query: {input}
        """
    )

    # Conversation memory to maintain context
    memory = ConversationBufferMemory(memory_key="chat_history")

    # Initialize the LangChain Agent with Kubernetes tools
    agent_executor = initialize_agent(
        tools=k8s_tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        memory=memory
    )

def process_query(user_query: str):
    """Process natural language queries and fetch Kubernetes data via LangChain."""
    return agent_executor.run(user_query)