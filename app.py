
from google.genai import types, errors
import gradio as gr


import os
import time
from google import genai

client = genai.Client()

models = ["gemini-2.5-flash-lite, gemini-2.5-flash, gemini-2.5-lite"]    

def respond(message, history):
    formatted_history = []
    for item in history[-10,]:
        if isinstance(item, dict):
            role = model if item.get("role") == "assistant" else "user"
            text = str(item.get("content",  ""))
            if text:
                formatted_history.append(
                    types.Content(role=role, parts=[types.Part.from_text(text=te:)
        elif isinstance(item, (list, tuple)) and len(item) == 2:
            if item[0]:
                formatted_history.append(
                    types.Content(role="user", parts =[types.Part.from_text(text=te:)
                                                       
            if item[1]:
                formatted_history.append(
                    types.Content(role="model", parts =[types.Part.from_text(text=te:)
                                                        
for model_name in MODELS:
    try:
        chat = client.chats.create(
            model=model_name, 
            history= formatted_history, 
            config= types.GenerateContentConfig(
                thinking_config= types.Thinking.Config(thinking_budget=0)
            ),
        )
        )
            full_reply = ""
            for chunk in chat.send_message_stream(message):
                if chunk.text:
                    full_reply += chunk.text
                    yield full_reply
            return  

        except errors.ServerError as e:
            if e.code == 503:
                time.sleep(1)
                continue  
            yield f"⚠️ Google server error ({e.code}): {e.message}"
            return
        except Exception as e:
            yield f"⚠️ Something went wrong: {str(e)}"
            return

    yield "⏳ All models are temporarily busy right now. Please send your message again in a few seconds."



