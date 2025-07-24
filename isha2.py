import tkinter as tk
from tkinter import scrolledtext
import speech_recognition as sr
import pyttsx3
import datetime
import os
import pyautogui
import webbrowser
import random
from threading import Thread

# =============== Check for Microphone ===============
mic_available = False
try:
    mic_list = sr.Microphone.list_microphone_names()
    if len(mic_list) > 0:
        mic_available = True
except:
    mic_available = False

# =============== Initialize ===============
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 0.9)
recognizer = sr.Recognizer()
mic_active = False

# =============== Speak Function ===============
def speak(text):
    chat_box.insert(tk.END, f"ISHA: {text}\n")
    chat_box.see(tk.END)
    engine.say(text)
    engine.runAndWait()

# =============== Listen Function ===============
def listen():
    if not mic_available:
        return ""
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = recognizer.listen(source, timeout=5)
            command = recognizer.recognize_google(audio).lower()
            return command
        except:
            return ""

# =============== Command Functions ===============
def get_time():
    speak("Current time is " + datetime.datetime.now().strftime("%I:%M %p"))

def get_date():
    speak("Today's date is " + datetime.date.today().strftime("%B %d, %Y"))

def solve_math(expression):
    try:
        result = eval(expression)
        speak("The result is " + str(result))
    except:
        speak("Sorry, I could not solve that.")

def show_settings_popup():
    settings = [
        "Display setting (01)", "Sound setting (03)", "Notification (07)", "Focus assist (08)",
        "Power & sleep (04)", "Storage (05)", "Multitasking (088)", "Projecting (099)",
        "Shared experiences (076)", "Clipboard (054)", "Remote desktop (00)", "Optional features (021)",
        "About setting (007)", "System (0022)", "Devices (0033)", "Mobile devices (0044)",
        "Network & internet (0055)", "Personalization (0066)", "Apps (0099)", "Account (0088)",
        "Time & language (0010)", "Gaming (0009)", "Ease of access (0080)", "Privacy (0076)",
        "Update & security (0087)"
    ]
    popup = tk.Toplevel(root)
    popup.title("All Settings")
    popup.geometry("400x400")
    tk.Label(popup, text="Settings List:", font=('Arial', 14)).pack()
    scroll = scrolledtext.ScrolledText(popup, wrap=tk.WORD, width=40, height=20)
    scroll.pack(padx=10, pady=10)
    for item in settings:
        scroll.insert(tk.END, item + "\n")

def show_apps_popup():
    apps = [
        "Alarms & Clock", "Calculator", "Calendar", "Camera", "Copilot", "Cortana", "Game Bar",
        "Groove Music", "Mail", "Maps", "Microsoft Edge", "Solitaire", "Microsoft Store",
        "Mixed Reality Portal", "Movies & TV", "Office", "OneDrive", "OneNote", "Outlook", "Paint",
        "Paint 3D", "Phone Link", "PowerPoint", "Settings", "Skype", "Snip & Sketch", "Sticky Notes",
        "Tips", "Voice Recorder", "Weather", "Windows Backup", "Windows Security", "Word", "Xbox",
        "About your PC", "Notepad", "CMD", "Excel", "Control Panel", "File Explorer"
    ]
    popup = tk.Toplevel(root)
    popup.title("All Apps")
    popup.geometry("400x400")
    tk.Label(popup, text="Apps List:", font=('Arial', 14)).pack()
    scroll = scrolledtext.ScrolledText(popup, wrap=tk.WORD, width=40, height=20)
    scroll.pack(padx=10, pady=10)
    for item in apps:
        scroll.insert(tk.END, item + "\n")

def open_setting_by_code(code):
    mapping = {
        "01": "display", "03": "sound", "07": "notifications", "08": "quiethours",
        "04": "powersleep", "05": "storagesense", "088": "multitasking", "099": "project",
        "076": "crossdevice", "054": "clipboard", "00": "remotedesktop", "021": "optionalfeatures",
        "007": "about", "0022": "system", "0033": "devices", "0044": "mobile-devices",
        "0055": "network", "0066": "personalization", "0099": "appsfeatures", "0088": "yourinfo",
        "0010": "dateandtime", "0009": "gaming", "0080": "easeofaccess", "0076": "privacy",
        "0087": "windowsupdate"
    }
    if code in mapping:
        os.system(f"start ms-settings:{mapping[code]}")
        speak("Opening setting")
    else:
        speak("Invalid code")

