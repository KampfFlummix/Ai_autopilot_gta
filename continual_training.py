import tensorflow as tf
tf.config.run_functions_eagerly(True)

import os
import json
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.utils import to_categorical
import cv2
import shutil

print("Current working directory:", os.getcwd())
print("Model file exists:", os.path.exists("models/gta_model.h5"))

os.chdir("C:/Projects/Autopilot")

IMG_SIZE = (160, 120)
DATA_DIR = "training_data"
MODEL_PATH = "models/gta_model.h5"

def load_data():
    with open(os.path.join(DATA_DIR, "labels.json"), "r") as f:
        labels_dict = json.load(f)

    images = []
    labels = []

    for img_name, keys in labels_dict.items():
        img_path = os.path.join(DATA_DIR, img_name)
        if os.path.exists(img_path):
            img = cv2.imread(img_path)
            img = cv2.resize(img, IMG_SIZE)
            img = img / 255.0
            images.append(img)
            labels.append(keys)

    return np.array(images), labels

# 🔁 Bestehendes Modell laden
print("📦 Lade bestehendes Modell...")
model = load_model(MODEL_PATH)

# 📥 Neue Daten laden
print("📊 Lade neue Daten...")
X, y_raw = load_data()
from tensorflow.keras.utils import to_categorical

labels_map = {'w':0, 's':1, 'a':2, 'd':3, 'space':4, 'shift':5, 'ctrl':6}

y = []
for keys in y_raw:
    # Nimm den ersten Key oder 'w', falls leer
    action_key = keys[0] if keys else 'w'
    y.append(labels_map.get(action_key, 0))

y = to_categorical(y, num_classes=len(labels_map))

# Modell neu kompilieren mit passendem Optimizer, Loss und Metriken
model.compile(
    optimizer=Adam(learning_rate=0.001),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# 📚 Weiter trainieren
print(f"🧠 Trainiere auf {len(X)} neuen Beispielen...")
model.fit(X, y, epochs=5, batch_size=32)
model.save(MODEL_PATH)
print("✅ Modell gespeichert.")


# 🧹 Automatisch Daten aufräumen
ARCHIVE_DIR = os.path.join(DATA_DIR, "archiviert")
os.makedirs(ARCHIVE_DIR, exist_ok=True)

for filename in os.listdir(DATA_DIR):
    file_path = os.path.join(DATA_DIR, filename)
    if filename.endswith(".jpg") or filename == "labels.json":
        shutil.move(file_path, os.path.join(ARCHIVE_DIR, filename))

print("🧼 Alte Trainingsdaten verschoben nach:", ARCHIVE_DIR)
