import traceback
from fastapi import WebSocket
from openai import RateLimitError, AuthenticationError
from src.langchain_agent import process_query, init_llm_and_executor


async def websocket_handler(websocket: WebSocket):
    """WebSocket for real-time Kubernetes AI chatbot."""
    await websocket.accept()
    await websocket.send_text("🔹 Kubernetes Chat Assistant Started! Using OPENROUTER_API_KEY from environment.")

    initialized = False

    while True:
        query = await websocket.receive_text()

        if query.lower() == "exit":
            await websocket.send_text("❌ Closing connection.")
            break

        if not initialized:
            try:
                init_llm_and_executor()
                initialized = True
                await websocket.send_text("✅ LLM initialized! You can now ask questions.")
            except ValueError as e:
                await websocket.send_text(f"❌ Configuration error: {str(e)}")
                await websocket.send_text("Type 'exit' to quit.")
                continue
            except AuthenticationError:
                await websocket.send_text("❌ Invalid API Key! Please check your OPENROUTER_API_KEY environment variable.")
                await websocket.send_text("Type 'exit' to quit.")
                continue
            except RateLimitError:
                await websocket.send_text("⚠️ You exceeded your quota, please check your plan and billing details.")
                await websocket.send_text("Type 'exit' to quit.")
                continue
            except Exception as e:
                error_message = f"❌ An unexpected error occurred: {str(e)}"
                print(traceback.format_exc())
                await websocket.send_text(error_message)
                continue

        try:
            response = process_query(query)
            await websocket.send_text(str(response.get('output')))
        except Exception as e:
            error_message = f"❌ Query processing error: {str(e)}"
            print(traceback.format_exc())
            await websocket.send_text(error_message)

    await websocket.close()