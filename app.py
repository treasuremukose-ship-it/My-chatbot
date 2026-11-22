from dotenv import load_dotenv
from google.genai import types
import gradio as gr

load_dotenv()

import os

from google import genai

client = genai.Client()

chat = client.chats.create(model="gemini-3.5-flash-lite")

def respond(message, history):
    chat = client.chats.create(model="gemini-3.5-flash-lite")
    response = chat.send_message(message)
    return response.text


demo = gr.ChatInterface(fn=respond, title = "My Gemini Chatbot")

port = int(os.environ.get("PORT", 10000))
demo.launch(server_name="0.0.0.0", server_port=port)




