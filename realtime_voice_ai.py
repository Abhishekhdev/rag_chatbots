import os
import time
import pygame
import speech_recognition as sr
from gtts import gTTS
import google.generativeai as genai

# ✅ Step 1: Configure Gemini API
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("❌ ERROR: GEMINI_API_KEY not found. Please set your API key in environment variables.")
    exit()

genai.configure(api_key=api_key)

# 🔹 Use a known working Gemini model for text generation
valid_model_name = "models/gemini-2.5-pro"
model = genai.GenerativeModel(valid_model_name)
print(f"Using Gemini model: {valid_model_name}")

# 🔊 Convert text → speech
def speak(text):
    try:
        os.makedirs("temp", exist_ok=True)  # Ensure temp folder exists

        # Save unique file to avoid permission conflicts
        tts_file = f"temp/reply_{int(time.time() * 1000)}.mp3"
        tts = gTTS(text=text, lang='en')
        tts.save(tts_file)

        pygame.mixer.init()
        pygame.mixer.music.load(tts_file)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            time.sleep(0.5)
    except Exception as e:
        print(f"⚠️ TTS error: {e}")

# 🧠 Ask Gemini model
def ask_gemini(prompt):
    try:
        response = model.generate_content(prompt)
        reply = response.text.strip()
        print(f"🤖 Gemini: {reply}")
        return reply
    except Exception as e:
        print(f"⚠️ Gemini API error: {e}")
        return "Sorry, there was a problem connecting to Gemini."

# 🎤 Real-time continuous listening
def continuous_listen():
    recognizer = sr.Recognizer()

    # ⚡ Set thresholds for better laptop mic recognition
    recognizer.energy_threshold = 400
    recognizer.dynamic_energy_threshold = True
    recognizer.pause_threshold = 0.4
    recognizer.non_speaking_duration = 0.2

    # List and select microphone
    mic_list = sr.Microphone.list_microphone_names()
    print("Available microphones:", mic_list)
    mic_index = 0  # replace with your laptop mic index
    mic = sr.Microphone(device_index=mic_index)

    with mic as source:
        # Calibrate for ambient noise
        print("🎧 Calibrating for ambient noise, please wait...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("🎧 Gemini Voice Assistant is ready! (Say 'stop' to exit)")

        try:
            while True:
                print("🎙️ Listening...")
                audio = recognizer.listen(source, phrase_time_limit=5)  # limit per phrase

                try:
                    text = recognizer.recognize_google(audio)
                    print(f"🧑 You said: {text}")

                    if text.lower() in ["stop", "exit", "quit"]:
                        print("👋 Goodbye!")
                        speak("Goodbye! Have a great day!")
                        break

                    reply = ask_gemini(text)
                    speak(reply)

                except sr.UnknownValueError:
                    print("⚠️ Could not understand audio.")
                except sr.RequestError as e:
                    print(f"⚠️ Speech Recognition error: {e}")

        except KeyboardInterrupt:
            print("\n👋 Stopped by user")
            speak("Goodbye! Have a great day!")

# 🚀 Run the assistant
if __name__ == "__main__":
    continuous_listen()
