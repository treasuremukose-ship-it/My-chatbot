import os
import time
from google import genai
from google.genai import types, errors
import gradio as gr

client = genai.Client()

# 1. Valid models (automatically switches to the next if one has a 503 traffic spike)
MODELS = ["gemini-3.5-flash-lite", "gemini-3.5-flash", "gemini-3.0-flash"]

def respond(message, history):
    # 2. Safely rebuild conversation memory across all Gradio versions
    formatted_history = []
    for item in history[-10:]:
        if isinstance(item, dict):
            role = "model" if item.get("role") == "assistant" else "user"
            text = str(item.get("content", ""))
            if text:
                formatted_history.append(
                    types.Content(role=role, parts=[types.Part.from_text(text=text)])
                )
        elif isinstance(item, (list, tuple)) and len(item) == 2:
            if item[0]:
                formatted_history.append(
                    types.Content(role="user", parts=[types.Part.from_text(text=str(item[0]))])
                )
            if item[1]:
                formatted_history.append(
                    types.Content(role="model", parts=[types.Part.from_text(text=str(item[1]))])
                )

    # 3. Try models in order with error handling so the app never crashes
    for model_name in MODELS:
        try:
            chat = client.chats.create(
                model=model_name,
                history=formatted_history,
                config=types.GenerateContentConfig(
                    thinking_config=types.ThinkingConfig(thinking_budget=0)
                ),
            )
            full_reply = ""
            for chunk in chat.send_message_stream(message):
                if chunk.text:
                    full_reply += chunk.text
                    yield full_reply
            return  # Success! Exit the loop

        except errors.ServerError as e:
            if e.code == 503:
                time.sleep(1)
                continue  # Silently try the next backup model
            yield f"⚠️ Google server error ({e.code}): {e.message}"
            return
        except Exception as e:
            yield f"⚠️ Something went wrong: {str(e)}"
            return

    yield "⏳ All models are temporarily busy right now. Please send your message again in a few seconds."

demo = gr.ChatInterface(fn=respond, title="My Gemini Chatbot")

port = int(os.environ.get("PORT", 10000))
demo.launch(server_name="0.0.0.0", server_port=port)


