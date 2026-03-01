# backend/speechtotext.py

import speech_recognition as sr
from pydub import AudioSegment
import tempfile

# ✅ Absolute path to ffmpeg
AudioSegment.converter = r"C:\Users\lenovo\Downloads\ffmpeg\ffmpeg-8.0.1-full_build\bin\ffmpeg.exe"

def process_voice(uploaded_audio):

    # Save uploaded file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".tmp") as temp_file:
        temp_file.write(uploaded_audio.read())
        input_path = temp_file.name

    # Convert to wav using ffmpeg
    sound = AudioSegment.from_file(input_path)
    wav_path = input_path + ".wav"
    sound.export(wav_path, format="wav")

    recognizer = sr.Recognizer()

    with sr.AudioFile(wav_path) as source:
        audio_data = recognizer.record(source)

    transcript_text = recognizer.recognize_google(audio_data, language="en-IN")

    return transcript_text