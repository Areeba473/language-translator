import os
import gradio as gr
from groq import Groq

# Get Groq API Key from Environment Variable
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize Groq Client
client = Groq(api_key=GROQ_API_KEY)


def translate_english_to_urdu(text):
    if not text.strip():
        return "Please enter some English text."

    try:
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional English to Urdu translator."
                },
                {
                    "role": "user",
                    "content": f"Translate this into Urdu: {text}"
                }
            ],
            temperature=0.3,
            max_tokens=500
        )

        urdu_translation = completion.choices[0].message.content
        return urdu_translation

    except Exception as e:
        return f"Error: {str(e)}"


# Gradio Interface
interface = gr.Interface(
    fn=translate_english_to_urdu,
    inputs=gr.Textbox(
        label="Enter English Text",
        placeholder="Type English here...",
        lines=4
    ),
    outputs=gr.Textbox(
        label="Urdu Translation",
        lines=4
    ),
    title="English to Urdu Translator",
    description="Translate English text into Urdu using Groq AI",
    theme="soft"
)


if __name__ == "__main__":
    interface.launch()
