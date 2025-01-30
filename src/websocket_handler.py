import traceback
from fastapi import WebSocket
from openai import RateLimitError, AuthenticationError
from src.langchain_agent import process_query, set_openai_key


async def websocket_handler(websocket: WebSocket):
    """WebSocket for real-time Kubernetes AI chatbot."""
    await websocket.accept()
    await websocket.send_text("🔹 Kubernetes Chat Assistant Started! Please enter your OpenAI API key.")

    api_key_set = False

    while True:
        query = await websocket.receive_text()

        if query.lower() == "exit":
            await websocket.send_text("❌ Closing connection.")
            break

        if not api_key_set:
            try:
                set_openai_key(query)
                api_key_set = True
                await websocket.send_text("✅ API Key successfully set! You can now ask questions.")
                continue
            except AuthenticationError:
                await websocket.send_text("❌ Invalid API Key! Please try again or type 'exit' to quit.")
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

        response = process_query(query)
        await websocket.send_text(str(response))

    await websocket.close()