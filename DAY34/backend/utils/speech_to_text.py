import speech_recognition as sr

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for a task command...")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        return text.lower()
    except sr.UnknownValueError:
        return "Sorry, I didn't understand that."
