import os
import time
import threading
import cv2
import numpy as np
from tensorflow.keras.models import load_model
import pyautogui  # nur für Screenshots
import keyboard    # Low‑Level Input
from pynput import keyboard as pk

# Paths & Settings
MODEL_PATH = 'models/gta_model.h5'
IMG_SIZE    = (160, 120)
MONITOR     = {'top':0, 'left':0, 'width':1920, 'height':1080}

# ESC-Flag zum Stoppen
stop_requested = False
def on_esc(key):
    global stop_requested
    if key == pk.Key.esc:
        stop_requested = True
        print("🛑 ESC gedrückt – Stoppe Autopilot")

# Starte Listener für ESC
listener = pk.Listener(on_press=on_esc)
listener.start()

print("📦 Lade Modell...")
model = load_model(MODEL_PATH)

print("🚗 Autopilot startet in 3 Sekunden… (ESC zum Stoppen)")
time.sleep(3)

# Mapping der Modell‑Ausgabe auf Keys
KEYS = ['w','a','s','d','shift','ctrl','space']

def release_all():
    for k in KEYS:
        try: keyboard.release(k)
        except: pass

def predict_and_drive():
    global stop_requested
    while not stop_requested:
        # Screenshot
        img = pyautogui.screenshot(region=(MONITOR['left'],MONITOR['top'],MONITOR['width'],MONITOR['height']))
        frame = cv2.resize(np.array(img), IMG_SIZE) / 255.0
        pred  = model.predict(frame[None, ...], verbose=0)[0]

        # Vorherige Tasten alle loslassen
        release_all()
        # Neue drücken, wenn pred>0.5
        for i,k in enumerate(KEYS):
            if pred[i] > 0.5:
                keyboard.press(k)

        time.sleep(0.1)

    # Am Ende sicher alles loslassen
    release_all()
    print("✅ Autopilot gestoppt.")

if __name__ == '__main__':
    predict_and_drive()
