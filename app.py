import streamlit as st
from pathlib import Path
from streamlit_lottie import st_lottie
import requests
from dotenv import load_dotenv
import os

# Voice Addons
from streamlit_mic_recorder import mic_recorder
import pyttsx3

# Real-time voice feature
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase, RTCConfiguration, WebRtcMode

# --- RAG Chatbot Imports ---
from modules.text_extraction import extract_text
from modules.text_processing import chunk_text
from modules.embeddings_store import add_documents_to_faiss
from modules.llm_chain import ask_question
from modules.config import UPLOAD_DIR

# --- Load environment variables ---
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# --- Import Gemini ---
import google.generativeai as genai
genai.configure(api_key=GEMINI_API_KEY)

# --- Helper function to load Lottie animations ---
def load_lottie_url(url: str):
    try:
        r = requests.get(url)
        if r.status_code == 200:
            return r.json()
    except Exception as e:
        st.warning(f"⚠️ Failed to load Lottie animation: {e}")
    return None

# --- Streamlit Page Setup ---
st.set_page_config(page_title="RAG & Voice Chatbot", page_icon="🤖", layout="centered")
st.sidebar.title("Select Mode")
mode = st.sidebar.radio("Choose chatbot mode:", ["RAG Document Chatbot", "Real-Time Voice Assistant"])

# =========================
# 📘 RAG DOCUMENT CHATBOT
# =========================
if mode == "RAG Document Chatbot":
    st.markdown("""
        <style>
            .main {
                max-width: 640px;
                margin: 40px auto;
                background: #f8fafc;
                padding: 25px 40px 32px 40px;
                border-radius: 24px;
                box-shadow: 0 6px 32px rgba(56,108,220,0.10);
            }
            .step-title {
                font-size: 1.2em;
                font-weight: 700;
                color: #3b82f6;
                margin-top: 10px;
            }
        </style>
    """, unsafe_allow_html=True)
    st.markdown('<div class="main">', unsafe_allow_html=True)

    lottie_url = "https://assets2.lottiefiles.com/packages/lf20_Cc8Bpg.json"
    lottie_json = load_lottie_url(lottie_url)

    st.title("📚 RAG Chatbot")
    st.markdown("##### Upload PDF, DOCX, or Image and ask questions instantly! 🚀")
    if lottie_json:
        st_lottie(lottie_json, speed=1, width=120, height=120, loop=True)

    Path(UPLOAD_DIR).mkdir(parents=True, exist_ok=True)
    st.markdown("---")
    st.markdown('<div class="step-title">1️⃣ Upload your document</div>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "📂 Drag & drop or browse your file",
        type=["pdf", "docx", "doc", "png", "jpg", "jpeg"]
    )

    if uploaded_file:
        file_path = UPLOAD_DIR / uploaded_file.name
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.success(f"✅ File '{uploaded_file.name}' uploaded successfully!")
        with st.spinner("🔄 Extracting and processing text..."):
            try:
                text = extract_text(file_path)
                chunks = chunk_text(text)
                add_documents_to_faiss(chunks, uploaded_file.name)
                st.balloons()
                st.success("🎉 Document ingested and ready for questions!")
            except Exception as e:
                st.error(f"⚠️ Error while processing file: {e}")

    st.markdown("---")
    st.markdown('<div class="step-title">2️⃣ Ask your question</div>', unsafe_allow_html=True)
    st.markdown("🎤 Or use your voice to ask:")

    mic_val = mic_recorder(
        start_prompt="🎙️ Start Recording",
        stop_prompt="⏹️ Stop Recording",
        just_once=True,
        use_container_width=False,
    )

    with st.form(key='chat_form', clear_on_submit=True):
        user_question = st.text_input("💬 Type your question here:")
        if mic_val and isinstance(mic_val, dict) and mic_val.get("text"):
            user_question = mic_val["text"]
            st.info(f"🎧 Voice input: {user_question}")

        send_button = st.form_submit_button("🚀 Send")

        if send_button and user_question:
            with st.spinner("🤔 Thinking..."):
                try:
                    answer = ask_question(user_question)
                    st.success(answer)
                    engine = pyttsx3.init()
                    engine.say(answer)
                    engine.runAndWait()
                except Exception as e:
                    st.error(f"⚠️ Error: {str(e)}")

    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# 🗣️ REAL-TIME VOICE ASSISTANT (Integrated with RAG)
# =========================
elif mode == "Real-Time Voice Assistant":
    st.header("🗣️ Real-Time Voice-to-Voice RAG AI Conversation")

    import tempfile
    import numpy as np
    import whisper
    import soundfile as sf
    import threading

    st.info(
        "🎧 Speak to your **RAG-powered AI Assistant** in real-time!\n\n"
        "📄 It uses your uploaded document context (FAISS + embeddings)\n"
        "🧠 Whisper for speech-to-text, RAG for response, and pyttsx3 for voice output.\n"
        "If your mic doesn’t work, ensure browser microphone access is allowed."
    )

    whisper_model = whisper.load_model("small")
    gemini_model = genai.GenerativeModel("gemini-1.5-flash")

    if "user_said" not in st.session_state:
        st.session_state["user_said"] = ""
    if "ai_reply" not in st.session_state:
        st.session_state["ai_reply"] = ""
    if "error" not in st.session_state:
        st.session_state["error"] = ""

    class VoiceBotProcessor(AudioProcessorBase):
        def __init__(self):
            self.last_user_text = ""
            self.engine = pyttsx3.init()

        def recv(self, frame):
            try:
                audio = frame.to_ndarray().flatten().astype(np.float32)
                with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_wav:
                    sf.write(temp_wav.name, audio, 48000)
                    result = whisper_model.transcribe(temp_wav.name)

                user_text = result.get("text", "").strip()
                if not user_text or user_text == self.last_user_text:
                    return frame

                self.last_user_text = user_text
                st.session_state["user_said"] = user_text

                # 🎯 Try RAG response first
                try:
                    ai_reply = ask_question(user_text)
                    if not ai_reply or len(ai_reply.strip()) < 3:
                        raise ValueError("Empty RAG reply")
                except Exception:
                    # 🔄 Fallback to Gemini if RAG fails
                    response = gemini_model.generate_content(user_text)
                    ai_reply = getattr(response, "text", "Sorry, I couldn’t generate a reply.")

                st.session_state["ai_reply"] = ai_reply

                # 🎤 Speak asynchronously
                threading.Thread(target=self._speak, args=(ai_reply,), daemon=True).start()

            except Exception as e:
                st.session_state["error"] = f"⚠️ Audio processing error: {e}"

            return frame

        def _speak(self, text):
            try:
                self.engine.stop()
                self.engine.say(text)
                self.engine.runAndWait()
            except:
                pass

    rtc_config = RTCConfiguration(
        {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
    )

    webrtc_streamer(
        key="voice-ai",
        mode=WebRtcMode.SENDRECV,
        audio_processor_factory=VoiceBotProcessor,
        media_stream_constraints={"audio": True, "video": False},
        rtc_configuration=rtc_config,
        async_processing=True
    )

    st.markdown("<style>video{display:none;}</style>", unsafe_allow_html=True)

    st.subheader("🎤 Live Transcript")
    st.write(f"**🧍 You said:** {st.session_state.get('user_said', '')}")
    st.write(f"**🤖 AI replied:** {st.session_state.get('ai_reply', '')}")
    if st.session_state.get("error"):
        st.warning(st.session_state["error"])
