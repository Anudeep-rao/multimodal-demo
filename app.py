import streamlit as st
import os
from openai import OpenAI
from google import genai
from PIL import Image
import pytesseract
import tempfile
from gtts import gTTS
from backend.speechtotext import process_voice
from io import BytesIO

# ==============================
# PAGE CONFIG
# ==============================

st.set_page_config(page_title="Multimodal Vernacular AI", layout="wide")

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# ==============================
# GEMINI CLIENT
# ==============================

api_key = os.getenv("GOOGLE_API_KEY")
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

if not api_key:
    st.error("⚠️ GOOGLE_API_KEY not found in environment variables.")
    st.stop()

client = genai.Client(api_key=api_key)

# ==============================
# LANGUAGE MAP
# ==============================

languages = ["Hindi", "Telugu", "Tamil", "French", "German", "Spanish"]

st.markdown("## 🩺 Multimodal Vernacular Prescription AI")

target_language = st.selectbox("Select Language", languages)

# ==============================
# MODEL DETECTION
# ==============================

def get_supported_model():
    try:
        models = client.models.list()
        model_names = [m.name for m in models]

        # Prefer Gemini if available
        for name in model_names:
            if "gemini" in name:
                return name

        # Fall back to Bison if Gemini not found
        for name in model_names:
            if "bison" in name:
                return name

        # If nothing matches, return None
        return None

    except Exception as e:
        st.error(f"Could not list models: {str(e)}")
        return None

MODEL_NAME = get_supported_model()

def gemini_translate(text):
    if not text.strip():
        return "No valid text detected."

    if not MODEL_NAME:
        return "No supported translation model found."

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=f"""
            You are a professional medical translator.
            Translate the following prescription into {target_language}.
            Keep medical meaning accurate.

            Prescription:
            {text}
            """
        )
        return response.text

    except Exception as e:
        return f"Translation failed: {str(e)}"


# ==============================
# IMAGE GENERATION FUNCTION
# ==============================
import base64

def generate_image(prompt, style):
    try:
        result = openai_client.images.generate(
            model="gpt-image-1",
            prompt=f"{prompt}, {style}, high quality, detailed",
            size="1024x1024"
        )

        image_base64 = result.data[0].b64_json
        image_bytes = base64.b64decode(image_base64)

        return image_bytes

    except Exception as e:
        st.error(f"Image generation failed: {str(e)}")
        return None

# ==============================
# AUDIO FUNCTION
# ==============================

def generate_audio(text):
    tts = gTTS(text)
    temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(temp_audio.name)
    return temp_audio.name

# ==============================
# TABS
# ==============================

tab1, tab2, tab3, tab4 = st.tabs([
    "📝 Text Input",
    "🖼 Image Input",
    "🎤 Voice Input",
    "🎨 Generate Image"
])

# =========================================================
# TEXT INPUT
# =========================================================

with tab1:
    text_input = st.text_area("Enter Prescription")

    if st.button("Process Text"):
        if text_input:
            with st.spinner("Translating..."):
                translated = gemini_translate(text_input)

            st.success("Translated Text")
            st.write(translated)

            audio_file = generate_audio(translated)
            st.audio(audio_file)

# =========================================================
# IMAGE INPUT (OCR)
# =========================================================

with tab2:
    uploaded_image = st.file_uploader("Upload Prescription Image", type=["png", "jpg", "jpeg"])

    if uploaded_image:
        image = Image.open(uploaded_image)
        st.image(image)

        if st.button("Process Image"):
            with st.spinner("Extracting text..."):
                extracted_text = pytesseract.image_to_string(image)

            st.info("Extracted Text")
            st.write(extracted_text)

            with st.spinner("Translating..."):
                translated = gemini_translate(extracted_text)

            st.success("Translated Text")
            st.write(translated)

            audio_file = generate_audio(translated)
            st.audio(audio_file)

# =========================================================
# VOICE INPUT
# =========================================================

# =========================================================
# VOICE INPUT (UPDATED CLEAN VERSION)
# =========================================================
# =========================================================
# VOICE INPUT (FINAL CLEAN VERSION)
# =========================================================

with tab3:
    uploaded_audio = st.file_uploader("Upload Voice File", type=["mp3", "wav", "m4a"])

    if uploaded_audio:
        st.audio(uploaded_audio)

        if st.button("Process Voice"):

            try:
                # ONLY call backend function
                transcript_text = process_voice(uploaded_audio)

                st.info("Transcribed Text")
                st.write(transcript_text)

                # Translate using Gemini
                translated = gemini_translate(transcript_text)

                st.success("Translated Text")
                st.write(translated)

                # Generate Audio
                audio_file = generate_audio(translated)
                st.audio(audio_file)

            except Exception as e:
                st.error(f"Voice processing failed: {str(e)}")

# =========================================================
# IMAGE GENERATION TAB
# =========================================================

with tab4:
    prompt = st.text_input("Enter image prompt")
    style = st.selectbox("Select Style", ["Medical Diagram", "Realistic", "Cartoon", "3D Render"])

    if st.button("Generate Image"):
        if prompt:
            with st.spinner("Generating image..."):
                image_bytes = generate_image(prompt, style)

            if image_bytes:
                image = Image.open(BytesIO(image_bytes))
                st.image(image)
        else:
            st.warning("Please enter a prompt.")
