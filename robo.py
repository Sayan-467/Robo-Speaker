from flask import Flask, request
import os
import pyttsx3
from tkinter import *
from tkinter import ttk
from tkinter import filedialog, messagebox
from gtts import gTTS
import speech_recognition as sr
from pynput import keyboard
from datetime import datetime

# Initialize ttsx Engine 
engine = pyttsx3.init()

# Main Window 
root = Tk()
root.title("Welcome to Robo Speaker")
root.geometry("600x800")
root.resizable(False, False)

# Title Label
title_label = ttk.Label(root, text="Robo Speaker", font=("Helvetica", 24, "bold"))
title_label.pack(pady=10)

# Text Input Box 
entry = ttk.Entry(root, width=70)
entry.pack(pady=10)

# Functions for speak, clear and exit text 
def speak_text():
    text = entry.get().strip()
    if text:
        engine.say(text)
        engine.runAndWait()
    else:
        messagebox.showwarning("Enter valid text to speak")

def clear_text():
    entry.delete(0, 10000)

def exit_app():
    engine.say("Time to quit")
    engine.runAndWait()
    root.destroy()

# GUI formation function
speak_btn = ttk.Button(root, text="Speak", width=25, command=speak_text)
speak_btn.pack()

clear_btn = ttk.Button(root, text="Clear", width=25, command=clear_text)
clear_btn.pack()

exit_btn = ttk.Button(root, text="Exit", width=25, command=exit_app)
exit_btn.pack()

# Enhanching the voice
engine.setProperty('rate', 150)
engine.setProperty('volume', 0.8)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# Adding file input 
def openFile():
    filePath = filedialog.askopenfilename(filetypes=[("Text file", "*.txt")])
    if filePath == True:
        with open(filePath, 'r') as file:
            content = file.read()
            entry.delete("1", ttk.END)
            entry.insert(ttk.END, content)
            engine.say(content)
            engine.runAndWait()

# text to audio file conversion 
def exportAudio():
    text = entry.get("1", ttk.END).strip()
    if text:
        try:
            audio = gTTS(text=text, lang='en', slow=False)
            file_path = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=[("MP3 files", "*.mp3")])

            if file_path:
                audio.save(file_path)
                messagebox.showinfo("Success", f"Audio saved as {file_path}")
        except Exception as e:
            messagebox.showinfo("Error", f"Error occured as {e}")
    else:
        messagebox.showinfo("Please enter valid input to avoid an input error ...")

# Buttons for File Upload and Export to Audio
file_btn = ttk.Button(root, text="Open File & Speak", command=openFile, width=15)
file_btn.pack(pady=5)

export_btn = ttk.Button(root, text="Export as MP3", command=exportAudio, width=15)
export_btn.pack(pady=5)

# Changing System Voice 
def change_voice():
    current_voice = engine.getProperty("voice")
    if current_voice == voices[0].id:
        engine.setProperty("voice", voices[1].id)
        voice_btn.config(text="Switch to Male Voice")
    else:
        engine.setProperty("voice", voices[0].id)
        voice_btn.config(text="Switch to Female Voice")

# Buttons for Changing Current Voice 
voice_btn = ttk.Button(root, text="Switch to Female Voice", command=change_voice, width=15)
voice_btn.pack(pady=5)

# Change the Speech Rate and Speech Volume 
def speech_rate(val):
    engine.setProperty("rate", float(val))

def speech_volume(val):
    engine.setProperty("volume", float(val))

# Buttons for Changing Speech Rate and Volume
rate_label = ttk.Label(root, text="Speech Rate", font=("Helvetica", 12))
rate_label.pack()

rate_slider = ttk.Scale(root, from_=50, to=300, orient="horizontal", command=speech_rate)
rate_slider.set(150)
rate_slider.pack()

volume_label = ttk.Label(root, text="Volume", font=("Helvetica", 12))
volume_label.pack()

volume_slider = ttk.Scale(root, from_=0.0, to=1.0, orient="horizontal", command=speech_volume)
volume_slider.set(0.8)
volume_slider.pack()

# Adding Hotkey Support 
def onPress(key):
    try:
        if key.char == 's':
            engine.say("You pressed S ...")
            engine.runAndWait()
    except AttributeError:
        pass

with keyboard.Listener(on_press=onPress) as listener:
    listener.join()

# Adding Personalization 
now = datetime.now()
hour = now.hour

def addGreetings():
    if hour < 12:
        greeting = "Good Morning"
    elif 12 <= hour < 18:
        greeting = "Good Afternoon"
    else:
        greeting = "Good Evening"

    engine.say(f"{greeting}, Welcome to Robo Speaker")
    engine.runAndWait()

addGreetings()

# Footer
footer_label = ttk.Label(root, text="Created by Sayan", font=("Helvetica", 10))
footer_label.pack(pady=20)

# Start the Application 
root.mainloop()
