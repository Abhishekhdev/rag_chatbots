import os
import tempfile
import speech_recognition as sr
from gtts import gTTS
import pygame
import google.generativeai as genai

# ✅ Set Gemini API key
os.environ["GEMINI_API_KEY"] = "AIzaSyCYWQ7GiDxYg_1Y72JgU38DfQCg_yeaJ5c"
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# ✅ Initialize recognizer and TTS player
recognizer = sr.Recognizer()

# ✅ Create safe folder for saving TTS files
TEMP_DIR = os.path.join(os.getcwd(), "temp_audio")
os.makedirs(TEMP_DIR, exist_ok=True)

# ✅ Initialize Gemini model
model = genai.GenerativeModel("gemini-1.5-flash-latest")

def speak(text):
    """Convert text to speech"""
    tts = gTTS(text=text, lang='en')
    temp_path = os.path.join(TEMP_DIR, "output.mp3")
    tts.save(temp_path)
    pygame.mixer.init()
    pygame.mixer.music.load(temp_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue
    pygame.mixer.quit()

def listen():
    """Listen from microphone"""
    with sr.Microphone() as source:
        print("🎙️ Say something...")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        print(f"✅ You said: {text}")
        return text.lower()
    except sr.UnknownValueError:
        print("❌ Could not understand audio")
        return ""
    except sr.RequestError:
        print("⚠️ Speech service error")
        return ""

def chat_with_gemini(prompt):
    """Chat with Gemini"""
    response = model.generate_content(prompt)
    answer = response.text.strip()
    print("🤖 Gemini:", answer)
    return answer

print("🤖 Gemini Voice Chat started! Say 'exit' to stop.")

while True:
    user_input = listen()
    if user_input in ["exit", "quit", "stop"]:
        print("👋 Goodbye!")
        speak("Goodbye!")
        break
    if not user_input:
        continue
    print("🧠 Thinking...")
    try:
        answer = chat_with_gemini(user_input)
        speak(answer)
    except Exception as e:
        print("⚠️ Error:", e)
        speak("Sorry, there was an error while responding.")
