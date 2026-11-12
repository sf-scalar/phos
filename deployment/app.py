#!/usr/bin/env python3
"""
Scalar Phos — Local Gradio Chat Application
Connects to a local Ollama instance running Scalar Phos Flash or Pro.
Licensed under the Apache License 2.0
"""

import os
import gradio as gr
from openai import OpenAI

# Initialize OpenAI client pointing to local Ollama server
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",  # Ollama doesn't require a real API key
)

# Default model selector (matches Ollama tags)
DEFAULT_MODEL = "hf.co/scalar-ai/scalar-phos-flash:Q4_K_M"


def predict(message, history, model_choice):
    """Formats chat history and streams responses from the local model."""
    # Convert history format for OpenAI client
    messages = [{"role": "system", "content": "You are Scalar Phos, an efficient AI assistant developed by Scalar AI."}]
    
    for user_msg, assistant_msg in history:
        messages.append({"role": "user", "content": user_msg})
        messages.append({"role": "assistant", "content": assistant_msg})
    
    messages.append({"role": "user", "content": message})

    try:
        stream = client.chat.completions.create(
            model=model_choice,
            messages=messages,
            temperature=0.7,
            stream=True
        )
        
        partial_response = ""
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                partial_response += chunk.choices[0].delta.content
                yield partial_response
    except Exception as e:
        yield f"⚠️ **Connection Error:** Could not connect to local Ollama endpoint (`http://localhost:11434`). Make sure Ollama is running (`ollama serve`) and the model is pulled.\n\n*Details: {e}*"


# Build Gradio UI
with gr.Blocks(title="Scalar Phos Local Chat") as demo:
    gr.Markdown("# Scalar Phos — Local Chat Interface")
    gr.Markdown("Interact with your locally deployed **Scalar Phos Flash** or **Pro** models via Ollama.")
    
    with gr.Row():
        model_dropdown = gr.Dropdown(
            choices=[
                "hf.co/scalar-ai/scalar-phos-flash:Q4_K_M",
                "hf.co/scalar-ai/scalar-phos-pro:Q4_K_M"
            ],
            value=DEFAULT_MODEL,
            label="Active Model Weight / GGUF Target"
        )

    gr.ChatInterface(
        fn=predict,
        additional_inputs=[model_dropdown],
        chatbot=gr.Chatbot(height=450),
        textbox=gr.Textbox(placeholder="Type a message or ask a question...", container=False, scale=7),
        theme="soft",
        examples=[
            "Explain quantum computing in two simple sentences.",
            "Write a Python script to check if a number is prime.",
            "What makes parameter-efficient fine-tuning effective?"
        ]
    )

if __name__ == "__main__":
    print("Starting Scalar Phos Gradio server...")
    print("Ensure Ollama is active locally (`ollama serve`).")
    demo.launch(server_name="127.0.0.1", server_port=7860, share=False)
