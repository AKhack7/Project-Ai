import os
import time
import pyttsx3
import speech_recognition as sr
import webbrowser
import pyautogui
import random
import requests
import datetime
import threading
import subprocess
from flask import Flask, request, send_file

# 🔹 Flask App Setup
app = Flask(__name__)

@app.route('/')
def index():
    return send_file('index.html')

@app.route('/style.css')
def style():
    return send_file('style.css')

@app.route('/script.js')
def script():
    return send_file('script.js')

@app.route('/start-ai', methods=['GET'])
def start_ai():
    threading.Thread(target=main).start()
    return "AI Assistant Started"

# 🔹 Voice Engine Setup
engine = pyttsx3.init()
engine.setProperty('rate', 170)
engine.setProperty('volume', 1.0)
engine.setProperty('voice', engine.getProperty('voices')[1].id)  # Female voice

def speak(text):
    print(f"Isha: {text}")
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = recognizer.listen(source)
            command = recognizer.recognize_google(audio).lower()
            print(f"You said: {command}")
            return command
        except sr.UnknownValueError:
            return None
        except sr.RequestError:
            return None

def wish_me():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good morning!")
    elif 12 <= hour < 18:
        speak("Good afternoon!")
    else:
        speak("Good evening!")


def find_now():
    speak("What do you want me to search?")
    query = listen()
    if query:
        url = f"https://www.google.com/search?q={query}"
        webbrowser.open(url)
        speak(f"Searching for {query}")

def activate_red_mode():
    speak("Red mode activated. Just kidding!")

def open_software(command):
    speak("Which software do you want to open?")

def close_software(command):
    speak("Closing the software.")

def open_youtube():
    webbrowser.open("https://youtube.com")

def open_google():
    webbrowser.open("https://google.com")

def open_instagram():
    webbrowser.open("https://instagram.com")

def open_whatsapp():
    webbrowser.open("https://web.whatsapp.com")

def take_screenshot():
    filename = f"screenshot_{int(time.time())}.png"
    pyautogui.screenshot().save(filename)
    speak("Screenshot taken")

def shutdown_pc():
    speak("Shutting down the system")
    os.system("shutdown /s /t 1")

def restart_pc():
    speak("Restarting the system")
    os.system("shutdown /r /t 1")

def get_weather():
    speak("Currently, weather information is not integrated.")

def get_time():
    now = datetime.datetime.now().strftime("%H:%M:%S")
    speak(f"The time is {now}")

def calculate_expression(command):
    command = command.replace("calculate", "").strip()
    try:
        result = eval(command)
        speak(f"The answer is {result}")
    except:
        speak("Sorry, I couldn't calculate that.")

def thank_you_reply():
    responses = ["You're welcome!", "No problem!"]
    speak(random.choice(responses))

def hello():
    responses = ["Hi there!", "Hello! How can I help?"]
    speak(random.choice(responses))

def start_translation():
    speak("Which language should I translate into?")
    language = listen()
    speak("I am listening for translation.")
    while True:
        text = listen()
        if text == "stop translation":
            break
        translated_text = f"(Translated in {language}) {text}"
        speak(translated_text)

playlist_links = [
    "https://youtube.com/playlist?list=PLF1lUEthDOiRy8JyacQBqORxyW6nk2Zv6",
    "https://youtube.com/playlist?list=PL2Zx_3d_dxUh1oZqrdNkCsh5JT4_e2KF0",
    "https://youtube.com/playlist?list=PLQgFnvIVU9qsveEcsrbMcVSy9jp1K6_Sw",
    "https://youtube.com/playlist?list=PLQgFnvIVU9qsP0zGD9PYQo0vJJa45vS1G"
]

def play_song():
    webbrowser.open(random.choice(playlist_links))

def main():
    wish_me()
    speak("I AM ISHA.... INTELLIGENT SYSTEM FOR HUMAN ASSISTANCE.")

    while True:
        command = listen()
        if not command:
            continue
        if any(phrase in command for phrase in ["find now", "search", "search now"]):
            find_now()
        elif "activate red mode" in command:
            activate_red_mode()
        elif "open" in command:
            open_software(command)
        elif "close" in command:
            close_software(command)
        elif "youtube" in command:
            open_youtube()
        elif "google" in command:
            open_google()
        elif "instagram" in command:
            open_instagram()
        elif "whatsapp" in command:
            open_whatsapp()
        elif "thank you" in command or "thanks" in command:
            thank_you_reply()
        elif "hello" in command or "hi" in command:
            hello()
        elif "screenshot" in command:
            take_screenshot()
        elif "shutdown" in command or "good night" in command:
            shutdown_pc()
        elif "restart" in command:
            restart_pc()
        elif "weather" in command:
            get_weather()
        elif "time" in command:
            get_time()
        elif "play song" in command or "play music" in command:
            play_song()
        elif "calculate" in command or "calculator" in command:
            calculate_expression(command)

if __name__ == '__main__':
    app.run(debug=True)
