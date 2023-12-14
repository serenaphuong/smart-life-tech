import pyttsx3
import speech_recognition as sr

# Set up Text-to-Speech
engine = pyttsx3.init()

# Set up SpeechRecognition
recognizer = sr.Recognizer()

# Function to speak text
def speak_text(text):
    engine.say(text)
    engine.runAndWait()

# Function to capture speech and return text
def recognize_speech():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        print("Processing...")
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "Speech not recognized"
    except sr.RequestError as e:
        return f"Error: {e}"

if __name__ == "__main__":
    # Text-to-Speech
    text_to_speak = "Hello, how are you?"
    speak_text(text_to_speak)

    # Speech-to-Text
    recognized_text = recognize_speech()
    print(f"Recognized Text: {recognized_text}")