def open_app(name):
    apps = {
        "calculator": "calc", "notepad": "notepad", "cmd": "cmd", "paint": "mspaint",
        "file explorer": "explorer", "control panel": "control", "excel": "excel",
        "word": "winword", "powerpoint": "powerpnt", "microsoft edge": "start msedge:",
        "alarms & clock": "start ms-clock:", "calendar": "start outlookcal:",
        "camera": "start microsoft.windows.camera:", "cortana": "start ms-cortana:",
        "copilot": "start ms-copilot:", "game bar": "start xbox-gamebar:",
        "groove music": "start mswindowsmusic:", "mail": "start outlookmail:",
        "maps": "start bingmaps:", "microsoft solitaire collection": "start microsoft.microsoftsolitairecollection:",
        "microsoft store": "start ms-windows-store:", "mixed reality portal": "start ms-holographicfirstlaunch:",
        "movies & tv": "start mswindowsvideo:", "office": "start ms-officeapp:", "onedrive": "start onedrive:",
        "onenote": "start onenote:", "outlook": "start outlook:", "paint 3d": "start ms-paint:",
        "phone link": "start ms-phone:", "settings": "start ms-settings:", "skype": "start skype:",
        "snip & sketch": "start ms-screenclip:", "sticky notes": "start stikynot:",
        "tips": "start ms-get-started:", "voice recorder": "start ms-voicerecorder:",
        "weather": "start bingweather:", "windows backup": "start ms-settings:backup",
        "windows security": "start windowsdefender:", "xbox": "start xbox:",
        "about your pc": "start ms-settings:about"
    }
    name = name.lower()
    if name in apps:
        os.system(apps[name])
        speak(f"Opening {name}")
    else:
        speak("App not found")

# =============== Process Command ===============
def process_command(cmd):
    if not cmd: return
    if "time" in cmd: get_time()
    elif "date" in cmd: get_date()
    elif "solve" in cmd or any(op in cmd for op in ['+', '-', '*', '/']): solve_math(cmd)
    elif "about all setting" in cmd: show_settings_popup()
    elif "about all app" in cmd: show_apps_popup()
    elif "open" in cmd:
        for word in cmd.split():
            if word.isdigit():
                open_setting_by_code(word)
                return
        name = cmd.replace("open", "").strip()
        open_app(name)
    elif "search" in cmd or "find now" in cmd:
        speak("What should I search?")
        query = listen()
        if query:
            speak(f"Searching for {query}")
            webbrowser.open(f"https://www.google.com/search?q={query}")
    elif "play song" in cmd:
        songs = [
            "https://youtu.be/-Me4lYdECn0", "https://youtu.be/ydk-JTPln9I", "https://youtu.be/YJg1rs0R2sE"
        ]
        speak("Playing song")
        webbrowser.open(random.choice(songs))
    elif "screenshot" in cmd:
        pyautogui.screenshot().save("screenshot.png")
        speak("Screenshot saved")
    elif "shutdown" in cmd:
        os.system("shutdown /s /t 1")
    elif "restart" in cmd:
        os.system("shutdown /r /t 1")
    elif "hello" in cmd or "hi" in cmd:
        speak("Hi, how can I help you?")
    elif "thank you" in cmd:
        speak("You're welcome!")
    else:
        speak("Sorry, I didn't understand.")

# =============== GUI Setup ===============
root = tk.Tk()
root.title("ISHA - AI Assistant")
root.geometry("600x400")

chat_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=15, width=60)
chat_box.pack(pady=10)

text_entry = tk.Entry(root, width=50)
text_entry.pack(pady=5)

def on_enter(event=None):
    command = text_entry.get().lower()
    chat_box.insert(tk.END, f"You: {command}\n")
    text_entry.delete(0, tk.END)
    process_command(command)

text_entry.bind("<Return>", on_enter)

def toggle_mic():
    global mic_active
    mic_active = not mic_active
    voice_button.config(bg="green" if mic_active else "red")
    if mic_active:
        Thread(target=mic_loop).start()

def mic_loop():
    while mic_active:
        command = listen()
        if command:
            chat_box.insert(tk.END, f"You: {command}\n")
            chat_box.see(tk.END)
            process_command(command)

voice_button = tk.Button(root, text="🎤 Voice", fg="white", bg="red", command=toggle_mic)
voice_button.pack(pady=5)

if not mic_available:
    voice_button.config(state=tk.DISABLED)

# ✅ FIX: Speak after GUI loads
root.after(100, lambda: speak("Hello, I am ISHA. INTELLIGENT SYSTEM FOR HUMAN ASSISTANCE."))
root.mainloop()