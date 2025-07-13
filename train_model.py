import os
import json
import cv2
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, Flatten, Dense, Input
from tensorflow.keras.utils import to_categorical

# Pfade
BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "training_data")
MODEL_DIR = os.path.join(BASE_DIR, "models")
os.makedirs(MODEL_DIR, exist_ok=True)

labels_map = {'w':0, 's':1, 'a':2, 'd':3, 'space':4, 'shift':5, 'ctrl':6}

# Labels laden
labels_file = os.path.join(DATA_DIR, "labels.json")
if not os.path.exists(labels_file):
    print(f"Labels-Datei nicht gefunden: {labels_file}")
    exit(1)

with open(labels_file, "r") as f:
    labels = json.load(f)

X, y = [], []
for img_name, keys in labels.items():
    path = os.path.join(DATA_DIR, img_name)
    img = cv2.imread(path)
    if img is None:
        print(f"Warnung: Bild nicht gefunden oder fehlerhaft: {path}")
        continue
    img = cv2.resize(img, (160,120))
    X.append(img)
    # Für Einfachheit: erster Key oder 'w' wenn leer
    action_key = keys[0] if keys else 'w'
    y.append(labels_map.get(action_key, 0))

if not X or not y:
    print("Keine gültigen Trainingsdaten gefunden!")
    exit(1)

X = np.array(X) / 255.0
y = to_categorical(y, num_classes=len(labels_map))

model = Sequential([
    Input(shape=(120,160,3)),
    Conv2D(16, (3,3), activation='relu'),
    Conv2D(32, (3,3), activation='relu'),
    Flatten(),
    Dense(64, activation='relu'),
    Dense(len(labels_map), activation='softmax')
])
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.fit(X, y, epochs=5, batch_size=16)

model.save(os.path.join(MODEL_DIR, "gta_model.h5"))
print("Modell gespeichert in models/gta_model.h5")