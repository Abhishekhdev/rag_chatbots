import os
import speech_recognition as sr
import pyttsx3
from modules.llm_chain import ask_question  # Use your Gemini-based RAG function
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize text-to-speech
engine = pyttsx3.init()

def speak(text):
    """Convert text to speech"""
    engine.say(text)
    engine.runAndWait()

def recognize_speech():
    """Capture and recognize speech"""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙️ Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            print(f"🗣️ You said: {text}")
            return text
        except sr.UnknownValueError:
            print("❌ Sorry, I didn't understand that.")
            return None
        except sr.RequestError:
            print("⚠️ Speech recognition service error.")
            return None

def main():
    print("🤖 Gemini Voice RAG Chat Started. Say 'exit' to stop.")
    while True:
        question = recognize_speech()
        if not question:
            continue
        if question.lower() in ["exit", "quit", "stop"]:
            speak("Goodbye!")
            break

        print("🔍 Retrieving context and generating answer...")
        answer = ask_question(question)
        print(f"🤖 AI: {answer}")
        speak(answer)

if __name__ == "__main__":
    main()
