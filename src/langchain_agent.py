from langchain.agents import initialize_agent
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.agents import AgentType
from openai import NotFoundError
from src.langchain_tools import broad_insights_tools, deep_dive_tools

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
    model_name = "chatgpt-4o-latest"
    llm = ChatOpenAI(model_name=model_name, openai_api_key=api_key)

    try:
        llm.invoke("Hi, this is a test query")
    except NotFoundError as e:
        print(f"{model_name} doesn't exist, using gpt-4o-mini instead")
        llm = ChatOpenAI(model_name="gpt-4o-mini", openai_api_key=api_key)
        llm.invoke("Hi, this is a test query")

    # Define a Prompt Template for guiding the agent
    prompt_template = PromptTemplate(
        input_variables=["input"],
        template="""
            You are an **AI Kubernetes Troubleshooting Assistant**.

            🔹 **You have access to two categories of tools**:
            1️⃣ **Broad Insights Tools** → Surface-level data for multiple resources.
            2️⃣ **Deep Dive Tools** → Detailed analysis of specific resources.

            ---

            **📌 How to use these tools:**
            - **Start with Broad Insights** → Use **broad tools** if the user asks about overall cluster health.
            - **Use Deep Dive Tools** → If an issue is suspected, analyze a specific resource in-depth.
            - **Correlate multiple tool outputs** to provide insightful recommendations.

            ---

            **🔹 Available Tools:**

            🟢 **Broad Insights Tools**
            - `"Get All Pods with Resource Usage"` → Lists all pods with CPU & Memory usage.
            - `"Get All Services"` → Lists all services with their types and ports.
            - `"Get All Deployments"` → Lists deployments with replica status.
            - `"Get All Nodes"` → Lists nodes with their health & capacity.
            - `"Get All Endpoints"` → Fetches endpoints and associated services.
            - `"Get Cluster Events"` → Lists recent cluster-wide warnings & failures.
            - `"Get Namespace List"` → Lists all namespaces and their statuses.

            🔵 **Deep Dive Tools**
            - `"Describe Pod with Restart Count"` → Fetches detailed pod info + restart count.
            - `"Get Pod Logs"` → Fetches the last 10 log lines for a specific pod.
            - `"Describe Service"` → Fetches service details (ClusterIP, NodePort, ExternalName).
            - `"Describe Deployment"` → Fetches replica counts & container images.
            - `"Get Node Status & Capacity"` → Fetches node health conditions & resource usage.
            - `"Check RBAC Events & Role Bindings"` → Fetches RBAC security events & role bindings.
            - `"Get Persistent Volumes & Claims"` → Lists PVs, PVCs, and their bound claims.
            - `"Get Running Jobs & CronJobs"` → Lists active Jobs & CronJobs.
            - `"Get Ingress Resources & Annotations"` → Lists Ingress rules, hosts, and annotations.
            - `"Check Pod Affinity & Anti-Affinity"` → Analyzes pod scheduling constraints.

            ---

            **🚀 General Workflow for Debugging:
            1️⃣ Identify affected resources.
            2️⃣ Use **Broad Insights Tools** for an overview.
            3️⃣ Use **Deep Dive Tools** for root cause analysis.
            4️⃣ Provide actionable recommendations.

            ---

            **🚀 Example Workflow for a Pod Issue:**
            1️⃣ **User Query:** "Why is my app crashing?"
            2️⃣ **Step 1:** Use `"Get All Pods with Resource Usage"` to identify failing pods.
            3️⃣ **Step 2:** Use `"Describe Pod with Restart Count"` for specific failure reasons.
            4️⃣ **Step 3:** Use `"Get Pod Logs"` to analyze errors.
            5️⃣ **Step 4:** If node issues are suspected, use `"Get Node Status & Capacity"`.
            6️⃣ **Step 5:** Provide an **actionable recommendation** based on tool outputs.

            ---

            **🔹 User Query:** {input}
            """
    )

    # Conversation memory to maintain context
    memory = ConversationBufferMemory(memory_key="chat_history")

    # Initialize the LangChain Agent with Kubernetes tools
    agent_executor = initialize_agent(
        tools=broad_insights_tools + deep_dive_tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        memory=memory,
        prompt=prompt_template
    )

def process_query(user_query: str):
    """Process natural language queries and fetch Kubernetes data via LangChain."""
    if agent_executor is None:
        return {"status": "error", "message": "API Key not set. Please provide a valid OpenAI API key first."}

    return agent_executor.invoke(user_query)