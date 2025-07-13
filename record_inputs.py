import cv2
import numpy as np
import pyautogui
import threading
import time
import os
import json
from pynput import keyboard

# Absoluter Pfad zum Ordner, in dem das Script liegt
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Pfad zum training_data-Ordner (relativ zum Skriptordner)
TRAINING_DATA_DIR = os.path.join(BASE_DIR, 'training_data')

# Wenn Ordner nicht existiert, erstelle ihn
if not os.path.exists(TRAINING_DATA_DIR):
    os.makedirs(TRAINING_DATA_DIR)

# Bildschirmbereich anpassen falls nötig
MONITOR = {"top": 0, "left": 0, "width": 1920, "height": 1080}
DATA_DIR = TRAINING_DATA_DIR
LABELS_FILE = os.path.join(DATA_DIR, "labels.json")
labels = {}
recording = False
current_keys = set()
frame_id = 0

def capture_loop():
    global frame_id
    while recording:
        img = pyautogui.screenshot(region=(MONITOR["left"], MONITOR["top"], MONITOR["width"], MONITOR["height"]))
        img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        img_name = f"{str(frame_id).zfill(6)}.jpg"
        cv2.imwrite(os.path.join(DATA_DIR, img_name), img)
        labels[img_name] = list(current_keys)
        frame_id += 1
        time.sleep(0.1)

def on_press(key):
    try:
        k = key.char.lower()
    except:
        k = key.name
    current_keys.add(k)

def on_release(key):
    try:
        k = key.char.lower()
    except:
        k = key.name
    if k in current_keys:
        current_keys.remove(k)

def start_recording():
    global recording
    recording = True
    threading.Thread(target=capture_loop, daemon=True).start()
    print(">> Aufnahme gestartet.")

def stop_recording():
    global recording
    recording = False
    time.sleep(0.2)
    with open(LABELS_FILE, "w") as f:
        json.dump(labels, f)
    print(">> Aufnahme gestoppt. Labels gespeichert.")

listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()

print("Recorder bereit. Befehle: start, stop, exit")
while True:
    cmd = input(">> ").strip().lower()
    if cmd == "start":
        if not recording:
            start_recording()
        else:
            print("Bereits aufnahme aktiv.")
    elif cmd == "stop":
        if recording:
            stop_recording()
        else:
            print("Keine Aufnahme aktiv.")
    elif cmd == "exit":
        if recording:
            stop_recording()
        print("Beende Recorder.")
        break
    else:
        print("Ungültig. Nutze start, stop oder exit.")
