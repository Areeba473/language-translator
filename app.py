import os
import gradio as gr
from groq import Groq

# API Key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY not found")

client = Groq(api_key=GROQ_API_KEY)

def translate_english_to_urdu(text):
    if not text.strip():
        return "Please enter English text."

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a professional translator. "
                    "Translate English text into Urdu. "
                    "Only return the Urdu translation."
                )
            },
            {"role": "user", "content": text}
        ],
        temperature=0.2,
        max_tokens=300,
    )

    return response.choices[0].message.content.strip()


# 🎨 Blue & White Theme
theme = gr.themes.Base(
    primary_hue="blue",
    secondary_hue="cyan",
    neutral_hue="gray",
    radius_size="lg",
    font=["Inter", "system-ui", "sans-serif"],
)

# 🧱 UI Layout
with gr.Blocks(theme=theme, css="""
#title {
    text-align: center;
    font-size: 2.3rem;
    font-weight: 700;
    color: #1e3a8a;
}
#subtitle {
    text-align: center;
    color: #4b5563;
    margin-bottom: 1.5rem;
}
.gradio-container {
    max-width: 900px !important;
}
button.primary {
    background: linear-gradient(90deg, #2563eb, #3b82f6) !important;
    border: none !important;
}
""") as demo:

    gr.Markdown("<div id='title'>English → Urdu Translator</div>")
    gr.Markdown("<div id='subtitle'>Fast & Accurate Translation using Groq AI</div>")

    with gr.Row():
        with gr.Column():
            english_text = gr.Textbox(
                label="English Text",
                placeholder="Type English here...",
                lines=6
            )
        with gr.Column():
            urdu_text = gr.Textbox(
                label="Urdu Translation",
                lines=6
            )

    with gr.Row():
        translate_btn = gr.Button("Translate", variant="primary")
        clear_btn = gr.Button("Clear", variant="secondary")

    translate_btn.click(
        fn=translate_english_to_urdu,
        inputs=english_text,
        outputs=urdu_text
    )

    clear_btn.click(
        fn=lambda: ("", ""),
        inputs=None,
        outputs=[english_text, urdu_text]
    )

    gr.Markdown(
        "<center style='color:#6b7280;margin-top:1rem;'>"
        "Powered by Groq • Built with Gradio"
        "</center>"
    )

if __name__ == "__main__":
    demo.launch()
