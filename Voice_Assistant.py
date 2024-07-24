import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import tkinter as tk
import threading

recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        update_status("Listening...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print(f"User said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I did not understand that.")
            update_status("Waiting...")
            return ""
        except sr.RequestError:
            speak("Sorry, there seems to be an issue with the service.")
            update_status("Waiting...")
            return ""

def handle_command(command):
    if "hello" in command:
        response = "Hello! How can I help you today?"
        speak(response)
    elif "time" in command:
        current_time = datetime.datetime.now().strftime("%H:%M")
        response = f"The current time is {current_time}"
        speak(response)
    elif "date" in command:
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        response = f"Today's date is {current_date}"
        speak(response)
    elif "search for" in command:
        search_query = command.replace("search for", "").strip()
        url = f"https://www.google.com/search?q={search_query}"
        webbrowser.open(url)
        response = f"Here are the search results for {search_query}"
        speak(response)
    elif "open" in command:
        website = command.replace("open", "").strip()
        url = f"https://{website}"
        webbrowser.open(url)
        response = f"Opening {website}"
        speak(response)
    else:
        response = "Sorry, I can only respond to basic commands for now."
        speak(response)
    
    update_status("Waiting...")

def listen_and_handle():
    while listening:
        command = listen()
        if command:
            handle_command(command)

def start_listening():
    global listening
    listening = True
    global listening_thread
    listening_thread = threading.Thread(target=listen_and_handle)
    listening_thread.start()

def stop_listening():
    global listening
    listening = False
    speak("Goodbye!")
    root.quit()

def update_status(status):
    status_label.config(text=status, fg="green" if status == "Listening..." else "red")

root = tk.Tk()
root.title("Voice Assistant")
root.geometry("600x600")
root.configure(bg="#f0f0f0")

frame = tk.Frame(root, bg="#f0f0f0")
frame.pack(pady=20)

emoji_label = tk.Label(frame, text="🤖", font=("Arial", 120, "bold"), bg="#f0f0f0")
emoji_label.grid(row=0, column=0, columnspan=2)

status_label = tk.Label(frame, text="Waiting...", font=("Helvetica", 24), bg="#f0f0f0")
status_label.grid(row=1, column=0, columnspan=2, pady=10)

start_button = tk.Button(frame, text="Start Listening", command=start_listening, bg="green", fg="white", font=("Helvetica", 14))
start_button.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

stop_button = tk.Button(frame, text="Stop Listening", command=stop_listening, bg="red", fg="white", font=("Helvetica", 14))
stop_button.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

root.mainloop()