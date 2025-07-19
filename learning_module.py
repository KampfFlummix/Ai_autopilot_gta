import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Conv2D, Flatten
from config import DATA_LOG_PATH, MODEL_PATH, LEARNING_RATE, BATCH_SIZE

class LearningModule:
    def __init__(self):
        self.model = self.load_or_create_model()
        self.data_buffer = []
        
    def load_or_create_model(self):
        if os.path.exists(MODEL_PATH):
            return load_model(MODEL_PATH)
        else:
            model = Sequential([
                Conv2D(32, (3,3), activation='relu', input_shape=(100, 100, 3)),
                Flatten(),
                Dense(128, activation='relu'),
                Dense(2, activation='linear')  # Steering, Speed
            ])
            model.compile(optimizer=tf.keras.optimizers.Adam(LEARNING_RATE),
                          loss='mse')
            return model
            
    def record_data(self, frame, metadata):
        # Frame verkleinern
        small_frame = cv2.resize(frame, (100, 100))
        self.data_buffer.append({
            'frame': small_frame,
            'controls': metadata['controls']
        })
        
        # Automatisches Speichern alle 100 Einträge
        if len(self.data_buffer) >= 100:
            self.save_data()
            
    def save_data(self):
        if not self.data_buffer:
            return
            
        # Daten für Training vorbereiten
        X = np.array([item['frame'] for item in self.data_buffer])
        y = np.array([
            [item['controls']['steering'], item['controls']['speed'] 
            for item in self.data_buffer
        ])
        
        # Modell trainieren
        self.model.fit(X, y, batch_size=BATCH_SIZE, epochs=1, verbose=0)
        
        # Modell speichern
        self.model.save(MODEL_PATH)
        
        # Puffer leeren
        self.data_buffer = []
        print("Daten gespeichert und Modell aktualisiert")