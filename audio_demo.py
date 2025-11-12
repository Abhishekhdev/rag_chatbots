import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, AudioProcessorBase
import av, speech_recognition as sr, pyttsx3
import google.generativeai as genai
import io

# 🔑 Configure Gemini API
genai.configure(api_key="AIzaSyCYWQ7GiDxYg_1Y72JgU38DfQCg_yeaJ5c")

st.title("🎤 Gemini Voice-to-Voice Assistant")

recognizer = sr.Recognizer()
engine = pyttsx3.init()

class AudioProcessor(AudioProcessorBase):
    def recv_audio(self, frame: av.AudioFrame) -> av.AudioFrame:
        audio_data = frame.to_ndarray().flatten().tobytes()

        try:
            # Convert audio bytes to text using SpeechRecognition
            with sr.AudioFile(io.BytesIO(audio_data)) as source:
                audio = recognizer.record(source)
                text = recognizer.recognize_google(audio)
                st.write(f"🗣️ You said: {text}")

                # Send recognized text to Gemini
                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content(text)

                reply = response.text
                st.write(f"🤖 Gemini: {reply}")

                # Convert AI reply to speech
                engine.say(reply)
                engine.runAndWait()

        except Exception as e:
            st.write("🎧 Listening...")

        return frame


webrtc_streamer(
    key="voice-to-voice",
    mode=WebRtcMode.SENDRECV,
    audio_processor_factory=AudioProcessor,
    media_stream_constraints={"audio": True, "video": False},
)
