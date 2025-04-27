import pytesseract
from PIL import ImageGrab
import speech_recognition as sr
import pyautogui
import pyttsx3
import cv2
import numpy as np
import time
import os

# 🗣 Setup Tesseract Path (Windows only)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# 🎤 Voice Synthesizer
engine = pyttsx3.init()
engine.setProperty('rate', 150)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def speak(text):
    print("🗣 " + text)
    engine.say(text)
    engine.runAndWait()

# 🎧 Speech Recognition
recognizer = sr.Recognizer()

def listen_command():
    with sr.Microphone() as source:
        print("🎤 Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = recognizer.listen(source, timeout=3, phrase_time_limit=5)
            command = recognizer.recognize_google(audio).lower()
            print("✅ You said:", command)
            return command
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that.")
        except sr.RequestError:
            speak("Speech service is unavailable.")
        except sr.WaitTimeoutError:
            print("⌛ Timeout while listening.")
    return ""

def find_and_click_text(target_word):
    print(f"🔍 Searching for '{target_word}' on screen...")
    screenshot = ImageGrab.grab()
    open_cv_image = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    data = pytesseract.image_to_data(open_cv_image, output_type=pytesseract.Output.DICT)
    
    for i, word in enumerate(data["text"]):
        if target_word.lower() in word.lower():
            x, y, w, h = data["left"][i], data["top"][i], data["width"][i], data["height"][i]
            center_x = x + w // 2
            center_y = y + h // 2
            pyautogui.moveTo(center_x, center_y)
            pyautogui.click()
            response = f"I clicked on {word}"
            speak(response)
            return
    speak(f"I couldn't find {target_word} on screen.")

# 🚀 Main Program
def main():
    speak("Voice-controlled mouse with OCR is ready.")
    while True:
        command = listen_command()
        if "click" in command:
            try:
                target = command.split("click", 1)[1].strip()
                if target:
                    find_and_click_text(target)
            except Exception as e:
                speak("There was an error handling your command.")
        elif "exit" in command or "quit" in command:
            speak("Shutting down voice mouse. Goodbye!")
            break
        time.sleep(0.5)

if __name__ == "__main__":
    main()
